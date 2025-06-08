import heapq
from collections import defaultdict

class Node:
    def __init__(self, byte, freq):
        self.byte = byte
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_table(data):
    freq = defaultdict(int)
    for byte in data:
        freq[byte] += 1
    return freq

def build_huffman_tree(freq_table):
    heap = [Node(byte, freq) for byte, freq in freq_table.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = Node(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)

    return heap[0]

def build_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}
    if node is not None:
        if node.byte is not None:
            codebook[node.byte] = prefix
        build_codes(node.left, prefix + "0", codebook)
        build_codes(node.right, prefix + "1", codebook)
    return codebook

def compress_file(input_path, output_path):
    with open(input_path, 'rb') as f:
        data = f.read()

    freq_table = build_frequency_table(data)
    huffman_tree = build_huffman_tree(freq_table)
    codebook = build_codes(huffman_tree)

    encoded_data = ''.join(codebook[byte] for byte in data)
    padding = 8 - len(encoded_data) % 8
    encoded_data += '0' * padding
    padding_info = "{0:08b}".format(padding)

    b = bytearray()
    for i in range(0, len(encoded_data), 8):
        byte = encoded_data[i:i+8]
        b.append(int(byte, 2))

    with open(output_path, 'wb') as out:
        out.write(bytes(padding_info, 'utf-8'))
        out.write(bytes(b))

def decompress_file(input_path, output_path):
    with open(input_path, 'rb') as f:
        padding_info = f.read(8)
        padding = int(padding_info.decode('utf-8'))
        data = f.read()

    bit_string = ''.join(f"{byte:08b}" for byte in data)
    bit_string = bit_string[:-padding]

    # TODO: Save and load tree for full decompression
    with open(output_path, 'wb') as out:
        out.write(b"Decompression stub")  # stub for now
