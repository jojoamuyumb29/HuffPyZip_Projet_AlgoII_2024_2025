import heapq
import json
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
    padding = (8 - len(encoded_data) % 8) % 8
    encoded_data += '0' * padding

    padding_info = "{0:08b}".format(padding)

    # Convert bitstring to bytes
    b = bytearray()
    for i in range(0, len(encoded_data), 8):
        byte = encoded_data[i:i+8]
        b.append(int(byte, 2))

    # Sauvegarder le codebook (en tant que JSON)
    json_codebook = json.dumps({str(byte): code for byte, code in codebook.items()})
    json_codebook_bytes = json_codebook.encode('utf-8')
    codebook_length = len(json_codebook_bytes)

    with open(output_path, 'wb') as out:
        out.write(codebook_length.to_bytes(4, byteorder='big'))  # 4 octets pour taille du codebook
        out.write(json_codebook_bytes)  # codebook
        out.write(bytes([padding]))    # 1 octet pour padding
        out.write(bytes(b))            # données compressées

def decompress_file(input_path, output_path):
    with open(input_path, 'rb') as f:
        codebook_length_bytes = f.read(4)
        codebook_length = int.from_bytes(codebook_length_bytes, byteorder='big')

        codebook_bytes = f.read(codebook_length)
        codebook = json.loads(codebook_bytes.decode('utf-8'))
        codebook = {v: int(k) for k, v in codebook.items()}  # inverser : {code: byte}

        padding = ord(f.read(1))  # lire le padding (1 octet)

        data = f.read()

    bit_string = ''.join(f"{byte:08b}" for byte in data)
    bit_string = bit_string[:-padding] if padding > 0 else bit_string

    current_code = ""
    decoded_bytes = bytearray()

    for bit in bit_string:
        current_code += bit
        if current_code in codebook:
            decoded_bytes.append(codebook[current_code])
            current_code = ""

    with open(output_path, 'wb') as out:
        out.write(decoded_bytes)
