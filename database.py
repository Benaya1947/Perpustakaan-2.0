import os
import utils
from datetime import datetime, timedelta

BUKU_PATH = os.path.join("data", "book.json")
MEMBER_PATH = os.path.join("data", "anggota.json")
PEMINJAMAN_PATH = os.path.join("data", "pinjam.json")
RIWAYAT_PATH = os.path.join("data", "riwayat_kembali.json")

DENDA_PER_HARI = 2000  # denda per hari keterlambatan

class BukuManager:
    def __init__(self):
        # Load data buku dari file JSON
        self.data = utils.load_json(BUKU_PATH, [])

        # Pastikan semua buku punya stok
        for b in self.data:
            if "stok" not in b:
                b["stok"] = 1  # default stok 1 buku


    def simpan(self):
        """Simpan data buku ke file JSON."""
        utils.save_json(BUKU_PATH, self.data)

    def lihat_semua(self):
        utils.clear_screen()
        print("=== DAFTAR BUKU PERPUSTAKAAN ===")
        if not self.data:
            print("(Belum ada data buku)")
        else:
            for i, buku in enumerate(self.data, start=1):
                print(f"{i}. Judul : {buku['judul']}")
                print(f"   Penulis : {buku['penulis']}")
                print(f"   Tahun : {buku['tahun']}")
                print(f"   Stok : {buku.get('stok', 0)}")  # ← tambahin ini
                print("-" * 30)
        utils.pause()


    def tambah(self):
        """Menambah buku baru (tidak boleh duplikat)."""
        utils.clear_screen()
        print("=== TAMBAH BUKU ===")
        judul = utils.input_tidak_kosong("Judul buku: ")

        # Cek duplikat berdasarkan judul
        for buku in self.data:
            if buku["judul"].lower() == judul.lower():
                print("⚠ Buku ini sudah ada di daftar!")
                utils.pause()
                return

        penulis = utils.input_tidak_kosong("Penulis: ")
        tahun = utils.input_angka("Tahun terbit: ")

        self.data.append({
            "judul": judul,
            "penulis": penulis,
            "tahun": tahun
        })
        self.simpan()
        print("✅ Buku berhasil ditambahkan!")
        utils.pause()


    def edit(self):
        """Mengedit data buku."""
        utils.clear_screen()
        print("=== EDIT DATA BUKU ===")
        self.lihat_semua()
        if not self.data:
            return

        index = utils.input_angka("Masukkan nomor buku yang ingin diedit: ") - 1
        if 0 <= index < len(self.data):
            judul = utils.input_tidak_kosong("Judul baru: ")
            penulis = utils.input_tidak_kosong("Penulis baru: ")
            tahun = utils.input_angka("Tahun baru: ")

            self.data[index] = {
                "judul": judul,
                "penulis": penulis,
                "tahun": tahun
            }
            self.simpan()
            print("✅ Data buku berhasil diubah!")
        else:
            print("⚠ Nomor buku tidak valid.")
        utils.pause()

    def hapus(self):
        """Menghapus buku."""
        utils.clear_screen()
        print("=== HAPUS DATA BUKU ===")
        self.lihat_semua()
        if not self.data:
            return

        index = utils.input_angka("Masukkan nomor buku yang ingin dihapus: ") - 1
        if 0 <= index < len(self.data):
            konfirmasi = input(f"Yakin ingin menghapus buku '{self.data[index]['judul']}'? (y/n): ").lower()
            if konfirmasi == "y":
                del self.data[index]
                self.simpan()
                print("✅ Buku berhasil dihapus.")
            else:
                print("❌ Dibatalkan.")
        else:
            print("⚠ Nomor buku tidak valid.")
        utils.pause()

class MemberManager:
    def __init__(self):
        # Load data member dari file JSON
        self.data = utils.load_json(MEMBER_PATH, [])

    def simpan(self):
        """Simpan data member ke file JSON."""
        utils.save_json(MEMBER_PATH, self.data)

    def lihat_semua(self):
        """Menampilkan semua anggota perpustakaan."""
        utils.clear_screen()
        print("=== DAFTAR ANGGOTA PERPUSTAKAAN ===")
        if not self.data:
            print("(Belum ada data anggota)")
        else:
            for i, anggota in enumerate(self.data, start=1):
                print(f"{i}. ID: {anggota['id']}")
                print(f"   Nama: {anggota['nama']}")
                print(f"   Nomor HP: {anggota['hp']}")
                print(f"   Alamat: {anggota['alamat']}")
                print("-" * 30)
        utils.pause()

    def tambah(self):
        """Menambah member baru (tidak boleh ID duplikat)."""
        utils.clear_screen()
        print("=== TAMBAH MEMBER ===")
        member_id = utils.input_tidak_kosong("ID Member: ").strip().lower()

        # Cek apakah ID sudah ada
        for m in self.data:
            if m.get("id", "").strip().lower() == member_id:
                print("⚠ Member dengan ID ini sudah terdaftar!")
                utils.pause()
                return

        nama = utils.input_tidak_kosong("Nama: ")
        hp = utils.input_tidak_kosong("Nomor HP: ")
        alamat = utils.input_tidak_kosong("Alamat: ")

        self.data.append({
            "id": member_id,  # simpan sudah dalam format lower
            "nama": nama,
            "hp": hp,
            "alamat": alamat
        })
        self.simpan()
        print("✅ Member berhasil ditambahkan!")
        utils.pause()


    def edit(self):
        """Mengedit data anggota."""
        utils.clear_screen()
        print("=== EDIT ANGGOTA PERPUSTAKAAN ===")
        self.lihat_semua()

        if not self.data:
            return

        index = utils.input_angka("Masukkan nomor anggota yang ingin diedit: ") - 1
        if 0 <= index < len(self.data):
            id_anggota = utils.input_tidak_kosong("ID Anggota baru: ")
            nama = utils.input_tidak_kosong("Nama baru: ")
            hp = utils.input_tidak_kosong("Nomor HP baru: ")
            alamat = utils.input_tidak_kosong("Alamat baru: ")

            self.data[index] = {
                "id": id_anggota,
                "nama": nama,
                "hp": hp,
                "alamat": alamat
            }
            self.simpan()
            print("✅ Data anggota berhasil diubah!")
        else:
            print("⚠ Nomor anggota tidak valid.")
        utils.pause()

    def hapus(self):
        """Menghapus data anggota."""
        utils.clear_screen()
        print("=== HAPUS ANGGOTA PERPUSTAKAAN ===")
        self.lihat_semua()

        if not self.data:
            return

        index = utils.input_angka("Masukkan nomor anggota yang ingin dihapus: ") - 1
        if 0 <= index < len(self.data):
            konfirmasi = input(f"Yakin ingin menghapus anggota '{self.data[index]['nama']}'? (y/n): ").lower()
            if konfirmasi == "y":
                del self.data[index]
                self.simpan()
                print("✅ Anggota berhasil dihapus.")
            else:
                print("❌ Dibatalkan.")
        else:
            print("⚠ Nomor anggota tidak valid.")
        utils.pause()

class PeminjamanManager:
    def __init__(self, buku_manager, member_manager):
        self.data = utils.load_json(PEMINJAMAN_PATH, [])       # pinjaman aktif
        self.riwayat = utils.load_json(RIWAYAT_PATH, []) # riwayat pengembalian
        self.buku_manager = buku_manager
        self.member_manager = member_manager

    def simpan(self):
        utils.save_json(PEMINJAMAN_PATH, self.data)
        utils.save_json(RIWAYAT_PATH, self.riwayat)

    def tampilkan_pinjaman_aktif(self):
        """Menampilkan daftar peminjaman tanpa pause."""
        print("=== DAFTAR PEMINJAMAN AKTIF ===")
        if not self.data:
            print("(Belum ada peminjaman aktif)")
        else:
            hari_ini = datetime.now().date()
            for i, pinjam in enumerate(self.data, start=1):
                tgl_kembali = datetime.strptime(pinjam["tgl_kembali"], "%Y-%m-%d").date()
                if hari_ini > tgl_kembali:
                    terlambat = (hari_ini - tgl_kembali).days
                    denda = terlambat * DENDA_PER_HARI
                    status = f"Terlambat {terlambat} hari (Denda: Rp {denda:,})"
                else:
                    status = "On Time"
                print(f"{i}. Anggota: {pinjam['nama_anggota']}")
                print(f"   Buku: {pinjam['judul_buku']}")
                print(f"   Tgl Pinjam: {pinjam['tgl_pinjam']}")
                print(f"   Tgl Kembali: {pinjam['tgl_kembali']}")
                print(f"   Status: {status}")
                print("-" * 30)

    def lihat_semua(self):
        utils.clear_screen()
        self.tampilkan_pinjaman_aktif()
        utils.pause()

    def lihat_riwayat(self):
        utils.clear_screen()
        print("=== RIWAYAT PENGEMBALIAN ===")
        if not self.riwayat:
            print("(Belum ada riwayat)")
        else:
            for i, r in enumerate(self.riwayat, start=1):
                print(f"{i}. Anggota: {r['nama_anggota']}")
                print(f"   Buku: {r['judul_buku']}")
                print(f"   Tgl Pinjam: {r['tgl_pinjam']}")
                print(f"   Tgl Kembali (Rencana): {r['tgl_kembali_rencana']}")
                print(f"   Tgl Dikembalikan: {r['tgl_dikembalikan']}")
                print(f"   Terlambat: {r['terlambat_hari']} hari")
                print(f"   Denda: Rp {r['denda']:,}")
                print("-" * 30)
        utils.pause()

    def pinjam_buku(self):
        utils.clear_screen()
        print("=== PINJAM BUKU ===")

        # Pilih anggota
        self.member_manager.lihat_semua()
        if not self.member_manager.data:
            return
        idx_member = utils.input_angka("Pilih nomor anggota: ") - 1
        if not (0 <= idx_member < len(self.member_manager.data)):
            print("⚠ Nomor anggota tidak valid.")
            utils.pause()
            return
        anggota = self.member_manager.data[idx_member]

        # Pilih buku
        self.buku_manager.lihat_semua()
        if not self.buku_manager.data:
            return
        idx_buku = utils.input_angka("Pilih nomor buku: ") - 1
        if not (0 <= idx_buku < len(self.buku_manager.data)):
            print("⚠ Nomor buku tidak valid.")
            utils.pause()
            return
        buku = self.buku_manager.data[idx_buku]

        # Cek stok buku
        if buku["stok"] <= 0:
            print("❌ Buku tidak tersedia.")
            utils.pause()
            return

        # Tanggal pinjam & kembali
        tgl_pinjam = datetime.now().date()
        tgl_kembali = tgl_pinjam + timedelta(days=7)  # default 7 hari

        # Simpan data pinjaman
        self.data.append({
            "nama_anggota": anggota["nama"],
            "judul_buku": buku["judul"],
            "tgl_pinjam": str(tgl_pinjam),
            "tgl_kembali": str(tgl_kembali)
        })

        # Kurangi stok buku
        buku["stok"] -= 1
        self.buku_manager.simpan()
        self.simpan()

        print(f"✅ Buku '{buku['judul']}' berhasil dipinjam oleh {anggota['nama']}.")
        utils.pause()

    def kembalikan_buku(self):
        utils.clear_screen()
        print("=== PENGEMBALIAN BUKU ===")

        if not self.data:
            print("(Tidak ada pinjaman aktif)")
            utils.pause()
            return

        self.tampilkan_pinjaman_aktif()

        idx = utils.input_angka("Pilih nomor peminjaman yang ingin dikembalikan: ") - 1
        if not (0 <= idx < len(self.data)):
            print("⚠ Nomor tidak valid.")
            utils.pause()
            return

        pinjam = self.data[idx]
        tgl_kembali = datetime.strptime(pinjam["tgl_kembali"], "%Y-%m-%d").date()
        hari_ini = datetime.now().date()
        terlambat = max(0, (hari_ini - tgl_kembali).days)
        total_denda = terlambat * DENDA_PER_HARI

        if terlambat > 0:
            print(f"⚠ Terlambat {terlambat} hari. Total denda: Rp{total_denda:,}")
            sisa = total_denda
            while sisa > 0:
                try:
                    bayar = int(input(f"Masukkan nominal pembayaran (Sisa: Rp{sisa:,}): "))
                except ValueError:
                    print("⚠ Masukkan angka yang benar!")
                    continue
                if bayar <= 0:
                    print("⚠ Nominal harus lebih dari 0.")
                    continue
                sisa -= bayar
                if sisa > 0:
                    print(f"💰 Uang kurang Rp{sisa:,}. Silakan tambahkan.")
                elif sisa < 0:
                    print(f"✅ Pembayaran berhasil. Kembalian Anda: Rp{-sisa:,}")
                else:
                    print("✅ Pembayaran pas. Terima kasih.")
        else:
            print("✅ Tidak ada denda. Pengembalian tepat waktu.")

        # Tambah stok buku kembali
        for buku in self.buku_manager.data:
            if buku["judul"] == pinjam["judul_buku"]:
                buku["stok"] += 1
                break

        # Simpan ke riwayat
        self.riwayat.append({
            "nama_anggota": pinjam["nama_anggota"],
            "judul_buku": pinjam["judul_buku"],
            "tgl_pinjam": pinjam["tgl_pinjam"],
            "tgl_kembali_rencana": pinjam["tgl_kembali"],
            "tgl_dikembalikan": str(hari_ini),
            "terlambat_hari": terlambat,
            "denda": total_denda
        })

        # Hapus dari daftar pinjaman aktif
        del self.data[idx]
        self.buku_manager.simpan()
        self.simpan()

        print("✅ Buku berhasil dikembalikan dan dicatat di riwayat.")
        utils.pause()
