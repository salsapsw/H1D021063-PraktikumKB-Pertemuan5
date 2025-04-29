import tkinter as tk
from tkinter import messagebox
from pyswip import Prolog

prolog = Prolog()
prolog.consult("skin1004.pl")  

# Data Pertanyaan
pertanyaan = [
    ("Apakah kulit kamu kering?", "kering"),
    ("Apakah kulit kamu sensitif?", "sensitif"),
    ("Apakah kamu punya masalah iritasi?", "iritasi"),
    ("Apakah kamu suka produk natural?", "natural"),
]

jawaban_user = {}

index_pertanyaan = 0

def tampilkan_pertanyaan():
    if index_pertanyaan < len(pertanyaan):
        label_pertanyaan.config(text=pertanyaan[index_pertanyaan][0])
    else:
        proses_diagnosa()

def jawab(jawaban):
    global index_pertanyaan
    kunci = pertanyaan[index_pertanyaan][1]
    jawaban_user[kunci] = jawaban
    index_pertanyaan += 1
    tampilkan_pertanyaan()

def mulai_diagnosa():
    global index_pertanyaan
    index_pertanyaan = 0
    jawaban_user.clear()
    tampilkan_pertanyaan()

def proses_diagnosa():
    kulit = "sensitif" if jawaban_user.get("sensitif") else "kering"
    masalah = "iritasi" if jawaban_user.get("iritasi") else "dehidrasi"
    preferensi = "natural" if jawaban_user.get("natural") else "kimiawi"

    query = f"rekomendasi({kulit}, {masalah}, {preferensi}, R)"
    hasil = list(prolog.query(query))
    if hasil:
        produk = "\n".join(hasil[0]['R'])
        messagebox.showinfo("Rekomendasi Produk Skin1004", f"Berikut produk yang cocok untukmu:\n{produk}")
    else:
        messagebox.showinfo("Rekomendasi Produk Skin1004", "Tidak ada rekomendasi yang cocok ditemukan.")

# GUI
root = tk.Tk()
root.title("Sistem Pakar Rekomendasi Skincare Skin1004")

label_judul = tk.Label(root, text="Aplikasi Rekomendasi Skincare Skin1004", font=("Arial", 14, "bold"))
label_judul.pack(pady=10)

label_pertanyaan = tk.Label(root, text="", font=("Arial", 10))
label_pertanyaan.pack(pady=5)

frame_button = tk.Frame(root)
frame_button.pack(pady=5)

btn_tidak = tk.Button(frame_button, text="Tidak", width=10, command=lambda: jawab(False))
btn_tidak.pack(side=tk.LEFT, padx=5)

btn_ya = tk.Button(frame_button, text="Ya", width=10, command=lambda: jawab(True))
btn_ya.pack(side=tk.LEFT, padx=5)

btn_mulai = tk.Button(root, text="Mulai Diagnosa", command=mulai_diagnosa)
btn_mulai.pack(pady=10)

root.mainloop()
