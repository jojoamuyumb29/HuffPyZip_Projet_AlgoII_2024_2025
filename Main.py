import sys
from compressor import compress
from decompressor import decompress

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage : python main.py [compress|decompress] input_file output_file")
        exit(1)

    action = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    if action == "compress":
        compress(input_file, output_file)
        print("Compression terminée.")
    elif action == "decompress":
        decompress(input_file, output_file)
        print("Décompression terminée.")
    else:
        print("Action invalide. Choisissez 'compress' ou 'decompress'.")
