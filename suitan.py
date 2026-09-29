import random

print("=== GAME BATU, KERTAS, GUNTING ===")
print("Pilih salah satu: batu, kertas, atau gunting")

pilihan_tersedia = ["batu", "kertas", "gunting"]

pilihan_pemain = input("Pilihanmu: ").lower()
pilihan_komputer = random.choice(pilihan_tersedia)

print(f"\nKamu memilih     : {pilihan_pemain}")
print(f"Komputer memilih : {pilihan_komputer}")
print("-" * 30)

if pilihan_pemain not in pilihan_tersedia:
    print("Pilihanmu tidak valid! Harus memilih batu, kertas, atau gunting.")
elif pilihan_pemain == pilihan_komputer:
    print("Hasil: Seri! Pemikiran kalian sama.")
elif (pilihan_pemain == "batu" and pilihan_komputer == "gunting") or \
     (pilihan_pemain == "kertas" and pilihan_komputer == "batu") or \
     (pilihan_pemain == "gunting" and pilihan_komputer == "kertas"):
    print("Hasil: KAMU MENANG! Selamat!")
else:
    print("Hasil: KOMPUTER MENANG! Coba lagi ya.")