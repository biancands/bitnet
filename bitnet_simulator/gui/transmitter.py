import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from bitnet_simulator.physical_layer.carrier import ask, fsk, qam
from bitnet_simulator.physical_layer.baseband import nrz_polar, manchester, bipolar
import matplotlib.pyplot as plt

class Transmitter(Gtk.Window):
    def __init__(self):
        super().__init__(title="Transmitter - BitNet")
        self.set_border_width(10)
        self.set_default_size(400, 400)

        # layout principal
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        # bits input
        self.bits_entry = Gtk.Entry()
        self.bits_entry.set_placeholder_text("Enter bits (e.g., 101010)")
        vbox.pack_start(self.bits_entry, False, False, 0)

        # modulation type selection
        self.modulation_combo = Gtk.ComboBoxText()
        self.modulation_combo.append_text("ASK")
        self.modulation_combo.append_text("FSK")
        self.modulation_combo.append_text("8-QAM")
        self.modulation_combo.append_text("NRZ-Polar")
        self.modulation_combo.append_text("Manchester")
        self.modulation_combo.append_text("Bipolar")
        self.modulation_combo.set_active(0)
        vbox.pack_start(self.modulation_combo, False, False, 0)

        # generate signal button
        generate_button = Gtk.Button(label="Generate Signal")
        generate_button.connect("clicked", self.on_generate_signal)
        vbox.pack_start(generate_button, False, False, 0)

        self.signal_display = Gtk.TextView()
        self.signal_display.set_editable(False)
        self.signal_display.set_wrap_mode(Gtk.WrapMode.WORD)
        vbox.pack_start(self.signal_display, True, True, 0)

        copy_button = Gtk.Button(label="Copy Signal")
        copy_button.connect("clicked", self.on_copy_signal)
        vbox.pack_start(copy_button, False, False, 0)

        self.generated_signal = []

    def on_generate_signal(self, widget):
        bits = self.bits_entry.get_text()
        modulation = self.modulation_combo.get_active_text()

        try:
            bits_list = [int(b) for b in bits]

            if modulation == "ASK":
                signal = ask(bits_list)
            elif modulation == "FSK":
                signal = fsk(bits_list)
            elif modulation == "8-QAM":
                signal = qam(bits_list)
            elif modulation == "NRZ-Polar":
                signal = nrz_polar(bits_list)
            elif modulation == "Manchester":
                signal = manchester(bits_list)
            elif modulation == "Bipolar":
                signal = bipolar(bits_list)
            else:
                raise ValueError("Invalid modulation type.")

            self.generated_signal = signal
            self.update_signal_display(signal)
            self.plot_signal(signal)

        except Exception as e:
            self.show_error(str(e))

    def update_signal_display(self, signal):
        buffer = self.signal_display.get_buffer()
        signal_text = ", ".join(f"{x:.2f}" for x in signal)
        buffer.set_text(f"[{signal_text}]")

    def on_copy_signal(self, widget):
        if not self.generated_signal:
            self.show_error("No signal generated to copy!")
            return

        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        signal_text = ", ".join(f"{x:.2f}" for x in self.generated_signal)
        clipboard.set_text(f"[{signal_text}]", -1)
        print("Signal copied to clipboard!")

    def plot_signal(self, signal):
        plt.figure(figsize=(10, 4))
        plt.plot(signal)
        plt.title("Generated Signal")
        plt.xlabel("Time")
        plt.ylabel("Amplitude")
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
    win = Transmitter()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
