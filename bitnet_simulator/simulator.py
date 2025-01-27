import subprocess

def start_simulation():
    subprocess.Popen(["python3", "-m","bitnet_simulator.gui.receiver"])
    subprocess.Popen(["python3", "-m","bitnet_simulator.gui.transmitter"])

if __name__ == "__main__":
    start_simulation()