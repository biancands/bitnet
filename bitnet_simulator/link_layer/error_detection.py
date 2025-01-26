import zlib

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

# Error detection using Circular Redundancy Check (CRC-32)
def crc32(data):
    # Convert the binary data string to bytes
    bdata = int(data, 2).to_bytes((len(data) + 7) // 8, byteorder='big')   
    # Calculate the CRC-32
    crc = zlib.crc32(bdata)    
    # Convert the CRC to a binary string
    crc_binary = f"{crc:032b}"    
    return data + crc_binary

# Verify CRC-32
def verify_crc32(datacrc):
    # Split the data and the CRC
    data = datacrc[:-32]
    crc = datacrc[-32:]  
    # Convert the binary data string to bytes
    bdata = int(data, 2).to_bytes((len(data) + 7) // 8, byteorder='big') 
    # Calculate the CRC-32 checksum
    crc_calc = zlib.crc32(bdata)
    crc_calcb = f"{crc_calc:032b}" 
    return crc == crc_calcb

#data = "1101011111"
#framed_data = crc32(data)
#print("Dados com CRC:", framed_data)
#is_valid = verify_crc32(framed_data)
#print("CRC válido:", is_valid)
#corrupted_data = framed_data[:5] + ('1' if framed_data[5] == '0' else '0') + framed_data[6:]
#print("Dados corrompidos:", corrupted_data)
#is_valid_corrupted = verify_crc32(corrupted_data)
#print("CRC válido para dados corrompidos:", is_valid_corrupted)
#frames = ["01010101", "11001100", "11100011"]
#frames_with_parity = parity_to_frames(frames)
#print("Frames with Parity:", frames_with_parity)
#parity_check = parity_on_frames(frames_with_parity)
#print("Parity Check:", parity_check)
#frames_with_parity[1] = "110011100"
#parity_check_with_error = parity_on_frames(frames_with_parity)
#print("Parity Check with Error:", parity_check_with_error)
