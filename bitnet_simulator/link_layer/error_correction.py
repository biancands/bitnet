# Calculate parity bit positions
def calc_pos(l):
    parbits = 0
    while (2 ** parbits) < (l + parbits + 1):
        parbits += 1
    return [2 ** i for i in range(parbits)]

def calc_value(encoded, pos):
    return sum(
        encoded[j - 1] for j in range(1, len(encoded) + 1) if j & pos
    ) % 2

# Error correction using Hamming code
def hamming_encode(data):
    n = len(data)
    parpos = calc_pos(n)
    encodedl = n + len(parpos)
    encoded = [0] * encodedl

    # Copy the data bits to the encoded message
    data_index = 0
    for i in range(1, encodedl + 1):
        if i not in parpos:
            encoded[i - 1] = int(data[data_index])
            data_index += 1

    # Calculate the parity bits
    for pos in parpos:
        encoded[pos - 1] = calc_value(encoded, pos)

    return ''.join(map(str, encoded))

# Error correction using Hamming decode
def hamming_decode(encoded):
    encoded = [int(bit) for bit in encoded]
    parpos = calc_pos(len(encoded) - len(calc_pos(len(encoded))))

    # Detect the error position
    error_position = sum(
        pos for pos in parpos
        if calc_value(encoded, pos) != 0
    )

    # Correct the error
    if error_position > 0:
        print(f"Error detected at position: {error_position}")
        if encoded[error_position - 1] == 0:
            encoded[error_position - 1] = 1
        else:
            encoded[error_position - 1] = 0
    else:
        print("No error detected")

    # Remove the parity bits
    decoded = [
        encoded[i - 1] for i in range(1, len(encoded) + 1) if i not in parpos
    ]

    return ''.join(map(str, decoded))


#data = "10111"
#encoded_message = hamming_encode(data)
#print("Mensagem codificada:", encoded_message)
#encoded_message_with_error = encoded_message[:3] + ('1' if encoded_message[3] == '0' else '0') + encoded_message[4:]
#print("Mensagem com erro:", encoded_message_with_error)
#decoded_message = hamming_decode(encoded_message_with_error)
#print("Mensagem decodificada:", decoded_message)
