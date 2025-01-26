# transform text to binary
def text_to_bits(text):
    return ''.join(f"{ord(char):08b}" for char in text)

#transform binary to text
def bits_to_text(binary_data):
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

#count character framing
def count_character_framing(data):
    framed_data = ""
    for frame in data:
        binary_data = text_to_bits(frame)
        byte_count = len(binary_data) // 8
        header = f"{byte_count:08b}"
        framed_data += header + binary_data
    return framed_data

#deframe character framing
def deframe_count_character(framed_data):
    original_frames = []
    i = 0
    while i < len(framed_data):
        byte_count = int(framed_data[i:i+8], 2)
        i += 8 # move the index to the start
        binary_data = framed_data[i:i + (byte_count * 8)] # get the binary data
        i += byte_count * 8 # move the index to the next frame
        original_frames.append(bits_to_text(binary_data))
    return original_frames

#count character framing from text
def count_character_framing_from_text(text):
    words = text.split() # split the text into words for framing
    return count_character_framing(words)

#deframe character framing to text
def deframe_count_character_to_text(framed_data):
    frames = deframe_count_character(framed_data)
    return ' '.join(frames)

text = "Hello my friend"
framed = count_character_framing_from_text(text)
print("Framed Binary:", framed)

original_text = deframe_count_character_to_text(framed)
print("Original Text:", original_text)