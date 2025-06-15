import collections
import os
import time
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import customtkinter as ctk
from frequency_analyzer import Node, PriorityQueue, calculate_frequencies


# -------------------- BACKEND FONCTIONS --------------------


def compress_file(file_path, output_path):
    freqs = calculate_frequencies(file_path)
    pq = PriorityQueue()
    for byte, freq in freqs.items():
        pq.push(Node(byte, freq))

    while len(pq) > 1:
        left = pq.pop()
        right = pq.pop()
        merged = Node(None, left.frequency + right.frequency)
        merged.left = left
        merged.right = right
        pq.push(merged)

    tree = pq.pop() if len(pq) > 0 else None
    codebook = {}

    def generate_codes(node, code=""):
        if node is None:
            return
        if node.byte is not None:
            codebook[node.byte] = code
        else:
            generate_codes(node.left, code + "0")
            generate_codes(node.right, code + "1")

    generate_codes(tree)

    with open(file_path, 'rb') as f:
        data = f.read()

    try:
        bit_string = ''.join(codebook[byte] for byte in data)
    except KeyError as e:
        raise ValueError(f"Octet {e} non présent dans le dictionnaire Huffman.")

    padding = (8 - len(bit_string) % 8) % 8
    bit_string += '0' * padding

    with open(output_path, 'wb') as f:
        f.write(len(freqs).to_bytes(2, 'big'))
        for byte, freq in freqs.items():
            f.write(bytes([byte]))  # int to byte
            f.write(freq.to_bytes(4, 'big'))
        f.write(bytes([padding]))
        b = bytearray()
        for i in range(0, len(bit_string), 8):
            b.append(int(bit_string[i:i+8], 2))
        f.write(bytes(b))

def decompress_file(file_path, output_path):
    with open(file_path, 'rb') as f:
        length = int.from_bytes(f.read(2), 'big')
        freq_table = {}
        for _ in range(length):
            byte = f.read(1)[0]  # byte to int
            freq = int.from_bytes(f.read(4), 'big')
            freq_table[byte] = freq

        pq = PriorityQueue()
        for byte, freq in freq_table.items():
            pq.push(Node(byte, freq))

        while len(pq) > 1:
            left = pq.pop()
            right = pq.pop()
            merged = Node(None, left.frequency + right.frequency)
            merged.left = left
            merged.right = right
            pq.push(merged)

        tree = pq.pop() if len(pq) > 0 else None
        padding_byte = f.read(1)
        if not padding_byte:
            raise ValueError("Erreur : padding non trouvé dans le fichier compressé.")
        padding = int.from_bytes(padding_byte, 'big')

        bit_string = ""
        byte = f.read(1)
        while byte:
            bits = bin(byte[0])[2:].rjust(8, '0')
            bit_string += bits
            byte = f.read(1)
        if padding > 0:
            bit_string = bit_string[:-padding]

        result = bytearray()
        node = tree
        for bit in bit_string:
            node = node.left if bit == '0' else node.right
            if node.byte is not None:
                result.append(node.byte)  # int to byte
                node = tree

        with open(output_path, 'wb') as out:
            out.write(result)

# -------------------- GUI --------------------

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("HuffPyZip - Groupe 3")
app.geometry("600x500")
app.resizable(False, False)

file_path = None

def choose_file():
    global file_path
    file_path = fd.askopenfilename(filetypes=[("All Files", "*.*")])
    if file_path:
        entry_file.configure(state="normal")
        entry_file.delete(0, "end")
        entry_file.insert(0, file_path)
        entry_file.configure(state="readonly")
        log_textbox.insert("end", f"📂 Fichier sélectionné : {file_path}\n")
        log_textbox.see("end")

def handle_compress():
    if not file_path:
        mb.showerror("Erreur", "Veuillez d'abord sélectionner un fichier.")
        return

    output_path = fd.asksaveasfilename(defaultextension=".huff",
                                       filetypes=[("Fichier compressé Huffman", "*.huff")],
                                       title="Enregistrer sous...")
    if not output_path:
        return

    log_textbox.insert("end", f"📦 Compression de : {file_path}\n")
    progressbar.set(0.2)

    try:
        start = time.time()
        frequencies = calculate_frequencies(file_path)
        sorted_frequencies = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)
        log_textbox.insert("end", "\n📊 Tableau des fréquences (triées décroissantes) :\n")
        for byte, freq in sorted_frequencies:
            log_textbox.insert("end", f"  {byte} : {freq}\n")

        compress_file(file_path, output_path)
        end = time.time()
        progressbar.set(1.0)
        log_textbox.insert("end", f"✅ Fichier compressé : {output_path}\n")

        original_size = os.path.getsize(file_path)
        compressed_size = os.path.getsize(output_path)
        rate = (1 - compressed_size / original_size) * 100
        log_textbox.insert("end", f"📉 Taux de compression : {rate:.2f}%\n")
        log_textbox.insert("end", f"⏱️ Temps : {end - start:.2f} sec\n")

    except Exception as e:
        mb.showerror("Erreur", str(e))
        log_textbox.insert("end", f"❌ Erreur : {e}\n")

    log_textbox.see("end")

def handle_decompress():
    if not file_path:
        mb.showerror("Erreur", "Veuillez d'abord sélectionner un fichier.")
        return

    output_path = fd.asksaveasfilename(defaultextension="", filetypes=[("Tous les fichiers", "*.*")])
    if not output_path:
        return

    log_textbox.insert("end", f"📤 Décompression de : {file_path}\n")
    progressbar.set(0.2)

    try:
        start = time.time()
        decompress_file(file_path, output_path)
        end = time.time()
        progressbar.set(1.0)
        log_textbox.insert("end", f"✅ Fichier décompressé : {output_path}\n")
        log_textbox.insert("end", f"⏱️ Temps : {end - start:.2f} sec\n")

    except Exception as e:
        mb.showerror("Erreur", str(e))
        log_textbox.insert("end", f"❌ Erreur : {e}\n")

    log_textbox.see("end")

frame = ctk.CTkFrame(app, width=560, height=460, corner_radius=20)
frame.place(relx=0.5, rely=0.5, anchor="center")

title = ctk.CTkLabel(frame, text="✨ HuffPyZip - Groupe 3", font=ctk.CTkFont(size=24, weight="bold"))
title.pack(pady=(20, 10))

entry_file = ctk.CTkEntry(frame, placeholder_text="Aucun fichier sélectionné", width=400)
entry_file.pack(pady=(5, 5))
entry_file.configure(state="readonly")

btn_choose = ctk.CTkButton(frame, text="📁 Choisir un fichier", command=choose_file)
btn_choose.pack(pady=(5, 10))

btns_frame = ctk.CTkFrame(frame, fg_color="transparent")
btns_frame.pack(pady=(5, 10))

btn_compress = ctk.CTkButton(btns_frame, text="📦 Compresser", command=handle_compress)
btn_compress.grid(row=0, column=0, padx=10)

btn_decompress = ctk.CTkButton(btns_frame, text="📤 Décompresser", command=handle_decompress)
btn_decompress.grid(row=0, column=1, padx=10)

progressbar = ctk.CTkProgressBar(frame, width=400)
progressbar.set(0)
progressbar.pack(pady=(10, 10))

log_textbox = ctk.CTkTextbox(frame, width=500, height=180)
log_textbox.pack(pady=(5, 10))

btn_quit = ctk.CTkButton(frame, text="❌ Terminer", command=app.destroy)
btn_quit.pack(pady=(5, 10))

app.mainloop()

