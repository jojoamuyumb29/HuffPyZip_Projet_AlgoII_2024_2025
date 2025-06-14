import pickle

class HuffmanNode:
    def __init__(self, freq, byte=None, left=None, right=None):
        self.freq = freq
        self.byte = byte
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(freq_table):
    import heapq
    heap = [HuffmanNode(freq, byte) for byte, freq in freq_table.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(node1.freq + node2.freq, None, node1, node2)
        heapq.heappush(heap, merged)

    return heap[0] if heap else None

def decompress_file(input_path, output_path):
    with open(input_path, 'rb') as f:
        # Lire longueur de la table
        freq_length = int.from_bytes(f.read(4), 'big')

        # Lire la table de fréquences
        freq_serialized = f.read(freq_length)
        freq_table = pickle.loads(freq_serialized)

        # Lire le padding
        padding = ord(f.read(1))

        # Lire les données compressées
        bit_string = ""
        byte = f.read(1)
        while byte:
            bits = bin(ord(byte))[2:].rjust(8, '0')
            bit_string += bits
            byte = f.read(1)

        # Supprimer le padding
        if padding > 0:
            bit_string = bit_string[:-padding]

    # Reconstruire l’arbre
    tree = build_huffman_tree(freq_table)

    # Décompression via parcours de l’arbre
    decoded_bytes = bytearray()
    current = tree
    for bit in bit_string:
        current = current.left if bit == '0' else current.right
        if current.byte is not None:
            decoded_bytes.append(current.byte)
            current = tree

    with open(output_path, 'wb') as out:
        out.write(decoded_bytes)

    print("Décompression réussie.")
