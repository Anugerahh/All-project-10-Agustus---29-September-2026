from getpass import getpass

print("=== GAME SUIT 2 PLAYER ===")

pilihan_valid = ["batu", "gunting", "kertas"]

nama_p1 = input("Masukkan nama Player 1: ")
nama_p2 = input("Masukkan nama Player 2: ")

print(f"\n{nama_p1}, giliranmu memilih!")
print("Ketik pilihanmu (batu/gunting/kertas). Keteilkanmu TIDAK AKAN MUNCUL di layar agar rahasia!")
pilihan_p1 = getpass("Pilihan Player 1: ").lower()

print("\n" * 50)
print("Pilihan Player 1 sudah tersimpan secara rahasia!")
print("-" * 40)

print(f"{nama_p2}, sekarang giliranmu!")
pilihan_p2 = input("Pilihan Player 2 (batu/gunting/kertas): ").lower()

print("\n" + "=" * 40)
print(f"{nama_p1} memilih : {pilihan_p1}")
print(f"{nama_p2} memilih : {pilihan_p2}")
print("=" * 40)

if pilihan_p1 not in pilihan_valid or pilihan_p2 not in pilihan_valid:
    print("Ada pilihan yang salah/salah ketik! Gunakan hanya batu, gunting, atau kertas.")
elif pilihan_p1 == pilihan_p2:
    print("Hasil: SERI! Kalian berdua memilih hal yang sama.")
elif (pilihan_p1 == "batu" and pilihan_p2 == "gunting") or \
     (pilihan_p1 == "gunting" and pilihan_p2 == "kertas") or \
     (pilihan_p1 == "kertas" and pilihan_p2 == "batu"):
    print(f"Hasil: SELAMAT! {nama_p1.upper()} MENANG!")
else:
    print(f"Hasil: SELAMAT! {nama_p2.upper()} MENANG!")