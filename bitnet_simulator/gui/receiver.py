import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from bitnet_simulator.physical_layer.carrier import ask_demodulate, fsk_demodulate, qam_demodulate
import matplotlib.pyplot as plt

class Receiver(Gtk.Window):
    def __init__(self):
        super().__init__(title="Receiver - BitNet")
        self.set_border_width(10)
        self.set_default_size(400, 300)

        # principal layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        # bits input
        self.signal_entry = Gtk.Entry()
        self.signal_entry.set_placeholder_text("Enter modulated signal as list (e.g., [0.5, 1.0, -0.5])")
        vbox.pack_start(self.signal_entry, False, False, 0)

        # demodulation type selection
        self.modulation_combo = Gtk.ComboBoxText()
        self.modulation_combo.append_text("ASK")
        self.modulation_combo.append_text("FSK")
        self.modulation_combo.append_text("8-QAM")
        self.modulation_combo.set_active(0)
        vbox.pack_start(self.modulation_combo, False, False, 0)

        # demodulate signal button
        demodulate_button = Gtk.Button(label="Demodulate Signal")
        demodulate_button.connect("clicked", self.on_demodulate_signal)
        vbox.pack_start(demodulate_button, False, False, 0)

        # result label
        self.result_label = Gtk.Label(label="Demodulated bits will appear here.")
        vbox.pack_start(self.result_label, False, False, 0)

    def on_demodulate_signal(self, widget):
        signal_text = self.signal_entry.get_text()
        modulation = self.modulation_combo.get_active_text()

        try:
            signal = [float(x) for x in signal_text.strip("[]").split(",")]

            if modulation == "ASK":
                bits = ask_demodulate(signal, threshold=0.5, samples_per_bit=100)
            elif modulation == "FSK":
                bits = fsk_demodulate(signal, freq0=1, freq1=2, samples_per_bit=100, sampling_rate=100)
            elif modulation == "8-QAM":
                bits = qam_demodulate(signal, samples_per_bit=100)
            else:
                raise ValueError("Invalid modulation type.")

            self.result_label.set_text(f"Demodulated Bits: {bits}")

            self.plot_bits(bits)

        except Exception as e:
            self.show_error(str(e))

    def plot_bits(self, bits):
        samples_per_bit = 100
        signal = []
        for bit in bits:
            signal.extend([bit] * samples_per_bit)

        plt.figure(figsize=(10, 4))
        plt.step(range(len(signal)), signal, where='post')
        plt.title("Demodulated Signal")
        plt.xlabel("Time")
        plt.ylabel("Amplitude (0 or 1)")
        plt.ylim(-0.5, 1.5)
        plt.grid()
        plt.show()

    def show_error(self, message):
        dialog = Gtk.MessageDialog(
            self,
            0,
            Gtk.MessageType.ERROR,
            Gtk.ButtonsType.CLOSE,
            message,
        )
        dialog.run()
        dialog.destroy()

if __name__ == "__main__":
    win = Receiver()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
