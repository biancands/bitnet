import gi
import socket
import threading
import json
import random
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure
from bitnet_simulator.physical_layer.baseband import nrz_polar, manchester, bipolar
from bitnet_simulator.physical_layer.carrier import ask, fsk, qam
from bitnet_simulator.link_layer.framing import count_character_framing_from_text, byte_insertion_framing_from_text
from bitnet_simulator.link_layer.error_detection import crc32, parity_bit
from bitnet_simulator.link_layer.error_correction import hamming_encode

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

HOST = '127.0.0.1'
PORT = 4477

def introduce_error(bits, error_rate=0.1):
    bits = list(bits)
    if random.random() < error_rate:
        pos = random.randint(0, len(bits) - 1)
        bits[pos] = '1' if bits[pos] == '0' else '0'
        print(f"Error introduced at position: {pos}")
    return ''.join(bits)

class Transmitter(Gtk.Window):
    def __init__(self):
        super().__init__(title="Transmitter - BitNet")
        self.set_border_width(10)
        self.set_default_size(800, 600)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        self.text_entry = Gtk.Entry()
        self.text_entry.set_placeholder_text("Enter text to transmit")
        vbox.pack_start(self.text_entry, False, False, 0)

        self.framing_combo = Gtk.ComboBoxText()
        self.framing_combo.append_text("Count Character")
        self.framing_combo.append_text("Byte Insertion")
        self.framing_combo.set_active(0)
        vbox.pack_start(self.framing_combo, False, False, 0)

        self.error_detection_combo = Gtk.ComboBoxText()
        self.error_detection_combo.append_text("CRC32")
        self.error_detection_combo.append_text("Parity Bit")
        self.error_detection_combo.append_text("Hamming")
        self.error_detection_combo.set_active(0)
        vbox.pack_start(self.error_detection_combo, False, False, 0)

        self.modulation_combo = Gtk.ComboBoxText()
        self.modulation_combo.append_text("NRZ")
        self.modulation_combo.append_text("Manchester")
        self.modulation_combo.append_text("Bipolar")
        self.modulation_combo.append_text("ASK")
        self.modulation_combo.append_text("FSK")
        self.modulation_combo.append_text("8-QAM")
        self.modulation_combo.set_active(0)
        vbox.pack_start(self.modulation_combo, False, False, 0)

        self.figure = Figure(figsize=(10, 3))
        self.canvas = FigureCanvas(self.figure)
        vbox.pack_start(self.canvas, True, True, 0)

        send_button = Gtk.Button(label="Send")
        send_button.connect("clicked", self.on_send)
        vbox.pack_start(send_button, False, False, 0)

    def on_send(self, widget):
        text = self.text_entry.get_text()
        framing = self.framing_combo.get_active_text()
        error_detection = self.error_detection_combo.get_active_text()
        modulation = self.modulation_combo.get_active_text()

        if not text:
            self.show_error("Please fill in the text field!")
            return

        threading.Thread(target=self.process_and_send, args=(text, framing, error_detection, modulation)).start()

    def process_and_send(self, text, framing, error_detection, modulation):
        try:
            if framing == "Count Character":
                framed_data = count_character_framing_from_text(text)
            elif framing == "Byte Insertion":
                framed_data = byte_insertion_framing_from_text(text)
            else:
                raise ValueError("Unknown framing.")

            if error_detection == "Hamming":
                framed_data = hamming_encode(framed_data)
            elif error_detection == "CRC32":
                framed_data = crc32(framed_data)
            elif error_detection == "Parity Bit":
                framed_data = parity_bit(framed_data)
            else:
                raise ValueError("Unknown error detection type.")

            data_with_error = introduce_error(framed_data)

            if modulation == "NRZ":
                signal = nrz_polar([int(b) for b in data_with_error])
            elif modulation == "Manchester":
                signal = manchester([int(b) for b in data_with_error])
            elif modulation == "Bipolar":
                signal = bipolar([int(b) for b in data_with_error])
            elif modulation == "ASK":
                signal = ask([int(b) for b in data_with_error])
            elif modulation == "FSK":
                signal = fsk([int(b) for b in data_with_error])
            elif modulation == "8-QAM":
                signal = qam([int(b) for b in data_with_error])
            else:
                raise ValueError("Unknown modulation.")

            self.plot_signal(signal, "Modulated Signal")

            self.send_signal(framing, error_detection, modulation, signal)
        except Exception as e:
            self.show_error(str(e))

    def plot_signal(self, signal, title):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(signal, label=title, color="blue")
        ax.set_title(title)
        ax.set_xlabel("Samples")
        ax.set_ylabel("Amplitude")
        ax.grid(True)
        ax.legend()
        self.canvas.draw()

    def send_signal(self, framing, error_detection, modulation, signal):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                payload = {
                    "framing": framing,
                    "error_detection": error_detection,
                    "modulation": modulation,
                    "signal": signal,
                }
                json_payload = json.dumps(payload) + "\n"
                s.sendall(json_payload.encode())
        except Exception as e:
            self.show_error(f"Error sending: {str(e)}")

    def show_error(self, message):
        dialog = Gtk.MessageDialog(
            parent=self, flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CLOSE, text=message
        )
        dialog.run()
        dialog.destroy()


if __name__ == "__main__":
    win = Transmitter()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
