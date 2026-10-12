
import csv
import os
from models import Paket, Pemesanan


def simpan_pemesanan():
    print("\n=== TAMBAH PEMESANAN PAKET ===")

    nama = input("Nama pelanggan: ").strip()

    if not nama:
        print("Nama pelanggan harus diisi!")
        return

    daftar_paket = {
        "1": Paket("Basic", 50000),
        "2": Paket("Standard", 100000),
        "3": Paket("Premium", 150000)
    }

    print("\n=== PILIH PAKET ===")
    for nomor, paket in daftar_paket.items():
        print(f"{nomor}. {paket}")

    pilihan = input("Pilih paket (1-3): ")

    if pilihan not in daftar_paket:
        print("Pilihan paket tidak valid!")
        return

    try:
        jumlah = int(input("Jumlah paket: "))
        if jumlah <= 0:
            print("Jumlah paket harus lebih dari 0!")
            return
    except ValueError:
        print("Jumlah harus berupa angka!")
        return

    paket = daftar_paket[pilihan]

    id_pemesanan = "ORD" + str(
        sum(1 for _ in open("pemesanan.csv", encoding="utf-8"))
        if os.path.exists("pemesanan.csv") else 0
    ).zfill(3)

    pesanan = Pemesanan(
        id_pemesanan, nama, paket, jumlah
    )

    file_exists = os.path.exists("pemesanan.csv")

    with open(
        "pemesanan.csv", "a", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "ID", "Nama Pelanggan", "Paket",
                "Harga", "Jumlah", "Total", "Status"
            ])

        writer.writerow(pesanan.to_list())

    print("\n[PESANAN BERHASIL DISIMPAN]")
    print(pesanan)
    print(f"Status: {pesanan.status}")


def main():
    while True:
        print("\n=== MENU PEMESANAN ===")
        print("1. Tambah Pemesanan")
        print("0. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            simpan_pemesanan()

        elif pilihan == "0":
            print("Program selesai.")
            break

        else:
            print("Pilihan tidak valid!")


if __name__ == "__main__":
    main()
