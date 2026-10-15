import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox
from models import Paket, Pemesanan

FILE_DATA = "pemesanan.csv"
PAKET = {"Basic": 50000, "Standard": 100000, "Premium": 150000}
HEADER = ["ID", "Nama Pelanggan", "Paket", "Harga", "Jumlah", "Total", "Status"]


class AplikasiPemesanan:
    def __init__(self, root):
        self.root = root
        root.title("Paketin | Sistem Pemesanan Paket")
        root.geometry("920x620")
        root.minsize(800, 540)
        root.configure(bg="#F3F6FB")

        self.nama = tk.StringVar()
        self.pilihan = tk.StringVar(value="Standard")
        self.jumlah = tk.StringVar(value="1")
        self.harga = tk.StringVar()
        self.total = tk.StringVar()

        self.gaya()
        self.tampilan()
        self.perbarui_harga()
        self.muat_data()

    def gaya(self):
        s = ttk.Style()
        try:
            s.theme_use("clam")
        except tk.TclError:
            pass
        s.configure("Treeview", background="white", fieldbackground="white",
                    foreground="#172033", rowheight=30, font=("Segoe UI", 10))
        s.configure("Treeview.Heading", background="#E8EEF8",
                    foreground="#263653", font=("Segoe UI", 10, "bold"), padding=8)
        s.configure("TEntry", padding=7)
        s.configure("TCombobox", padding=6)

    def tampilan(self):
        header = tk.Frame(self.root, bg="#14213D", padx=26, pady=20)
        header.pack(fill="x")
        tk.Label(header, text="PAKETIN", bg="#14213D", fg="white",
                 font=("Segoe UI", 22, "bold")).pack(anchor="w")
        tk.Label(header, text="Sistem Pemesanan Paket", bg="#14213D",
                 fg="#C7D5EE", font=("Segoe UI", 10)).pack(anchor="w")

        body = tk.Frame(self.root, bg="#F3F6FB", padx=22, pady=18)
        body.pack(fill="both", expand=True)

        form = tk.Frame(body, bg="white", padx=18, pady=16,
                        highlightbackground="#E0E7F0", highlightthickness=1)
        form.pack(fill="x")
        tk.Label(form, text="Buat pemesanan", bg="white", fg="#172033",
                 font=("Segoe UI", 14, "bold")).grid(
                     row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

        labels = [("Nama pelanggan", 0), ("Pilih paket", 1), ("Jumlah", 2)]
        for label, col in labels:
            tk.Label(form, text=label, bg="white", fg="#45536B",
                     font=("Segoe UI", 10, "bold")).grid(
                         row=1, column=col, sticky="w", pady=5)

        self.nama_entry = ttk.Entry(form, textvariable=self.nama)
        self.nama_entry.grid(row=2, column=0, sticky="ew", padx=(0, 12))
        combo = ttk.Combobox(form, textvariable=self.pilihan,
                             values=list(PAKET), state="readonly")
        combo.grid(row=2, column=1, sticky="ew", padx=(0, 12))
        combo.bind("<<ComboboxSelected>>", self.perbarui_harga)
        spin = ttk.Spinbox(form, from_=1, to=999, textvariable=self.jumlah,
                           command=self.perbarui_total, width=7)
        spin.grid(row=2, column=2, sticky="ew", padx=(0, 12))
        spin.bind("<KeyRelease>", self.perbarui_total)

        price = tk.Frame(form, bg="#F0F5FF", padx=12, pady=8)
        price.grid(row=1, column=3, rowspan=2, sticky="nsew")
        tk.Label(price, text="HARGA PER PAKET", bg="#F0F5FF", fg="#5A6D8B",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(price, textvariable=self.harga, bg="#F0F5FF", fg="#2457D6",
                 font=("Segoe UI", 12, "bold")).pack(anchor="w")
        tk.Label(price, text="TOTAL PEMESANAN", bg="#F0F5FF", fg="#5A6D8B",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(7, 0))
        tk.Label(price, textvariable=self.total, bg="#F0F5FF", fg="#14213D",
                 font=("Segoe UI", 13, "bold")).pack(anchor="w")
        for col in range(4):
            form.grid_columnconfigure(col, weight=1)

        buttons = tk.Frame(form, bg="white")
        buttons.grid(row=3, column=0, columnspan=4, sticky="ew", pady=(16, 0))
        tk.Button(buttons, text="Simpan Pesanan", command=self.simpan,
                  bg="#2457D6", fg="white", activebackground="#1D46B0",
                  activeforeground="white", relief="flat", cursor="hand2",
                  font=("Segoe UI", 10, "bold"), padx=16, pady=9).pack(side="left")
        tk.Button(buttons, text="Bersihkan", command=self.bersihkan,
                  bg="#EEF2F8", fg="#263653", relief="flat", cursor="hand2",
                  padx=15, pady=9).pack(side="left", padx=8)
        tk.Button(buttons, text="Muat Ulang", command=self.muat_data,
                  bg="#EEF2F8", fg="#263653", relief="flat", cursor="hand2",
                  padx=15, pady=9).pack(side="right")

        table_frame = tk.Frame(body, bg="white", padx=14, pady=12,
                               highlightbackground="#E0E7F0", highlightthickness=1)
        table_frame.pack(fill="both", expand=True, pady=(14, 0))
        top = tk.Frame(table_frame, bg="white")
        top.pack(fill="x", pady=(0, 9))
        tk.Label(top, text="Daftar pemesanan", bg="white", fg="#172033",
                 font=("Segoe UI", 14, "bold")).pack(side="left")
        self.badge = tk.Label(top, text="0 pesanan", bg="#E8F0FF", fg="#2457D6",
                              font=("Segoe UI", 9, "bold"), padx=9, pady=5)
        self.badge.pack(side="right")

        cols = ("id", "nama", "paket", "harga", "jumlah", "total", "status")
        self.table = ttk.Treeview(table_frame, columns=cols, show="headings", height=7)
        headings = [
            ("id", "ID Pesanan", 90, "center"),
            ("nama", "Nama Pelanggan", 155, "w"),
            ("paket", "Paket", 95, "center"),
            ("harga", "Harga", 105, "e"),
            ("jumlah", "Jumlah", 65, "center"),
            ("total", "Total", 115, "e"),
            ("status", "Status", 90, "center"),
        ]
        for key, title, width, anchor in headings:
            self.table.heading(key, text=title)
            self.table.column(key, width=width, minwidth=55, anchor=anchor)
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scroll.set)
        self.table.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        tk.Label(self.root, text="Paketin  •  Data tersimpan di pemesanan.csv",
                 bg="#F3F6FB", fg="#718096", font=("Segoe UI", 9),
                 pady=7).pack(fill="x")

    @staticmethod
    def rupiah(angka):
        return "Rp" + f"{angka:,.0f}".replace(",", ".")

    def perbarui_harga(self, _event=None):
        harga = PAKET.get(self.pilihan.get(), 0)
        self.harga.set(self.rupiah(harga))
        self.perbarui_total()

    def perbarui_total(self, _event=None):
        try:
            jumlah = max(0, int(self.jumlah.get()))
        except (ValueError, tk.TclError):
            jumlah = 0
        self.total.set(self.rupiah(PAKET.get(self.pilihan.get(), 0) * jumlah))

    def pastikan_file(self):
        if not os.path.exists(FILE_DATA) or os.path.getsize(FILE_DATA) == 0:
            with open(FILE_DATA, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(HEADER)

    def buat_id(self):
        self.pastikan_file()
        terbesar = 0
        with open(FILE_DATA, newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row and row[0].startswith("ORD"):
                    try:
                        terbesar = max(terbesar, int(row[0][3:]))
                    except ValueError:
                        pass
        return f"ORD{terbesar + 1:03d}"

    def simpan(self):
        nama = self.nama.get().strip()
        paket_nama = self.pilihan.get()
        if not nama:
            messagebox.showwarning("Data belum lengkap",
                                   "Nama pelanggan wajib diisi.", parent=self.root)
            self.nama_entry.focus_set()
            return
        try:
            jumlah = int(self.jumlah.get())
            if jumlah < 1:
                raise ValueError
        except (ValueError, tk.TclError):
            messagebox.showwarning("Jumlah tidak valid",
                                   "Jumlah paket harus berupa angka minimal 1.",
                                   parent=self.root)
            return
        if paket_nama not in PAKET:
            messagebox.showwarning("Paket belum dipilih",
                                   "Silakan pilih paket terlebih dahulu.",
                                   parent=self.root)
            return

        paket = Paket(paket_nama, PAKET[paket_nama])
        pesanan = Pemesanan(self.buat_id(), nama, paket, jumlah, "Diproses")
        try:
            self.pastikan_file()
            with open(FILE_DATA, "a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(pesanan.to_list())
        except OSError as error:
            messagebox.showerror("Gagal menyimpan", str(error), parent=self.root)
            return

        self.muat_data()
        messagebox.showinfo(
            "Pesanan berhasil",
            f"ID: {pesanan.id_pemesanan}\nPelanggan: {nama}\n"
            f"Paket: {paket_nama}\nTotal: {self.rupiah(pesanan.hitung_total())}",
            parent=self.root)
        self.bersihkan()

    def bersihkan(self):
        self.nama.set("")
        self.pilihan.set("Standard")
        self.jumlah.set("1")
        self.perbarui_harga()
        self.nama_entry.focus_set()

    def muat_data(self):
        for item in self.table.get_children():
            self.table.delete(item)
        if not os.path.exists(FILE_DATA):
            self.badge.config(text="0 pesanan")
            return
        try:
            with open(FILE_DATA, newline="", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                next(reader, None)
                count = 0
                for row in reader:
                    if len(row) < 7:
                        continue
                    try:
                        harga, jumlah, total = int(row[3]), int(row[4]), int(row[5])
                    except ValueError:
                        continue
                    self.table.insert("", "end", values=(
                        row[0], row[1], row[2], self.rupiah(harga),
                        jumlah, self.rupiah(total), row[6]))
                    count += 1
            self.badge.config(text=f"{count} pesanan")
        except (OSError, csv.Error) as error:
            messagebox.showerror("Gagal membaca data", str(error), parent=self.root)


def main():
    root = tk.Tk()
    AplikasiPemesanan(root)
    root.mainloop()


if __name__ == "__main__":
    main()
