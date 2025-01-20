import numpy as np

def ask(bits, freq=1, amp1=1, amp0=0, bit_signal=100):
    """Amplitude Shift Keying (ASK) modulation."""

    # time vector for one bit duration
    time = np.linspace(0, 1, bit_signal)
    signal = []
    # generate the corresponding modulated waveform for the each bit
    for bit in bits:
        if bit == 1:
            amp = amp1
        else:
            amp = amp0
        # Create the carrier wave for the current bit and add to the signal
        signal.extend(amp * np.sin(2 * np.pi * freq * time))
    return signal

def fsk(bits, freq0=1, freq1=2, bit_signal=100):
    """Frequency Shift Keying (FSK) modulation."""

    # time vector for one bit duration
    time = np.linspace(0, 1, bit_signal)
    signal = []
    # generate the corresponding modulated waveform for the each bit
    for bit in bits:
        # Select the frequency based on the current bit (freq1 for 1, freq0 for 0)
        if bit == 1:
            freq = freq1
        else:
            freq = freq0
        # Create the carrier wave for the current bit and add to the signal
        signal.extend(np.sin(2 * np.pi * freq * time))
    return signal

def qam(bits, bit_signal=100):
    """8-QAM modulation."""
    if len(bits) % 3 != 0:
        raise ValueError("Bits length must be a multiple of 3 for 8-QAM.")
    time = np.linspace(0, 1, bit_signal)
    signal = []
    # generate the corresponding modulated waveform for the each group of 3 bits
    for i in range(0, len(bits), 3):
        # Map 3 bits to an amplitude and phase
        bit3 = bits[i:i + 3]
        # Calculate the amplitude and phase based on the 3 bits
        amp = 1 + bit3[0]
        # The phase is calculated based on the 2nd and 3rd bits
        phase = (bit3[1] * 2 + bit3[2]) * (np.pi / 4)
        carrier = amp * np.sin(2 * np.pi * time + phase)
        signal.extend(carrier)
    return signal
