
import tkinter.filedialog as fd
import customtkinter as ctk
from huffman_binary import compress_file, decompress_file

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("HuffPyZip - Groupe 3")
app.geometry("600x500")
app.resizable(False, False)

def choose_file():
    global file_path
    file_path = fd.askopenfilename(filetypes=[("All Files", "*.*")])
    if file_path:
        entry_file.configure(state="normal")
        entry_file.delete(0, "end")
        entry_file.insert(0, file_path)
        entry_file.configure(state="readonly")
        log_textbox.insert("end", f"📂 Fichier sélectionné : {file_path}\n")

def handle_compress():
    if file_path:
        output_path = file_path + ".huff"
        log_textbox.insert("end", f"Compression de : {file_path}\n")
        progressbar.set(0.2)
        compress_file(file_path, output_path)
        progressbar.set(1.0)
        log_textbox.insert("end", f"✅ Fichier compressé : {output_path}\n")

def handle_decompress():
    if file_path:
        output_path = file_path.replace(".huff", "_decompressed")
        log_textbox.insert("end", f"Décompression de : {file_path}\n")
        progressbar.set(0.2)
        decompress_file(file_path, output_path)
        progressbar.set(1.0)
        log_textbox.insert("end", f"✅ Fichier décompressé : {output_path}\n")

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
