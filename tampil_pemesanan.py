
import csv
import os
from models import Paket, Pemesanan


def muat_data():
    daftar_pemesanan = []

    if not os.path.exists("pemesanan.csv"):
        print("File pemesanan.csv belum tersedia.")
        return daftar_pemesanan

    with open(
        "pemesanan.csv", newline="", encoding="utf-8"
    ) as file:
        reader = csv.reader(file)
        next(reader, None)  # Lewati header

        for row in reader:
            if len(row) < 7:
                continue

            paket = Paket(row[2], int(row[3]))

            pesanan = Pemesanan(
                row[0],
                row[1],
                paket,
                int(row[4]),
                row[6]
            )

            daftar_pemesanan.append(pesanan)

    return daftar_pemesanan


def tampilkan_pemesanan():
    daftar = muat_data()

    if not daftar:
        print("Belum ada data pemesanan.")
        return

    print("\n=== DAFTAR PEMESANAN PAKET ===\n")

    print(
        f"{'ID':10}{'Nama':20}{'Paket':12}"
        f"{'Jumlah':10}{'Total':15}{'Status'}"
    )
    print("-" * 80)

    for pesanan in daftar:
        print(
            f"{pesanan.id_pemesanan:10}"
            f"{pesanan.nama_pelanggan:20}"
            f"{pesanan.paket.nama_paket:12}"
            f"{pesanan.jumlah:<10}"
            f"Rp{pesanan.hitung_total():<13,}"
            f"{pesanan.status}"
        )

    print("-" * 80)
    print(f"Total pesanan: {len(daftar)}")


def main():
    while True:
        print("\n=== MENU TAMPIL PEMESANAN ===")
        print("1. Tampilkan Pemesanan")
        print("2. Refresh Data")
        print("0. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampilkan_pemesanan()

        elif pilihan == "2":
            print("Data dimuat ulang...")
            tampilkan_pemesanan()

        elif pilihan == "0":
            print("Program selesai.")
            break

        else:
            print("Pilihan tidak valid!")


if __name__ == "__main__":
    main()
