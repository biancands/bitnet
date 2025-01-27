import gi
import socket
import threading
import json
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure
from bitnet_simulator.physical_layer.baseband import nrz_polar_demodulate, manchester_demodulate, bipolar_demodulate
from bitnet_simulator.physical_layer.carrier import ask_demodulate, fsk_demodulate, qam_demodulate
from bitnet_simulator.link_layer.framing import deframe_count_character_to_text, deframe_byte_insertion_to_text
from bitnet_simulator.link_layer.error_detection import verify_crc32, check_parity_bit
from bitnet_simulator.link_layer.error_correction import hamming_decode

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

HOST = '127.0.0.1'
PORT = 4477

class Receiver(Gtk.Window):
    def __init__(self):
        super().__init__(title="Receiver - BitNet")
        self.set_border_width(10)
        self.set_default_size(800, 600)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        self.figure_received = Figure(figsize=(10, 3))
        self.canvas_received = FigureCanvas(self.figure_received)
        vbox.pack_start(self.canvas_received, True, True, 0)

        self.figure_demodulated = Figure(figsize=(10, 3))
        self.canvas_demodulated = FigureCanvas(self.figure_demodulated)
        vbox.pack_start(self.canvas_demodulated, True, True, 0)

        self.log_display = Gtk.TextView()
        self.log_display.set_editable(False)
        self.log_display.set_wrap_mode(Gtk.WrapMode.WORD)
        vbox.pack_start(self.log_display, True, True, 0)

        receive_button = Gtk.Button(label="Start Reception")
        receive_button.connect("clicked", self.on_receive)
        vbox.pack_start(receive_button, False, False, 0)

        self.server_thread = None
        self.running = False

    def on_receive(self, widget):
        if not self.running:
            self.running = True
            self.server_thread = threading.Thread(target=self.start_server, daemon=True)
            self.server_thread.start()

    def start_server(self):
        print(f"Receiver listening on {HOST}:{PORT}")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((HOST, PORT))
                s.listen(1)
                while self.running:
                    conn, addr = s.accept()
                    with conn:
                        buffer = ""
                        while True:
                            chunk = conn.recv(1024).decode()
                            if not chunk:
                                break
                            buffer += chunk
                            if "\n" in buffer:
                                message, buffer = buffer.split("\n", 1)
                                GLib.idle_add(self.process_data, message)
        except Exception as e:
            print(f"Server error: {e}")

    def process_data(self, data):
        try:
            payload = json.loads(data)
            framing = payload.get("framing")
            error_detection = payload.get("error_detection")
            modulation = payload.get("modulation")
            signal = payload.get("signal")

            if not all([framing, error_detection, modulation, signal]):
                raise ValueError("Incomplete data in received JSON.")

            self.plot_signal(self.figure_received, signal, "Received Signal")

            demodulated = self.demodulate(signal, modulation)
            self.plot_signal(self.figure_demodulated, demodulated, "Demodulated Signal")

            decoded_bits, error_status = self.handle_error_detection(''.join(map(str, demodulated)), error_detection)

            decoded_text = self.deframe(decoded_bits, framing)

            self.update_logs(decoded_text, error_status)
        except json.JSONDecodeError:
            self.show_error("Error processing data: Invalid JSON.")
        except Exception as e:
            self.show_error(f"Error processing data: {e}")

    def handle_error_detection(self, bits, error_detection):
        if error_detection == "Hamming":
            decoded_bits = hamming_decode(bits)
            error_position = 0
            if isinstance(decoded_bits, tuple) and len(decoded_bits) == 2:
                decoded_bits, error_position = decoded_bits
            if error_position > 0:
                error_status = f"Error corrected at position: {error_position}"
            else:
                error_status = "No errors detected"
        elif error_detection == "CRC32":
            if not verify_crc32(bits):
                error_status = "CRC32 error detected!"
            else:
                error_status = "No errors detected"
            decoded_bits = bits
        elif error_detection == "Parity Bit":
            if not check_parity_bit(bits):
                error_status = "Parity Bit error detected!"
            else:
                error_status = "No errors detected"
            decoded_bits = bits
        else:
            raise ValueError("Unknown error detection type")
        return decoded_bits, error_status

    def demodulate(self, signal, modulation):
        if modulation == "NRZ":
            return nrz_polar_demodulate(signal)
        elif modulation == "Manchester":
            return manchester_demodulate(signal)
        elif modulation == "Bipolar":
            return bipolar_demodulate(signal)
        elif modulation == "ASK":
            return ask_demodulate(signal)
        elif modulation == "FSK":
            return fsk_demodulate(signal)
        elif modulation == "8-QAM":
            return qam_demodulate(signal)
        else:
            raise ValueError("Unknown modulation.")

    def deframe(self, corrected_bits, framing):
        if framing == "Count Character":
            return deframe_count_character_to_text(corrected_bits)
        elif framing == "Byte Insertion":
            return deframe_byte_insertion_to_text(corrected_bits)
        else:
            raise ValueError("Unknown framing type.")

    def plot_signal(self, figure, signal, title):
        figure.clear()
        ax = figure.add_subplot(111)
        ax.plot(signal, label=title, color="green" if "Received" in title else "orange")
        ax.set_title(title)
        ax.set_xlabel("Samples")
        ax.set_ylabel("Amplitude")
        ax.grid(True)
        ax.legend()
        if "Received" in title:
            self.canvas_received.draw()
        else:
            self.canvas_demodulated.draw()

    def update_logs(self, decoded_text, error_status):
        buffer = self.log_display.get_buffer()
        buffer.set_text(
            f"Decoded Text: {decoded_text}\n"
            f"Error Status: {error_status}"
        )

    def show_error(self, message):
        dialog = Gtk.MessageDialog(
            parent=self, flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CLOSE, text=message
        )
        dialog.run()
        dialog.destroy()

    def close_application(self, *args):
        self.running = False
        Gtk.main_quit()

if __name__ == "__main__":
    win = Receiver()
    win.connect("destroy", win.close_application)
    win.show_all()
    Gtk.main()
