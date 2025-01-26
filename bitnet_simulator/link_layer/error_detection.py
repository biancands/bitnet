# Error detection using parity bit
def parity_bit(data):
    count = data.count('1')
    p_bit = '0' if count % 2 == 0 else '1'
    return data + p_bit

# Check if the parity bit is correct
def check_parity_bit(data):
    p = data[:-1]
    p_bit = data[-1]
    count = p.count('1')
    expected_parity = '0' if count % 2 == 0 else '1'
    return p_bit == expected_parity

# Convert data to frames with parity bit
def parity_to_frames(data):
    return [parity_bit(frame) for frame in data]

# Check parity bit on frames
def parity_on_frames(data):
    return [check_parity_bit(frame) for frame in data]

#frames = ["01010101", "11001100", "11100011"]
#frames_with_parity = parity_to_frames(frames)
#print("Frames with Parity:", frames_with_parity)
#parity_check = parity_on_frames(frames_with_parity)
#print("Parity Check:", parity_check)
#frames_with_parity[1] = "110011100"
#parity_check_with_error = parity_on_frames(frames_with_parity)
#print("Parity Check with Error:", parity_check_with_error)
