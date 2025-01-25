import numpy as np
from scipy.fft import fft

#Amplitude Shift Keying (ASK) modulation
def ask(bits, freq=1, amp1=1, amp0=0, bit_signal=100):
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

#Frequency Shift Keying (FSK) modulation
def fsk(bits, freq0=1, freq1=2, bit_signal=100):
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

#8-Quadrature Amplitude Modulation (8-QAM) modulation
def qam(bits, bit_signal=100):
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

# Demodulation a signal using ASK
def ask_demodulate(signal, threshold=0.5, bit_signal=100):
    bits = []
    for i in range(0, len(signal), bit_signal):
        c = signal[i:i + bit_signal]
        avg_amp = np.mean(np.abs(c))
        bits.append(1 if avg_amp > threshold else 0)
    return bits

# Demodulation a signal using FSK
def fsk_demodulate(signal, freq0=1, freq1=2, bit_signal=100, sampling_rate=100):
    bits = []
    for i in range(0, len(signal), bit_signal):
        c = signal[i:i + bit_signal]
        fft_result = fft(c)
        freqs = np.fft.fftfreq(len(fft_result), d=1 / sampling_rate)
        dom_freq = freqs[np.argmax(np.abs(fft_result))]
        bits.append(1 if abs(dom_freq - freq1) < abs(dom_freq - freq0) else 0)
    return bits

# Demodulation a signal using 8-QAM
def qam_demodulate(signal, bit_signal=100):
    bits = []
    for i in range(0, len(signal), bit_signal):
        c = signal[i:i + bit_signal]
        amp = np.max(np.abs(c))
        phase = np.angle(np.mean(c))
        if amp > 1.5:
            bits.append(1)
        else:
            bits.append(0)
        if phase > 0:
            bits.append(1)
        else:
            bits.append(0)
    return bits
