#!/usr/bin/env python3
"""
Donat 3D Berputar dalam ASCII Art
----------------------------------
Merender sebuah donat (torus) 3D yang berputar secara real-time,
lengkap dengan efek pencahayaan dan z-buffering — semuanya hanya
pakai karakter ASCII di terminal, tanpa library eksternal.

Terinspirasi dari "donut.c" karya Andy Sloane, salah satu potongan
kode paling ikonik dalam budaya programmer.

Jalankan : python3 donut.py
Berhenti : tekan Ctrl+C
"""

import math
import os
import sys
import time

WIDTH = 80
HEIGHT = 22
R1 = 1      # radius tabung (penampang) donat
R2 = 2      # jarak dari pusat donat ke pusat tabung
K2 = 5      # jarak "kamera" ke donat

# Gradasi karakter dari paling gelap ke paling terang, mensimulasikan cahaya
LUMINANCE = ".,-~:;=!*#$@"


def render_frame(A, B):
    """Hitung satu frame donat yang sudah diputar sejauh sudut A (sumbu X) dan B (sumbu Z)."""
    output = [' '] * (WIDTH * HEIGHT)
    zbuffer = [0.0] * (WIDTH * HEIGHT)

    cosA, sinA = math.cos(A), math.sin(A)
    cosB, sinB = math.cos(B), math.sin(B)

    theta = 0.0
    while theta < 2 * math.pi:          # sudut mengelilingi tabung donat
        costheta, sintheta = math.cos(theta), math.sin(theta)
        phi = 0.0
        while phi < 2 * math.pi:        # sudut mengelilingi lubang donat
            cosphi, sinphi = math.cos(phi), math.sin(phi)

            circle_x = R2 + R1 * costheta
            circle_y = R1 * sintheta

            # Rotasi 3D lalu proyeksi perspektif ke layar 2D
            z = sinphi * circle_x * sinA + circle_y * cosA + K2
            ooz = 1 / z  # "one over z", dipakai untuk efek perspektif & z-buffer

            t = sinphi * circle_x * cosA - circle_y * sinA

            xp = int(WIDTH / 2 + 30 * ooz * (cosphi * circle_x * cosB - t * sinB))
            yp = int(HEIGHT / 2 + 15 * ooz * (cosphi * circle_x * sinB + t * cosB))

            # Perkiraan intensitas cahaya pada permukaan di titik ini
            luminance = ((circle_y * sinA - sinphi * costheta * cosA) * cosB
                         - sinphi * costheta * sinA
                         - sintheta * cosA
                         - cosphi * costheta * sinB)

            if 0 <= xp < WIDTH and 0 <= yp < HEIGHT:
                idx = xp + WIDTH * yp
                if ooz > zbuffer[idx]:      # hanya gambar titik terdekat ke kamera
                    zbuffer[idx] = ooz
                    lum_idx = max(0, min(int(luminance * 8), len(LUMINANCE) - 1))
                    output[idx] = LUMINANCE[lum_idx]

            phi += 0.02
        theta += 0.07

    return output


def main():
    A, B = 0.0, 0.0
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        while True:
            frame = render_frame(A, B)
            rows = (''.join(frame[r * WIDTH:(r + 1) * WIDTH]) for r in range(HEIGHT))
            sys.stdout.write("\x1b[H" + '\n'.join(rows) + '\n')
            sys.stdout.flush()

            A += 0.08   # kecepatan putar sumbu X
            B += 0.03   # kecepatan putar sumbu Z
            time.sleep(0.03)
    except KeyboardInterrupt:
        print("\nSampai jumpa! 🍩")


if __name__ == "__main__":
    main()