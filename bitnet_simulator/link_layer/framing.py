FLAG = "01111110"  # Flag byte in binary (~)
ESC = "11111101"   # Escape byte in binary (\)

# transform text to binary
def text_to_bits(text):
    return ''.join(f"{ord(char):08b}" for char in text)

#transform binary to text
def bits_to_text(binary_data):
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

#count character framing
def count_character(data):
    frames = ""
    for frame in data:
        binary_data = text_to_bits(frame)
        byte_count = len(binary_data) // 8
        header = f"{byte_count:08b}"
        frames += header + binary_data
    return frames

#deframe character framing
def deframe_count_character(data):
    original_frames = []
    i = 0
    while i < len(data):
        byte_count = int(data[i:i+8], 2)
        i += 8 # move the index to the start
        binary_data = data[i:i + (byte_count * 8)] # get the binary data
        i += byte_count * 8 # move the index to the next frame
        original_frames.append(bits_to_text(binary_data))
    return original_frames

#count character framing from text
def count_character_framing_from_text(text):
    words = text.split() # split the text into words for framing
    return count_character(words)

#deframe character framing to text
def deframe_count_character_to_text(data):
    frames = deframe_count_character(data)
    return ' '.join(frames)

#byte insertion framing
def byte_insertion(data):
    frames = ""
    for frame in data:
        binary_data = text_to_bits(frame)
        # Escape FLAG and ESC
        esc_data = binary_data.replace(FLAG, ESC + FLAG).replace(ESC, ESC + ESC)
        frames += FLAG + esc_data + FLAG
    return frames

#deframe byte insertion
def deframe_byte_insertion(data):
    frames = []
    i = 0
    while i < len(data):
        # Find the next FLAG
        start = data.find(FLAG, i)
        end = data.find(FLAG, start + len(FLAG))
        if start == -1 or end == -1:
            break
        # Extract the data between the flags
        raw_data = data[start + len(FLAG):end]
        # Remove the escapes
        unescaped_data = raw_data.replace(ESC + ESC, ESC).replace(ESC + FLAG, FLAG)
        frames.append(bits_to_text(unescaped_data))
        i = end + len(FLAG)
    return frames

def byte_insertion_framing_from_text(text):
    words = text.split()
    return byte_insertion(words)


def deframe_byte_insertion_to_text(data):
    frames = deframe_byte_insertion(data)
    return ' '.join(frames)

text = "Hello my friend"
framed = count_character_framing_from_text(text)
framed2 = byte_insertion_framing_from_text(text)
print("Framed Binary CC:", framed)
print("Framed Binary BI:", framed2)

original_text = deframe_count_character_to_text(framed)
original_text2 = deframe_byte_insertion_to_text(framed2)
print("Original Text CC:", original_text)
print("Original Text BI:", original_text2)