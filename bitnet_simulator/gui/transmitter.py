import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from bitnet_simulator.physical_layer.carrier import ask, fsk, qam
import matplotlib.pyplot as plt

class Transmitter(Gtk.Window):
    def __init__(self):
        super().__init__(title="Transmitter - BitNet")
        self.set_border_width(10)
        self.set_default_size(400, 200)

        # principal layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        # bits input
        self.bits_entry = Gtk.Entry()
        self.bits_entry.set_placeholder_text("Enter bits (e.g., 101010)")
        vbox.pack_start(self.bits_entry, False, False, 0)

        # modulation type
        self.modulation_combo = Gtk.ComboBoxText()
        self.modulation_combo.append_text("ASK")
        self.modulation_combo.append_text("FSK")
        self.modulation_combo.append_text("8-QAM")
        self.modulation_combo.set_active(0)
        vbox.pack_start(self.modulation_combo, False, False, 0)

        # generate signal button
        generate_button = Gtk.Button(label="Generate Signal")
        generate_button.connect("clicked", self.on_generate_signal)
        vbox.pack_start(generate_button, False, False, 0)

    def on_generate_signal(self, widget):
        # selected bits and modulation type
        bits = self.bits_entry.get_text()
        modulation = self.modulation_combo.get_active_text()

        try:
            # convert bits to a list of integers
            bits_list = [int(b) for b in bits]
            if modulation == "ASK":
                signal = ask(bits_list)
            elif modulation == "FSK":
                signal = fsk(bits_list)
            elif modulation == "8-QAM":
                signal = qam(bits_list)
            else:
                raise ValueError("Invalid modulation type.")

            # plot the generated signal
            self.plot_signal(signal)

        except Exception as e:
            self.show_error(str(e))

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
