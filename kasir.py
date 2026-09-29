import json
import os
from datetime import datetime


class Color:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


class Product:

    def __init__(self, product_id, name, price, stock, category):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "category": self.category,
        }

    @staticmethod
    def from_dict(data):
        return Product(
            data["product_id"],
            data["name"],
            data["price"],
            data["stock"],
            data["category"],
        )

class CartItem:

    def __init__(self, product, qty):
        self.product = product
        self.qty = qty

    @property
    def total_price(self):
        return self.product.price * self.qty


class Transaction:

    def __init__(
        self,
        trans_id,
        items,
        subtotal,
        tax,
        discount,
        grand_total,
        pay,
        change,
        timestamp=None,
    ):
        self.trans_id = trans_id
        self.items = items
        self.subtotal = subtotal
        self.tax = tax
        self.discount = discount
        self.grand_total = grand_total
        self.pay = pay
        self.change = change
        self.timestamp = timestamp or datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def to_dict(self):
        return {
            "trans_id": self.trans_id,
            "timestamp": self.timestamp,
            "items": [
                {
                    "name": item.product.name,
                    "price": item.product.price,
                    "qty": item.qty,
                    "total": item.total_price,
                }
                for item in self.items
            ],
            "subtotal": self.subtotal,
            "tax": self.tax,
            "discount": self.discount,
            "grand_total": self.grand_total,
            "pay": self.pay,
            "change": self.change,
        }


class Database:

    def __init__(
        self,
        products_file="products.json",
        history_file="transactions.json",
    ):
        self.products_file = products_file
        self.history_file = history_file

    def load_products(self):
        if not os.path.exists(self.products_file):
            default_products = [
                Product("P001", "Kopi Hitam", 15000, 50, "Minuman"),
                Product("P002", "Roti Bakar", 20000, 30, "Makanan"),
                Product("P003", "Es Teh Manis", 5000, 100, "Minuman"),
                Product("P004", "Nasi Goreng", 25000, 20, "Makanan"),
            ]
            self.save_products(default_products)
            return default_products

        try:
            with open(self.products_file, "r") as f:
                data = json.load(f)
                return [Product.from_dict(item) for item in data]
        except Exception:
            return []

    def save_products(self, products):
        with open(self.products_file, "w") as f:
            json.dump(
                [p.to_dict() for p in products], f, indent=4
            )

    def save_transaction(self, transaction):
        history = self.load_history()
        history.append(transaction.to_dict())
        with open(self.history_file, "w") as f:
            json.dump(history, f, indent=4)

    def load_history(self):
        if not os.path.exists(self.history_file):
            return []
        try:
            with open(self.history_file, "r") as f:
                return json.load(f)
        except Exception:
            return []


class POSApp:

    TAX_RATE = 0.11

    def __init__(self):
        self.db = Database()
        self.products = self.db.load_products()
        self.cart = []

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def print_header(self, title):
        print(Color.CYAN + "=" * 60)
        print(f"{title:^60}")
        print("=" * 60 + Color.ENDC)

    def format_rupiah(self, amount):
        return f"Rp {amount:,.0f}".replace(",", ".")

    def get_product_by_id(self, pid):
        for p in self.products:
            if p.product_id.upper() == pid.upper():
                return p
        return None

    def display_products(self):
        print(
            Color.BOLD
            + f"{'ID':<6} | {'Nama Produk':<20} | {'Kategori':<12} | {'Harga':<12} | {'Stok':<5}"
            + Color.ENDC
        )
        print("-" * 65)
        for p in self.products:
            print(
                f"{p.product_id:<6} | {p.name:<20} | {p.category:<12} | {self.format_rupiah(p.price):<12} | {p.stock:<5}"
            )
        print("-" * 65)

    def add_to_cart(self):
        self.display_products()
        pid = input("\nMasukkan ID Produk (atau 'x' batal): ").strip()
        if pid.lower() == "x":
            return

        product = self.get_product_by_id(pid)
        if not product:
            print(
                Color.FAIL
                + "Produk tidak ditemukan!"
                + Color.ENDC
            )
            input("Tekan Enter...")
            return

        try:
            qty = int(input(f"Jumlah untuk '{product.name}': "))
            if qty <= 0:
                print(
                    Color.FAIL
                    + "Jumlah harus lebih dari 0!"
                    + Color.ENDC
                )
            elif qty > product.stock:
                print(
                    Color.FAIL
                    + f"Stok tidak cukup! (Sisa: {product.stock})"
                    + Color.ENDC
                )
            else:
                for item in self.cart:
                    if item.product.product_id == product.product_id:
                        if item.qty + qty > product.stock:
                            print(
                                Color.FAIL
                                + "Total dalam keranjang melebihi stok!"
                                + Color.ENDC
                            )
                            input("Tekan Enter...")
                            return
                        item.qty += qty
                        print(
                            Color.GREEN
                            + "Jumlah produk di keranjang diperbarui!"
                            + Color.ENDC
                        )
                        input("Tekan Enter...")
                        return

                self.cart.append(CartItem(product, qty))
                print(
                    Color.GREEN
                    + f"'{product.name}' ditambahkan ke keranjang!"
                    + Color.ENDC
                )
        except ValueError:
            print(Color.FAIL + "Input harus angka!" + Color.ENDC)
        input("Tekan Enter...")

    def view_cart(self):
        if not self.cart:
            print(
                Color.WARNING
                + "Keranjang belanja kosong."
                + Color.ENDC
            )
            return False

        print(
            Color.BOLD
            + f"{'No':<3} | {'Nama Produk':<20} | {'Harga':<12} | {'Qty':<4} | {'Subtotal':<12}"
            + Color.ENDC
        )
        print("-" * 60)
        subtotal = 0
        for idx, item in enumerate(self.cart, 1):
            print(
                f"{idx:<3} | {item.product.name:<20} | {self.format_rupiah(item.product.price):<12} | {item.qty:<4} | {self.format_rupiah(item.total_price):<12}"
            )
            subtotal += item.total_price
        print("-" * 60)
        print(f"Subtotal: {self.format_rupiah(subtotal)}")
        return True

    def checkout(self):
        self.clear_screen()
        self.print_header("PROSES PEMBAYARAN")

        if not self.view_cart():
            input("\nTekan Enter...")
            return

        subtotal = sum(item.total_price for item in self.cart)

        discount = 0
        disc_input = input(
            "\nMasukkan Diskon (%) [0 jika tidak ada]: "
        ).strip()
        if disc_input.isdigit():
            disc_percent = float(disc_input)
            discount = subtotal * (disc_percent / 100)

        after_disc = subtotal - discount
        tax = after_disc * self.TAX_RATE
        grand_total = after_disc + tax

        print("\n" + "=" * 40)
        print(f"Subtotal     : {self.format_rupiah(subtotal)}")
        print(f"Diskon       : -{self.format_rupiah(discount)}")
        print(f"PPN (11%)    : +{self.format_rupiah(tax)}")
        print(
            Color.BOLD
            + f"TOTAL BAYAR  : {self.format_rupiah(grand_total)}"
            + Color.ENDC
        )
        print("=" * 40)

        while True:
            try:
                pay = float(
                    input("Jumlah Uang Diterima: Rp ")
                )
                if pay < grand_total:
                    print(
                        Color.FAIL
                        + "Uang pembayaran kurang!"
                        + Color.ENDC
                    )
                else:
                    change = pay - grand_total
                    print(
                        Color.GREEN
                        + f"Kembalian: {self.format_rupiah(change)}"
                        + Color.ENDC
                    )
                    break
            except ValueError:
                print(
                    Color.FAIL + "Input tidak valid!" + Color.ENDC
                )

        trans_id = f"TRX{datetime.now().strftime('%Y%m%d%H%M%S')}"
        transaction = Transaction(
            trans_id,
            self.cart,
            subtotal,
            tax,
            discount,
            grand_total,
            pay,
            change,
        )

        for item in self.cart:
            item.product.stock -= item.qty

        self.db.save_products(self.products)
        self.db.save_transaction(transaction)

        print(
            Color.GREEN
            + "\nTransaksi Berhasil Disimpan!"
            + Color.ENDC
        )
        self.print_receipt(transaction)

        self.cart = []
        input("\nTekan Enter untuk kembali ke menu utama...")

    def print_receipt(self, trans):
        print("\n" + "*" * 45)
        print(f"{'STRUK PEMBAYARAN TOKO SERBA':^45}")
        print(f"{'ID: ' + trans.trans_id:^45}")
        print(f"{trans.timestamp:^45}")
        print("*" * 45)
        for item in trans.items:
            print(f"{item.product.name}")
            print(
                f"  {item.qty} x {self.format_rupiah(item.product.price):<12} = {self.format_rupiah(item.total_price)}"
            )
        print("-" * 45)
        print(f"Subtotal     : {self.format_rupiah(trans.subtotal)}")
        print(f"Diskon       : -{self.format_rupiah(trans.discount)}")
        print(f"PPN (11%)    : +{self.format_rupiah(trans.tax)}")
        print(f"Grand Total  : {self.format_rupiah(trans.grand_total)}")
        print(f"Bayar        : {self.format_rupiah(trans.pay)}")
        print(f"Kembali      : {self.format_rupiah(trans.change)}")
        print("*" * 45)
        print(f"{'Terima Kasih Atas Kunjungan Anda!':^45}")
        print("*" * 45)

    def manage_products(self):
        while True:
            self.clear_screen()
            self.print_header("MANAJEMEN STOK PRODUK")
            self.display_products()
            print("\n1. Tambah Produk Baru")
            print("2. Update Stok Produk")
            print("3. Hapus Produk")
            print("0. Kembali")

            choice = input("\nPilih menu (0-3): ").strip()
            if choice == "1":
                pid = f"P{len(self.products) + 1:03d}"
                name = input("Nama Produk: ").strip()
                cat = input("Kategori: ").strip()
                try:
                    price = float(input("Harga: Rp "))
                    stock = int(input("Stok Awal: "))
                    self.products.append(
                        Product(pid, name, price, stock, cat)
                    )
                    self.db.save_products(self.products)
                    print(
                        Color.GREEN
                        + "Produk berhasil ditambahkan!"
                        + Color.ENDC
                    )
                except ValueError:
                    print(
                        Color.FAIL
                        + "Input harga/stok harus angka!"
                        + Color.ENDC
                    )
                input("Tekan Enter...")
            elif choice == "2":
                pid = input(
                    "Masukkan ID Produk yang diupdate: "
                ).strip()
                p = self.get_product_by_id(pid)
                if p:
                    try:
                        add_stock = int(
                            input(
                                f"Tambah stok untuk {p.name}: "
                            )
                        )
                        p.stock += add_stock
                        self.db.save_products(self.products)
                        print(
                            Color.GREEN
                            + "Stok berhasil diupdate!"
                            + Color.ENDC
                        )
                    except ValueError:
                        print(
                            Color.FAIL
                            + "Input stok harus angka!"
                            + Color.ENDC
                        )
                else:
                    print(
                        Color.FAIL
                        + "Produk tidak ditemukan!"
                        + Color.ENDC
                    )
                input("Tekan Enter...")
            elif choice == "3":
                pid = input(
                    "Masukkan ID Produk yang dihapus: "
                ).strip()
                p = self.get_product_by_id(pid)
                if p:
                    self.products.remove(p)
                    self.db.save_products(self.products)
                    print(
                        Color.GREEN
                        + "Produk berhasil dihapus!"
                        + Color.ENDC
                    )
                else:
                    print(
                        Color.FAIL
                        + "Produk tidak ditemukan!"
                        + Color.ENDC
                    )
                input("Tekan Enter...")
            elif choice == "0":
                break

    def view_history(self):
        self.clear_screen()
        self.print_header("RIWAYAT TRANSAKSI")
        history = self.db.load_history()

        if not history:
            print(
                Color.WARNING
                + "Belum ada transaksi tersimpan."
                + Color.ENDC
            )
        else:
            total_omset = 0
            for t in history:
                print(
                    f"ID: {t['trans_id']} | Tgl: {t['timestamp']} | Total: {self.format_rupiah(t['grand_total'])}"
                )
                total_omset += t["grand_total"]
            print("-" * 60)
            print(
                Color.BOLD
                + f"Total Omset: {self.format_rupiah(total_omset)}"
                + Color.ENDC
            )

        input("\nTekan Enter...")

    def run(self):
        while True:
            self.clear_screen()
            self.print_header("SYSTEM POINT OF SALE (KASIR)")
            print(f"Item di Keranjang: {len(self.cart)} item\n")
            print("1. Lihat Daftar Produk")
            print("2. Tambah Produk ke Keranjang")
            print("3. Lihat Keranjang & Checkout")
            print("4. Manajemen Stok Produk")
            print("5. Lihat Riwayat Transaksi")
            print("0. Keluar")

            choice = input("\nPilihan Menu (0-5): ").strip()

            if choice == "1":
                self.clear_screen()
                self.print_header("DAFTAR PRODUK")
                self.display_products()
                input("\nTekan Enter...")
            elif choice == "2":
                self.clear_screen()
                self.print_header("TAMBAH KELOMPOK BARANG")
                self.add_to_cart()
            elif choice == "3":
                if self.cart:
                    self.checkout()
                else:
                    self.clear_screen()
                    self.print_header("KERANJANG BELANJA")
                    self.view_cart()
                    input("\nTekan Enter...")
            elif choice == "4":
                self.manage_products()
            elif choice == "5":
                self.view_history()
            elif choice == "0":
                print(
                    Color.CYAN
                    + "\nTerima kasih telah menggunakan sistem kasir!"
                    + Color.ENDC
                )
                break


if __name__ == "__main__":
    app = POSApp()
    app.run()