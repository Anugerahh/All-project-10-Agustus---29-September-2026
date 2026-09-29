import random
import math
import time
import os

# Ukuran terminal
WIDTH = 80
HEIGHT = 24

# Jumlah bintang
STAR_COUNT = 180

# Posisi bintang
stars = []

for _ in range(STAR_COUNT):
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)
    z = random.uniform(0.1, 1)

    stars.append([x, y, z])


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def draw():
    screen = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for star in stars:
        x, y, z = star

        # Proyeksi 3D ke 2D
        scale = 1 / z

        sx = int(WIDTH / 2 + x * scale * WIDTH / 2)
        sy = int(HEIGHT / 2 + y * scale * HEIGHT / 2)

        if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:

            # Semakin dekat -> semakin terang/besar
            if z < 0.15:
                char = "@"
            elif z < 0.3:
                char = "O"
            elif z < 0.5:
                char = "*"
            elif z < 0.7:
                char = "."
            else:
                char = "."

            screen[sy][sx] = char

    # Tambahkan pusat wormhole
    cx = WIDTH // 2
    cy = HEIGHT // 2

    if 0 <= cy < HEIGHT and 0 <= cx < WIDTH:
        screen[cy][cx] = "X"

    print("\n".join("".join(row) for row in screen))


print("STAR TUNNEL 3D")
print("Tekan CTRL+C untuk keluar...")
time.sleep(2)

try:
    while True:

        # Gerakkan bintang menuju kita
        for star in stars:
            star[2] -= 0.025

            # Kalau sudah terlalu dekat, muncul lagi dari jauh
            if star[2] <= 0.03:
                star[0] = random.uniform(-1, 1)
                star[1] = random.uniform(-1, 1)
                star[2] = 1

        clear_screen()
        draw()

        time.sleep(0.03)

except KeyboardInterrupt:
    clear_screen()
    print("🚀 Kamu keluar dari Star Tunnel.")