import heapq
import os
import pickle
from collections import defaultdict

class HuffmanNode:
    def __init__(self, freq, byte=None, left=None, right=None):
        self.freq = freq
        self.byte = byte
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_table(data):
    freq = defaultdict(int)
    for byte in data:
        freq[byte] += 1
    return freq

def build_huffman_tree(freq_table):
    heap = [HuffmanNode(freq, byte) for byte, freq in freq_table.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(node1.freq + node2.freq, None, node1, node2)
        heapq.heappush(heap, merged)

    return heap[0] if heap else None

def build_codebook(root):
    codebook = {}

    def traverse(node, path=""):
        if node.byte is not None:
            codebook[node.byte] = path
            return
        traverse(node.left, path + "0")
        traverse(node.right, path + "1")

    if root:
        traverse(root)
    return codebook

def compress_file(input_path, output_path):
    with open(input_path, 'rb') as f:
        data = f.read()

    freq_table = build_frequency_table(data)
    tree = build_huffman_tree(freq_table)
    codebook = build_codebook(tree)

    encoded_data = ''.join(codebook[byte] for byte in data)

    # Padding
    padding = (8 - len(encoded_data) % 8) % 8
    encoded_data += '0' * padding

    # Convert bits to bytes
    compressed_bytes = bytearray()
    for i in range(0, len(encoded_data), 8):
        byte = encoded_data[i:i+8]
        compressed_bytes.append(int(byte, 2))

    with open(output_path, 'wb') as out:
        # Sérialiser la table de fréquence
        freq_serialized = pickle.dumps(freq_table)
        out.write(len(freq_serialized).to_bytes(4, 'big'))  # longueur en premier
        out.write(freq_serialized)

        # Écrire le padding
        out.write(bytes([padding]))

        # Écrire les données compressées
        out.write(compressed_bytes)

    print("Compression terminée avec succès.")
