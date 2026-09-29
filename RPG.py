import random
import time

print("=== DUNGEON ADVENTURE RPG ===")
nama_pahlawan = input("Masukkan nama pahlawanmu: ")

hp_pahlawan = 100
serangan_min = 15
serangan_max = 25
ramuan = 3

nama_monster = "Naga Bayangan"
hp_monster = 120
serangan_monster_min = 10
serangan_monster_max = 20

print(f"\n{nama_pahlawan} memasuki gua gelap dan berhadapan dengan {nama_monster}!")
print("Pertarungan sengit dimulai!\n")

while hp_pahlawan > 0 and hp_monster > 0:
    print("=" * 40)
    print(f"HP {nama_pahlawan}: {hp_pahlawan} | Ramuan Penyembuh: {ramuan}")
    print(f"HP {nama_monster}: {hp_monster}")
    print("=" * 40)
    
    print("PILIH AKSI:")
    print("1. Serang dengan Pedang")
    print("2. Minum Ramuan Penyembuh (+30 HP)")
    print("3. Lari dari Pertarungan")
    
    pilihan = input("Tindakanmu (1/2/3): ")
    
    if pilihan == "1":
        damage_pemain = random.randint(serangan_min, serangan_max)
        
        kritis = random.random() < 0.25
        if kritis:
            damage_pemain = damage_pemain * 2
            print("\n*** SERANGAN KRITIS! Damage berlipat ganda! ***")
        
        hp_monster = hp_monster - damage_pemain
        print(f"\nKamu menebas {nama_monster} sebesar {damage_pemain} damage!")
        
    elif pilihan == "2":
        if ramuan > 0:
            hp_pahlawan = hp_pahlawan + 30
            ramuan = ramuan - 1
            print(f"\nKamu meminum ramuan! HP bertambah 30. Sisa ramuan: {ramuan}")
        else:
            print("\nRamuanmu sudah habis! Kamu buang-buang giliran.")
            
    elif pilihan == "3":
        print(f"\n{nama_pahlawan} melarikan diri ketakutan! Pertarungan berakhir.")
        break
    else:
        print("\nPilihan salah! Kamu terpesona dan kehilangan giliran.")

    if hp_monster <= 0:
        print("\n" + "*" * 40)
        print(f"VICTORY! {nama_pahlawan} berhasil mengalahkan {nama_monster}!")
        print("*" * 40)
        break

    time.sleep(1)
    
    damage_monster = random.randint(serangan_monster_min, serangan_monster_max)
    hp_pahlawan = hp_pahlawan - damage_monster
    print(f"{nama_monster} membalas dan menyemburkan api sebesar {damage_monster} damage!")
    
    if hp_pahlawan <= 0:
        print("\n" + "x" * 40)
        print(f"GAME OVER! {nama_pahlawan} telah gugur di dalam gua...")
        print("x" * 40)
        break

    time.sleep(1)