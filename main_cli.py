import argparse
import os
from huffman_binary import compress_file, decompress_file

def calculate_compression_rate(original_path, compressed_path):
    try:
        original_size = os.path.getsize(original_path)
        compressed_size = os.path.getsize(compressed_path)
        rate = (1 - compressed_size / original_size) * 100
        return round(rate, 2)
    except Exception as e:
        return None

def main():
    parser = argparse.ArgumentParser(description="HuffPyZip - Compression et Décompression Huffman")
    parser.add_argument("--action", choices=["compress", "decompress"], required=True, help="Action à effectuer")
    parser.add_argument("--input", required=True, help="Chemin du fichier source")
    parser.add_argument("--output", required=True, help="Chemin du fichier de sortie")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"❌ Erreur : Le fichier '{args.input}' est introuvable.")
        return

    try:
        if args.action == "compress":
            print(f"📦 Compression de : {args.input}")
            compress_file(args.input, args.output)
            rate = calculate_compression_rate(args.input, args.output)
            if rate is not None:
                print(f"✅ Compression terminée : {args.output}")
                print(f"📉 Taux de compression : {rate}%")
            else:
                print(f"✅ Compression terminée, mais taux non calculable.")
        
        elif args.action == "decompress":
            print(f"📤 Décompression de : {args.input}")
            decompress_file(args.input, args.output)
            print(f"✅ Décompression terminée : {args.output}")
    
    except Exception as e:
        print(f"⚠️ Erreur pendant le traitement : {e}")

if __name__ == "__main__":
    main()
