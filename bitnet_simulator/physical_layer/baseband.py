import numpy as np

# Non-Return-to-Zero (NRZ) polar modulation
def nrz_polar(bits, h=1, l=-1, bit_signal=100):
    signal = []
    for bit in bits:
        value = h if bit == 1 else l
        signal.extend([value] * bit_signal)
    return signal

# Non-Return-to-Zero (NRZ) polar demodulation
def nrz_polar_demodulate(sig, threshold=0, bit_signal=100):
    bits = []
    for i in range(0, len(sig), bit_signal):
        avg = np.mean(sig[i:i + bit_signal])
        bits.append(1 if avg > threshold else 0)
    return bits

# Manchester modulation
def manchester(bits, h=1, l=-1, bit_signal=100):
    sig = []
    half_samples = bit_signal // 2
    for bit in bits:
        if bit == 1:
            sig.extend([h] * half_samples + [l] * half_samples)
        else:
            sig.extend([l] * half_samples + [h] * half_samples)
    return sig

# Manchester demodulation
def manchester_demodulate(sig, h=1, l=-1, bit_signal=100):
    bits = []
    half_samples = bit_signal // 2
    for i in range(0, len(sig), bit_signal):
        first_half = np.mean(sig[i:i + half_samples])
        second_half = np.mean(sig[i + half_samples:i + bit_signal])
        bits.append(1 if first_half == h and second_half == l else 0)
    return bits

# Bipolar modulation
def bipolar(bits, h=1, l=-1, zero=0, bit_signal=100):
    sig = []
    last_high = True
    for bit in bits:
        if bit == 1:
            value = h if last_high else l
            last_high = not last_high
        else:
            value = zero
        sig.extend([value] * bit_signal)
    return sig

# Bipolar demodulation
def bipolar_demodulate(signal, threshold=0, bit_signal=100):
    bits = []
    for i in range(0, len(signal), bit_signal):
        avg = np.mean(signal[i:i + bit_signal])
        bits.append(1 if abs(avg) > threshold else 0)
    return bits
