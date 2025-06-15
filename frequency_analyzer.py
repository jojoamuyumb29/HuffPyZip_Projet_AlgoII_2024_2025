import collections

class Node:
    def __init__(self, byte, frequency):
        self.byte = byte
        self.frequency = frequency
        self.left = None
        self.right = None

    def __repr__(self):
        return f"Node(byte={self.byte}, freq={self.frequency})"


class PriorityQueue:
    def __init__(self):
        self.nodes = []

    def push(self, node):
        self.nodes.append(node)
        self.nodes.sort(key=lambda n: n.frequency)

    def pop(self):
        return self.nodes.pop(0)

    def __len__(self):
        return len(self.nodes)

def calculate_frequencies(file_path):
    frequencies = collections.Counter()
    with open(file_path, 'rb') as file:
        byte = file.read(1)
        while byte:
            frequencies[byte[0]] += 1  # byte to int
            byte = file.read(1)
    return frequencies
