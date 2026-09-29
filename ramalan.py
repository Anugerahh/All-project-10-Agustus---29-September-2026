import random
import time

print("=" * 40)
print("🔮 SELAMAT DATANG DI MESIN PERAMAL ABSURD 🔮")
print("=" * 40)

nama = input("Siapa namamu, wahai manusia bumi? ")

print(f"\nHmm... {nama}, sistem sedang memindai masa depanmu...")
time.sleep(1.5)
print("Menganalisis gelombang aura positif...")
time.sleep(1.5)
print("Mengkoneksikan dengan satelit luar angkasa...\n")
time.sleep(2)

ramalan = [
    "Kamu akan menemukan uang Rp 20.000 di saku celana yang belum dicuci! 💸",
    "Besok, seekor kucing oren akan menatapmu dengan tajam dan mengklaim kamu sebagai babunya. 🐈",
    "Hati-hati, kamu akan tertawa ngakak melihat meme receh sampai tersedak air putih. 💧",
    "Seseorang akan membalas chat-mu dengan sangat cepat hari ini (tapi ternyata cuma operator). 📱",
    "Kecepatan Wi-Fi di rumahmu akan sangat kencang... tepat di saat kamu sudah mengantuk dan ingin tidur. 📶",
    "Kamu akan tiba-tiba hafal satu lagu random yang seliweran di FYP dan nyanyi terus seharian. 🎵"
]

print("✨ HASIL RAMALAN HARI INI ✨")
print(f">>> {random.choice(ramalan)} <<<")
print("\nTerima kasih sudah mencoba! Ingat, ini cuma buat seru-seruan ya! 😆")