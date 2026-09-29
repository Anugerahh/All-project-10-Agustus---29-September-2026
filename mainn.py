import random

print("=== Game Tebak Angka Rahasia ===")
print("Aku sudah memilih angka antara 1 sampai 100.")
print("Kamu punya 3 kali kesempatan untuk menebaknya!")

angka_rahasia = random.randint(1, 100)
tebakan_benar = False
kesempatan = 3

while kesempatan > 0 and not tebakan_benar:
    print(f"\nSisa kesempatanmu: {kesempatan}")
    tebakan_pemain = input("Masukkan angka tebakanmu: ")
    tebakan = int(tebakan_pemain)
    
    if tebakan == angka_rahasia:
        tebakan_benar = True
        print("Wah, tebakanmu BENAR! Kamu menang!")
    elif tebakan < angka_rahasia:
        print("Tebakanmu terlalu KECIL.")
    else:
        print("Tebakanmu terlalu BESAR.")
        
    kesempatan = kesempatan - 1

if not tebakan_benar:
    print("\nSayang sekali, kesempatanmu sudah habis.")
    print(f"Angka rahasianya adalah {angka_rahasia}. Coba lagi nanti ya!")