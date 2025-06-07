import heapq
from collections import Counter

# Cette classe représente un nœud de l'arbre de Huffman
class Node:
    def __init__(self, char=None, freq=0):
            self.char = char  # Le caractère (ex: 'a', 'b', etc.)
                    self.freq = freq  # Sa fréquence dans le texte
                            self.left = None  # Fils gauche
                                    self.right = None  # Fils droit

                                        # Cette méthode permet de comparer deux nœuds par leur fréquence
                                            def __lt__(self, other):
                                                    return self.freq < other.freq

                                                    # Cette fonction compte combien de fois chaque caractère apparaît dans le texte
                                                    def compter_frequences(texte):
                                                        return Counter(texte)

                                                        # Cette fonction construit l'arbre de Huffman à partir des fréquences
                                                        def construire_arbre(frequences):
                                                            # On crée une liste de nœuds (feuilles)
                                                                heap = [Node(char, freq) for char, freq in frequences.items()]
                                                                    heapq.heapify(heap)  # On transforme la liste en une file de priorité

                                                                        # On combine les deux nœuds les moins fréquents jusqu'à obtenir un seul arbre
                                                                            while len(heap) > 1:
                                                                                    gauche = heapq.heappop(heap)  # Nœud le moins fréquent
                                                                                            droite = heapq.heappop(heap)  # Deuxième moins fréquent
                                                                                                    fusion = Node(freq=gauche.freq + droite.freq)  # Nouveau nœud sans caractère
                                                                                                            fusion.left = gauche
                                                                                                                    fusion.right = droite
                                                                                                                            heapq.heappush(heap, fusion)

                                                                                                                                return heap[0]  # L'arbre complet (racine)

                                                                                                                                # Cette fonction parcourt l'arbre pour générer les codes binaires de chaque caractère
                                                                                                                                def generer_codes(arbre):
                                                                                                                                    codes = {}

                                                                                                                                        def parcourir(node, code=''):
                                                                                                                                                if node.char is not None:
                                                                                                                                                            # Si on est sur une feuille, on enregistre le code
                                                                                                                                                                        codes[node.char] = code
                                                                                                                                                                                else:
                                                                                                                                                                                            # Sinon, on continue à gauche (ajoute '0') et à droite (ajoute '1')
                                                                                                                                                                                                        parcourir(node.left, code + '0')
                                                                                                                                                                                                                    parcourir(node.right, code + '1')

                                                                                                                                                                                                                        parcourir(arbre)
                                                                                                                                                                                                                            return codes

                                                                                                                                                                                                                            # Cette fonction transforme le texte original en une chaîne de 0 et 1 grâce aux codes
                                                                                                                                                                                                                            def encoder_texte(texte, codes):
                                                                                                                                                                                                                                return ''.join(codes[char] for char in texte)

                                                                                                                                                                                                                                # Fonction principale de compression : prend un texte et retourne le texte codé + les codes
                                                                                                                                                                                                                                def compresser(texte):
                                                                                                                                                                                                                                    frequences = compter_frequences(texte)
                                                                                                                                                                                                                                        arbre = construire_arbre(frequences)
                                                                                                                                                                                                                                            codes = generer_codes(arbre)
                                                                                                                                                                                                                                                texte_code = encoder_texte(texte, codes)
                                                                                                                                                                                                                                                    return texte_code, codes