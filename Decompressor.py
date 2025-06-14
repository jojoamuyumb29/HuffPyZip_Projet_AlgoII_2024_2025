from huffman_tree import build_huffman_tree

def decompress(input_path, output_path):
    with open(input_path, 'rb') as f:
        length = int.from_bytes(f.read(2), 'big')
        freq_table = {}
        for _ in range(length):
            byte = ord(f.read(1))
            freq = int.from_bytes(f.read(4), 'big')
            freq_table[byte] = freq

        tree = build_huffman_tree(freq_table)

        padding = ord(f.read(1))
        bit_string = ""
        byte = f.read(1)
        while byte:
            bits = bin(ord(byte))[2:].rjust(8, '0')
            bit_string += bits
            byte = f.read(1)

        bit_string = bit_string[:-padding] if padding > 0 else bit_string

        result = bytearray()
        node = tree
        for bit in bit_string:
            node = node.left if bit == '0' else node.right
            if node.byte is not None:
                result.append(node.byte)
                node = tree

        with open(output_path, 'wb') as out:
            out.write(result)
