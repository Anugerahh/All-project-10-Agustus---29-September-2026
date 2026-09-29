import random
import time
import sys
import os

def nyalakan_api():
    # Mengaktifkan ANSI escape sequence di Windows
    if os.name == 'nt':
        os.system('')
        
    # Bersihkan layar satu kali sebelum mulai
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Ukuran kanvas api
    lebar = 70
    tinggi = 22
    
    # Palet karakter ASCII dari dingin (kosong) ke panas (tebal) - 13 tingkat
    chars = " .,:-~=+*#%@@"
    
    # Grid penyimpan suhu api (semua diisi suhu 0 pada awalnya)
    grid = [[0 for _ in range(lebar)] for _ in range(tinggi)]
    
    print("\nMenyalakan api... (Tekan Ctrl+C untuk memadamkan)")
    time.sleep(1)
    
    try:
        while True:
            # 1. KAYU BAKAR: Beri suhu maksimal secara acak di baris paling bawah layar
            for x in range(lebar):
                # Randomize intensitas panas di dasar api
                grid[tinggi-1][x] = random.randint(9, 12)
                
            # 2. PERAMBATAN & PENDINGINAN API
            # Api selalu bergerak dari bawah ke atas
            for y in range(tinggi - 1):
                for x in range(lebar):
                    # Ambil suhu dari piksel tepat di bawahnya
                    suhu_bawah = grid[y+1][x]
                    
                    # Efek Pendinginan: Suhu berkurang seiring naiknya api
                    decay = random.randint(0, 1)
                    # Efek Angin: Lidah api bisa bergoyang ke kiri atau kanan
                    angin = random.randint(-1, 1)
                    
                    suhu_baru = suhu_bawah - decay
                    if suhu_baru < 0: 
                        suhu_baru = 0
                        
                    # Tentukan posisi lidah api yang baru di baris atasnya
                    target_x = x + angin
                    
                    # Pastikan apinya tidak keluar dari batas pinggir layar
                    if 0 <= target_x < lebar:
                        grid[y][target_x] = suhu_baru
                        
            # 3. PROSES RENDER KE TERMINAL
            # Pindahkan kursor ke pojok kiri atas agar tidak berkedip (flicker)
            sys.stdout.write('\x1b[H')
            
            for y in range(tinggi):
                baris = ""
                for x in range(lebar):
                    suhu = grid[y][x]
                    baris += chars[suhu]
                sys.stdout.write(baris + "\n")
            
            sys.stdout.flush()
            time.sleep(0.04) # Kecepatan kobaran api
            
    except KeyboardInterrupt:
        print("\n\nApi berhasil dipadamkan.")

if __name__ == "__main__":
    nyalakan_api()