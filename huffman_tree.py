import heapq

class HuffmanNode:
    def __init__(self, freq, byte=None, left=None, right=None):
        self.freq = freq
        self.byte = byte
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(freq_table):
    heap = [HuffmanNode(freq, byte) for byte, freq in freq_table.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(node1.freq + node2.freq, None, node1, node2)
        heapq.heappush(heap, merged)
    return heap[0] if heap else None

def generate_codes(root):
    codebook = {}
    def traverse(node, path=""):
        if node is None:
            return
        if node.byte is not None:
            codebook[node.byte] = path
        else:
            traverse(node.left, path + "0")
            traverse(node.right, path + "1")
    traverse(root)
    return codebook
