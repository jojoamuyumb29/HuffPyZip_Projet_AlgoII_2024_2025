class Node:
    def __init__(self, byte, freq):
        self.byte = byte
        self.freq = freq
        self.left = None
        self.right = None

def decompress_file(input_path, output_path):
    with open(input_path, 'rb') as f:
        padding_info = f.read(8)
        padding = int(padding_info.decode('utf-8'))
        data = f.read()

    bit_string = ''.join(f"{byte:08b}" for byte in data)
    bit_string = bit_string[:-padding]

    # TODO: reconstruct Huffman tree and decode bit_string
    with open(output_path, 'wb') as out:
        out.write(b"Decompression stub")
