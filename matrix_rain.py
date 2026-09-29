#!/usr/bin/env python3
"""
Matrix Digital Rain — Efek Hujan Kode ala Film The Matrix (1999)
------------------------------------------------------------------
Karakter acak (termasuk katakana Jepang, sesuai efek asli buatan
Simon Whiteley) jatuh dari atas layar dengan jejak hijau yang
memudar, dan kepala berwarna putih terang di ujung depannya.

Jalankan : python3 matrix_rain.py
Berhenti : tekan Ctrl+C
"""

import os
import random
import shutil
import sys
import time

# Karakter yang dipakai: katakana (ciri khas efek asli) + angka + simbol + huruf
KATAKANA = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
SYMBOLS = "0123456789!@#$%^&*<>/\\|+-=:;"
CHARS = KATAKANA + SYMBOLS + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

RESET = "\033[0m"
HEAD_COLOR = "\033[1;97m"      # putih terang -> karakter paling depan
GREEN_BRIGHT = "\033[38;5;46m"
GREEN_MID = "\033[38;5;34m"
GREEN_DARK = "\033[38;5;22m"


class Column:
    """Satu kolom tetesan hujan kode, dengan posisi kepala & panjang jejak sendiri."""

    def __init__(self, height):
        self.height = height
        self.chars = [random.choice(CHARS) for _ in range(height)]
        self._full_reset()

    def _full_reset(self):
        self.head = random.randint(-self.height, 0)  # posisi awal acak -> tidak serempak
        self.length = random.randint(6, self.height)
        self.speed = random.choice([1, 1, 1, 2])

    def step(self):
        self.head += self.speed
        for _ in range(2):  # sesekali ganti karakter acak -> efek "berkedip"
            i = random.randint(0, self.height - 1)
            self.chars[i] = random.choice(CHARS)
        if self.head - self.length > self.height:
            self._full_reset()

    def color_at(self, row):
        dist = self.head - row
        if dist == 0:
            return HEAD_COLOR
        if 0 < dist <= self.length:
            ratio = dist / self.length
            if ratio <= 0.3:
                return GREEN_BRIGHT
            elif ratio <= 0.6:
                return GREEN_MID
            return GREEN_DARK
        return None  # tidak digambar (kosong)


def render(columns, width, height):
    lines = []
    for row in range(height):
        parts = []
        current = "__none__"
        for col in columns:
            color = col.color_at(row)
            if color != current:
                parts.append(color if color else RESET)
                current = color
            parts.append(col.chars[row] if color else " ")
        parts.append(RESET)
        lines.append("".join(parts))
    return "\n".join(lines)


def get_terminal_size():
    size = shutil.get_terminal_size(fallback=(100, 30))
    return size.columns, max(size.lines - 1, 10)


def main():
    width, height = get_terminal_size()
    columns = [Column(height) for _ in range(width)]

    os.system('cls' if os.name == 'nt' else 'clear')
    sys.stdout.write("\033[?25l")  # sembunyikan kursor
    try:
        while True:
            frame = render(columns, width, height)
            sys.stdout.write("\x1b[H" + frame)
            sys.stdout.flush()
            for col in columns:
                col.step()
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write(RESET + "\033[?25h\n")  # kembalikan warna & kursor
        print("Wake up, Neo... 🐇")


if __name__ == "__main__":
    main()