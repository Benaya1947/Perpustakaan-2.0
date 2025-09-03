import sys
import os
import tkinter as tk
from tkinter import messagebox
import datetime

# Tambahkan parent folder (Perpustakaan-2.0) ke sys.path
base_dir = os.path.dirname(os.path.abspath(__file__))  # = .../Perpustakaan-2.0/GUI
project_dir = os.path.abspath(os.path.join(base_dir, ".."))  # naik ke Perpustakaan-2.0
sys.path.append(project_dir)

import utils
print("Utils yang kepanggil:", utils.__file__)  # cek path utils.py yang dipakai


# pastikan bisa import utils.py dari root project
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_path not in sys.path:
    sys.path.append(project_path)

from utils import load_json, save_json

# --- Fungsi login ---
def login():
    username = entry_username.get()
    password = entry_password.get()

    akun_list = load_json(os.path.join(project_dir, "data", "akun.json"), [])

    for akun in akun_list:
        if akun["username"] == username and akun["password"] == password:
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {akun['username']} ({akun['role']})!")

            # Tutup window login
            root.destroy()

            # Buka dashboard sesuai role
            if akun["role"] == "Admin":
                open_admin_dashboard(akun["username"])
            else:
                open_member_dashboard(akun["username"])
            return

    messagebox.showerror("Login Gagal", "Username atau password salah.")

#===============================================================================================#

# --- Dashboard Admin ---
def open_admin_dashboard(username):
    admin_win = tk.Tk()
    admin_win.title("Admin Dashboard")
    tk.Label(admin_win, text=f"Halo Admin {username}!", font=("Arial", 14)).pack(pady=20)

    tk.Button(admin_win, text="Kelola Buku", command=kelola_buku).pack(pady=5)
    tk.Button(admin_win, text="Kelola Member", command=kelola_member).pack(pady=5)
    tk.Button(admin_win, text="Logout", command=admin_win.destroy).pack(pady=20)

    admin_win.mainloop()

# --- Fitur Kelola Buku (Admin) ---
def kelola_buku():
    buku_win = tk.Toplevel()
    buku_win.title("Kelola Buku")
    buku_win.geometry("400x300")

    # load data buku
    buku_list = load_json(os.path.join(project_dir, "data", "buku.json"), [])

    # tampilkan daftar buku
    listbox = tk.Listbox(buku_win, width=50)
    listbox.pack(pady=10)

    def refresh_listbox():
        listbox.delete(0, tk.END)
        for buku in buku_list:
            listbox.insert(
                tk.END,
                f"{buku['id']} - {buku['judul']} ({buku['penulis']}) | Stok: {buku['stok']}"
            )

    refresh_listbox()

    # tombol tambah buku
    def tambah_buku():
        tambah_win = tk.Toplevel(buku_win)
        tambah_win.title("Tambah Buku")

        tk.Label(tambah_win, text="Judul:").pack()
        entry_judul = tk.Entry(tambah_win)
        entry_judul.pack()

        tk.Label(tambah_win, text="Penulis:").pack()
        entry_penulis = tk.Entry(tambah_win)
        entry_penulis.pack()

        tk.Label(tambah_win, text="Stok:").pack()
        entry_stok = tk.Entry(tambah_win)
        entry_stok.pack()

        def simpan():
            buku_baru = {
                "id": len(buku_list) + 1,
                "judul": entry_judul.get(),
                "penulis": entry_penulis.get(),
                "stok": int(entry_stok.get())
            }
            buku_list.append(buku_baru)
            save_json(os.path.join(project_dir, "data", "buku.json"), buku_list)
            listbox.insert(tk.END, f"{buku_baru['id']} - {buku_baru['judul']} ({buku_baru['penulis']}) | Stok: {buku_baru['stok']}")
            tambah_win.destroy()

        tk.Button(tambah_win, text="Simpan", command=simpan).pack(pady=5)

    # --- Edit Buku ---
    def edit_buku():
        try:
            index = listbox.curselection()[0]
        except IndexError:
            messagebox.showerror("Error", "Pilih buku dulu!")
            return

        buku = buku_list[index]

        edit_win = tk.Toplevel(buku_win)
        edit_win.title("Edit Buku")

        tk.Label(edit_win, text="Judul:").pack()
        entry_judul = tk.Entry(edit_win)
        entry_judul.insert(0, buku["judul"])
        entry_judul.pack()

        tk.Label(edit_win, text="Penulis:").pack()
        entry_penulis = tk.Entry(edit_win)
        entry_penulis.insert(0, buku["penulis"])
        entry_penulis.pack()

        tk.Label(edit_win, text="Stok:").pack()
        entry_stok = tk.Entry(edit_win)
        entry_stok.insert(0, buku["stok"])
        entry_stok.pack()

        def simpan_edit():
            buku["judul"] = entry_judul.get()
            buku["penulis"] = entry_penulis.get()
            buku["stok"] = int(entry_stok.get())
            save_json(os.path.join(project_dir, "data", "buku.json"), buku_list)
            refresh_listbox()
            edit_win.destroy()

        tk.Button(edit_win, text="Simpan", command=simpan_edit).pack(pady=5)

    # --- Hapus Buku ---
    def hapus_buku():
        try:
            index = listbox.curselection()[0]
        except IndexError:
            messagebox.showerror("Error", "Pilih buku dulu!")
            return

        buku = buku_list[index]
        if messagebox.askyesno("Konfirmasi", f"Yakin mau hapus buku '{buku['judul']}'?"):
            buku_list.pop(index)
            save_json(os.path.join(project_dir, "data", "buku.json"), buku_list)
            refresh_listbox()

    # tombol-tombol
    tk.Button(buku_win, text="Tambah Buku", command=tambah_buku).pack(pady=5)
    tk.Button(buku_win, text="Edit Buku", command=edit_buku).pack(pady=5)
    tk.Button(buku_win, text="Hapus Buku", command=hapus_buku).pack(pady=5)

# --- Fitur Kelola Member (Admin) ---
def kelola_member():
    member_win = tk.Toplevel()
    member_win.title("Kelola Member")
    member_win.geometry("400x300")

    # load data member
    member_list = load_json(os.path.join(project_dir, "data", "member.json"), [])

    # Listbox untuk tampilkan member
    listbox = tk.Listbox(member_win, width=50)
    listbox.pack(pady=10)

    def refresh_listbox():
        listbox.delete(0, tk.END)
        for m in member_list:
            listbox.insert(tk.END, f"{m['id']} - {m['nama']} | {m['email']}")

    refresh_listbox()

    # --- Tambah Member ---
    def tambah_member():
        tambah_win = tk.Toplevel(member_win)
        tambah_win.title("Tambah Member")

        tk.Label(tambah_win, text="Nama:").pack()
        entry_nama = tk.Entry(tambah_win)
        entry_nama.pack()

        tk.Label(tambah_win, text="Email:").pack()
        entry_email = tk.Entry(tambah_win)
        entry_email.pack()

        def simpan():
            member_baru = {
                "id": len(member_list) + 1,
                "nama": entry_nama.get(),
                "email": entry_email.get()
            }
            member_list.append(member_baru)
            save_json(os.path.join(project_dir, "data", "member.json"), member_list)
            refresh_listbox()
            tambah_win.destroy()

        tk.Button(tambah_win, text="Simpan", command=simpan).pack(pady=5)

    # --- Edit Member ---
    def edit_member():
        try:
            index = listbox.curselection()[0]
        except IndexError:
            messagebox.showerror("Error", "Pilih member dulu!")
            return

        m = member_list[index]

        edit_win = tk.Toplevel(member_win)
        edit_win.title("Edit Member")

        tk.Label(edit_win, text="Nama:").pack()
        entry_nama = tk.Entry(edit_win)
        entry_nama.insert(0, m["nama"])
        entry_nama.pack()

        tk.Label(edit_win, text="Email:").pack()
        entry_email = tk.Entry(edit_win)
        entry_email.insert(0, m["email"])
        entry_email.pack()

        def simpan_edit():
            m["nama"] = entry_nama.get()
            m["email"] = entry_email.get()
            save_json(os.path.join(project_dir, "data", "member.json"), member_list)
            refresh_listbox()
            edit_win.destroy()

        tk.Button(edit_win, text="Simpan", command=simpan_edit).pack(pady=5)

    # --- Hapus Member ---
    def hapus_member():
        try:
            index = listbox.curselection()[0]
        except IndexError:
            messagebox.showerror("Error", "Pilih member dulu!")
            return

        m = member_list[index]
        if messagebox.askyesno("Konfirmasi", f"Yakin mau hapus member '{m['nama']}'?"):
            member_list.pop(index)
            save_json(os.path.join(project_dir, "data", "member.json"), member_list)
            refresh_listbox()

    # Tombol-tombol
    tk.Button(member_win, text="Tambah Member", command=tambah_member).pack(pady=5)
    tk.Button(member_win, text="Edit Member", command=edit_member).pack(pady=5)
    tk.Button(member_win, text="Hapus Member", command=hapus_member).pack(pady=5)

#===============================================================================================#

# --- Dashboard Member ---
def open_member_dashboard(username):
    member_win = tk.Tk()
    member_win.title("Member Dashboard")
    tk.Label(member_win, text=f"Halo {username}!", font=("Arial", 14)).pack(pady=20)

    tk.Button(member_win, text="Lihat Buku", command=lihat_buku).pack(pady=5)
    tk.Button(member_win, text="Pinjam Buku", command=lambda: pinjam_buku(username)).pack(pady=5)
    tk.Button(member_win, text="Kembalikan Buku", command=lambda: kembalikan_buku(username)).pack(pady=5)
    tk.Button(member_win, text="Cek Saldo", command=lambda: cek_saldo(username)).pack(pady=5)
    tk.Button(member_win, text="Isi Saldo", command=lambda: isi_saldo(username)).pack(pady=5)
    tk.Button(member_win, text="Logout", command=member_win.destroy).pack(pady=20)

    member_win.mainloop()

# --- Lihat Buku ---
def lihat_buku():
    buku_win = tk.Toplevel()
    buku_win.title("Daftar Buku")
    buku_win.geometry("400x300")

    buku_list = load_json(os.path.join(project_dir, "data", "buku.json"), [])

    listbox = tk.Listbox(buku_win, width=50)
    listbox.pack(pady=10)

    for buku in buku_list:
        listbox.insert(tk.END, f"{buku['id']} - {buku['judul']} ({buku['penulis']}) | Stok: {buku['stok']}")

# --- Pinjam Buku ---
def pinjam_buku(username):
    pinjam_win = tk.Toplevel()
    pinjam_win.title("Pinjam Buku")
    pinjam_win.geometry("400x300")

    buku_list = load_json(os.path.join(project_dir, "data", "buku.json"), [])
    peminjaman_list = load_json(os.path.join(project_dir, "data", "peminjaman.json"), [])

    listbox = tk.Listbox(pinjam_win, width=50)
    listbox.pack(pady=10)

    for buku in buku_list:
        listbox.insert(tk.END, f"{buku['id']} - {buku['judul']} (Stok: {buku['stok']})")

    def konfirmasi_pinjam():
        try:
            index = listbox.curselection()[0]
        except IndexError:
            messagebox.showerror("Error", "Pilih buku dulu!")
            return

        buku = buku_list[index]
        if buku["stok"] <= 0:
            messagebox.showerror("Error", "Stok buku habis!")
            return

        # Kurangi stok
        buku["stok"] -= 1
        save_json(os.path.join(project_dir, "data", "buku.json"), buku_list)

        # Catat peminjaman
        today = datetime.date.today()
        due_date = today + datetime.timedelta(days=7)  # jatuh tempo 7 hari

        peminjaman_baru = {
            "username": username,
            "id_buku": buku["id"],
            "judul": buku["judul"],
            "tanggal_pinjam": str(today),
            "tanggal_kembali": str(due_date),
            "status": "dipinjam"
        }
        peminjaman_list.append(peminjaman_baru)
        save_json(os.path.join(project_dir, "data", "peminjaman.json"), peminjaman_list)

        messagebox.showinfo("Berhasil", f"Buku '{buku['judul']}' berhasil dipinjam.\nHarus dikembalikan sebelum {due_date}.")
        pinjam_win.destroy()

    tk.Button(pinjam_win, text="Pinjam", command=konfirmasi_pinjam).pack(pady=5)

# --- Kembalikan Buku ---
def kembalikan_buku(username):
    kembali_win = tk.Toplevel()
    kembali_win.title("Kembalikan Buku")
    kembali_win.geometry("400x300")

    buku_list = load_json(os.path.join(project_dir, "data", "buku.json"), [])
    member_list = load_json(os.path.join(project_dir, "data", "member.json"), [])
    peminjaman_list = load_json(os.path.join(project_dir, "data", "peminjaman.json"), [])

    listbox = tk.Listbox(kembali_win, width=50)
    listbox.pack(pady=10)

    # filter hanya pinjaman aktif si user
    pinjaman_user = [p for p in peminjaman_list if p["username"] == username and p["status"] == "dipinjam"]

    for p in pinjaman_user:
        listbox.insert(tk.END, f"{p['id_buku']} - {p['judul']} (Jatuh tempo: {p['tanggal_kembali']})")

    def konfirmasi_kembali():
        try:
            index = listbox.curselection()[0]
        except IndexError:
            messagebox.showerror("Error", "Pilih buku dulu!")
            return

        pinjaman = pinjaman_user[index]
        today = datetime.date.today()
        due_date = datetime.date.fromisoformat(pinjaman["tanggal_kembali"])

        # Hitung denda
        denda_per_hari = 1000
        terlambat = (today - due_date).days
        denda = denda_per_hari * terlambat if terlambat > 0 else 0

        # update saldo member
        for m in member_list:
            if m["username"] == username:
                if denda > 0:
                    if m.get("saldo", 0) < denda:
                        messagebox.showerror("Error", f"Saldo tidak cukup untuk bayar denda Rp{denda}")
                        return
                    m["saldo"] -= denda
                break

        save_json(os.path.join(project_dir, "data", "member.json"), member_list)

        # update stok buku
        for b in buku_list:
            if b["id"] == pinjaman["id_buku"]:
                b["stok"] += 1
                break
        save_json(os.path.join(project_dir, "data", "buku.json"), buku_list)

        # update status peminjaman
        for p in peminjaman_list:
            if p is pinjaman:
                p["status"] = "dikembalikan"
                break
        save_json(os.path.join(project_dir, "data", "peminjaman.json"), peminjaman_list)

        messagebox.showinfo("Berhasil", f"Buku '{pinjaman['judul']}' berhasil dikembalikan.\nDenda: Rp{denda}")
        kembali_win.destroy()

    tk.Button(kembali_win, text="Kembalikan", command=konfirmasi_kembali).pack(pady=5)

# --- Cek Saldo ---
def cek_saldo(username):
    members = load_json(os.path.join(project_dir, "data", "member.json"), [])
    for m in members:
        if m["username"] == username:
            messagebox.showinfo("Cek Saldo", f"Saldo Anda saat ini: Rp {m['saldo']:,}")
            return
    messagebox.showerror("Error", "Data member tidak ditemukan.")

# --- Isi Saldo ---
def isi_saldo(username):
    isi_win = tk.Toplevel()
    isi_win.title("Isi Saldo")
    isi_win.geometry("300x200")

    tk.Label(isi_win, text="Masukkan nominal isi saldo:").pack(pady=10)
    entry_nominal = tk.Entry(isi_win)
    entry_nominal.pack(pady=5)

    def simpan_saldo():
        try:
            nominal = int(entry_nominal.get())
            if nominal <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Nominal harus angka positif!")
            return

        member_list = load_json(os.path.join(project_dir, "data", "member.json"), [])
        for m in member_list:
            if m["username"] == username:
                m["saldo"] = m.get("saldo", 0) + nominal
                break
        save_json(os.path.join(project_dir, "data", "member.json"), member_list)

        messagebox.showinfo("Berhasil", f"Saldo berhasil ditambah Rp{nominal}")
        isi_win.destroy()

    tk.Button(isi_win, text="Isi Saldo", command=simpan_saldo).pack(pady=10)


#===============================================================================================

# --- UI setup ---
root = tk.Tk()
root.title("Login Form")
root.geometry("300x200")

# Username
tk.Label(root, text="Username").pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

# Password
tk.Label(root, text="Password").pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

# Tombol Login
tk.Button(root, text="Login", command=login).pack(pady=20)

root.mainloop()

