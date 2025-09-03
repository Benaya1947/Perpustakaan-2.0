import tkinter as tk  # import tkinter

# 1. Bikin window utama
window = tk.Tk()
window.title("Halo Tkinter!")   # judul jendela
window.geometry("400x200")      # ukuran jendela (px)

# 2. Bikin Label (tulisan)
label = tk.Label(window, text="Selamat datang di Tkinter!", font=("Arial", 14))
label.pack(pady=20)  # ditaruh di window + kasih jarak vertical

# 3. Bikin fungsi untuk tombol
def ubah_teks():
    label.config(text="Tombol sudah diklik!")

# 4. Bikin Button
button = tk.Button(window, text="Klik Saya", command=ubah_teks)
button.pack()

# 5. Jalankan window
window.mainloop()
