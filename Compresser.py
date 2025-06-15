import collections
from huffman_tree import build_huffman_tree, generate_codes

def compress(input_path, output_path):
    with open(input_path, 'rb') as f:
        data = f.read()

    freq_table = collections.Counter(data)
    tree = build_huffman_tree(freq_table)
    codes = generate_codes(tree)

    with open(output_path, 'wb') as f:
        f.write(len(freq_table).to_bytes(2, 'big'))
        for byte, freq in freq_table.items():
            f.write(bytes([byte]))
            f.write(freq.to_bytes(4, 'big'))

        bit_string = ''.join(codes[byte] for byte in data)

        padding = (8 - len(bit_string) % 8) % 8
        bit_string += '0' * padding
        f.write(bytes([padding]))

        b = bytearray()
        for i in range(0, len(bit_string), 8):
            byte = int(bit_string[i:i+8], 2)
            b.append(byte)
        f.write(bytes(b))
