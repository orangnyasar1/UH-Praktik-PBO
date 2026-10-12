
class Paket:
    def __init__(self, nama_paket, harga):
        self.nama_paket = nama_paket
        self.harga = harga

    def to_list(self):
        return [self.nama_paket, self.harga]

    def __str__(self):
        return f"{self.nama_paket} - Rp{self.harga:,}"


class Pemesanan:
    def __init__(
        self, id_pemesanan, nama_pelanggan,
        paket, jumlah, status="Diproses"
    ):
        self.id_pemesanan = id_pemesanan
        self.nama_pelanggan = nama_pelanggan
        self.paket = paket
        self.jumlah = jumlah
        self.status = status

    def hitung_total(self):
        return self.paket.harga * self.jumlah

    def to_list(self):
        return [
            self.id_pemesanan,
            self.nama_pelanggan,
            self.paket.nama_paket,
            self.paket.harga,
            self.jumlah,
            self.hitung_total(),
            self.status
        ]

    def __str__(self):
        return (
            f"{self.id_pemesanan} - {self.nama_pelanggan} "
            f"- {self.paket.nama_paket} "
            f"- Total: Rp{self.hitung_total():,}"
        )
