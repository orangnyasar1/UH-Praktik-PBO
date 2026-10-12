
import subprocess


def buka_tambah_pemesanan():
    subprocess.run(["python", "tambah_pemesanan.py"])


def buka_tampil_pemesanan():
    subprocess.run(["python", "tampil_pemesanan.py"])


def menu_utama():
    while True:
        print("\n" + "=" * 40)
        print(" SISTEM PEMESANAN PAKET ".center(40, "="))
        print("=" * 40)
        print("1. Tambah Pemesanan")
        print("2. Tampilkan Pemesanan")
        print("0. Keluar")
        print("=" * 40)

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            buka_tambah_pemesanan()

        elif pilihan == "2":
            buka_tampil_pemesanan()

        elif pilihan == "0":
            print("Terima kasih.")
            break

        else:
            print("Pilihan tidak valid!")


if __name__ == "__main__":
    menu_utama()
