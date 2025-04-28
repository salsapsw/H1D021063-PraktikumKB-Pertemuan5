import tkinter as tk
from tkinter import ttk, messagebox
from pyswip import Prolog

# Inisialisasi Prolog
prolog = Prolog()
prolog.consult("pakar_malaria_gui.pl")

# State aplikasi
disease_list = []
syndromes_map = {}
index_penyakit = 0
index_gejala = 0
current_penyakit = ""
current_gejala = ""


def mulai_diagnosa():
    global disease_list, syndromes_map, index_penyakit, index_gejala
    # Bersihkan database gejala di Prolog
    prolog.retractall("gejala_pos(_)")
    prolog.retractall("gejala_neg(_)")

    # Update state tombol
    start_btn.config(state=tk.DISABLED)
    yes_btn.config(state=tk.NORMAL)
    no_btn.config(state=tk.NORMAL)

    # Ambil daftar penyakit dari Prolog
    disease_list = [p["X"] for p in prolog.query("penyakit(X)")]
    # Bangun mapping penyakit -> list gejala
    syndromes_map.clear()
    for disease in disease_list:
        syndromes_map[disease] = [g["X"] for g in prolog.query(f'gejala(X, "{disease}")')]

    index_penyakit = 0
    index_gejala = -1
    pertanyaan_selanjutnya()


def pertanyaan_selanjutnya(ganti_penyakit=False):
    global index_penyakit, index_gejala, current_penyakit, current_gejala

    if ganti_penyakit:
        index_penyakit += 1
        index_gejala = -1

    # Jika semua penyakit sudah dicek
    if index_penyakit >= len(disease_list):
        hasil_diagnosa()
        return

    current_penyakit = disease_list[index_penyakit]
    index_gejala += 1

    # Jika semua gejala untuk penyakit ini sudah ditanyakan
    if index_gejala >= len(syndromes_map[current_penyakit]):
        hasil_diagnosa(current_penyakit)
        return

    current_gejala = syndromes_map[current_penyakit][index_gejala]

    # Cek apakah gejala sudah diberi jawaban
    if list(prolog.query(f"gejala_pos({current_gejala})")):
        return pertanyaan_selanjutnya()
    if list(prolog.query(f"gejala_neg({current_gejala})")):
        return pertanyaan_selanjutnya(ganti_penyakit=True)

    # Ambil pertanyaan dari Prolog
    q = next(prolog.query(f'pertanyaan({current_gejala}, Q)'))["Q"]
    if isinstance(q, bytes):
        q = q.decode()
    tampilkan_pertanyaan(q)


def tampilkan_pertanyaan(text):
    kotak_pertanyaan.config(state=tk.NORMAL)
    kotak_pertanyaan.delete("1.0", tk.END)
    kotak_pertanyaan.insert(tk.END, text)
    kotak_pertanyaan.config(state=tk.DISABLED)


def jawaban(ans):
    if ans:
        prolog.assertz(f"gejala_pos({current_gejala})")
        pertanyaan_selanjutnya()
    else:
        prolog.assertz(f"gejala_neg({current_gejala})")
        pertanyaan_selanjutnya(ganti_penyakit=True)


def hasil_diagnosa(penyakit=None):
    yes_btn.config(state=tk.DISABLED)
    no_btn.config(state=tk.DISABLED)
    start_btn.config(state=tk.NORMAL)

    if penyakit:
        messagebox.showinfo("Hasil Diagnosa", f"Anda terdeteksi: {penyakit}")
    else:
        messagebox.showinfo("Hasil Diagnosa", "Tidak terdeteksi penyakit.")


# ----- Setup GUI -----
root = tk.Tk()
root.title("Sistem Pakar Diagnosis Penyakit Malaria")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Judul aplikasi
ttk.Label(mainframe, text="Aplikasi Diagnosa Penyakit Malaria",
          font=("Arial", 16)).grid(column=0, row=0, columnspan=3, pady=5)

# Label kolom pertanyaan
ttk.Label(mainframe, text="Kolom Pertanyaan:").grid(column=0, row=1)

# Kotak pertanyaan
kotak_pertanyaan = tk.Text(mainframe, height=4, width=40, state=tk.DISABLED)
kotak_pertanyaan.grid(column=0, row=2, columnspan=3, pady=5)

# Tombol Ya / Tidak
yes_btn = ttk.Button(mainframe, text="Ya", state=tk.DISABLED, command=lambda: jawaban(True))
yes_btn.grid(column=1, row=3, sticky=(tk.W, tk.E), padx=5, pady=5)
no_btn = ttk.Button(mainframe, text="Tidak", state=tk.DISABLED, command=lambda: jawaban(False))
no_btn.grid(column=2, row=3, sticky=(tk.W, tk.E), padx=5, pady=5)

# Tombol Mulai
start_btn = ttk.Button(mainframe, text="Mulai Diagnosa", command=mulai_diagnosa)
start_btn.grid(column=1, row=4, columnspan=2, sticky=(tk.W, tk.E), pady=10)

# Padding uniform untuk semua widget
for widget in mainframe.winfo_children():
    widget.grid_configure(padx=5, pady=5)

# Jalankan GUI
root.mainloop()
