"""
Kembang Api Interaktif
------------------------
Klik di mana saja pada jendela untuk meluncurkan roket kembang api.
Roket akan naik lalu meledak jadi puluhan partikel warna-warni yang
jatuh perlahan karena gravitasi sambil meredup hingga menghilang.
Kembang api juga akan meluncur otomatis secara berkala.

Jalankan  : python3 fireworks.py
Tutup     : tutup jendelanya, atau tekan Escape
"""

import math
import random
import tkinter as tk


WIDTH = 900
HEIGHT = 600
BACKGROUND = "black"
GRAVITY = 0.05
FRAME_DELAY = 16

PALETTES = [
    ["red", "orange", "yellow"],
    ["cyan", "deepskyblue", "white"],
    ["magenta", "violet", "hotpink"],
    ["lime", "springgreen", "white"],
    ["gold", "orange", "red"],
    ["white", "lightblue", "skyblue"],
    ["yellow", "hotpink", "cyan"],
]


def rgb_color(r, g, b):
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))
    return "rgb:{:02x}/{:02x}/{:02x}".format(r, g, b)


class Particle:
    """
    Satu titik cahaya kecil dengan posisi, kecepatan, warna, dan umur.
    Warnanya meredup menuju hitam seiring waktu sampai akhirnya lenyap.
    """

    def __init__(self, canvas, x, y, vx, vy, color, life, size, gravity_scale=1.0):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.size = size
        self.gravity_scale = gravity_scale
        r, g, b = canvas.winfo_rgb(color)
        self.base_rgb = (r / 256, g / 256, b / 256)
        self.item = canvas.create_oval(x - size, y - size, x + size, y + size,
                                        fill=color, outline="")

    def update(self):
        self.vy += GRAVITY * self.gravity_scale
        self.vx *= 0.995
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

        if self.life <= 0:
            self.canvas.delete(self.item)
            return False

        ratio = self.life / self.max_life
        r, g, b = self.base_rgb
        self.canvas.coords(self.item, self.x - self.size, self.y - self.size,
                            self.x + self.size, self.y + self.size)
        self.canvas.itemconfig(self.item, fill=rgb_color(r * ratio, g * ratio, b * ratio))
        return True


class Rocket:
    """
    Roket yang meluncur ke atas meninggalkan jejak percikan,
    lalu meledak jadi banyak partikel begitu mencapai puncak.
    """

    def __init__(self, canvas, x, target_y, particles):
        self.canvas = canvas
        self.particles = particles
        self.x = x
        self.y = float(HEIGHT)
        self.target_y = target_y
        self.vy = -random.uniform(9, 12)
        self.color = random.choice(["white", "gold", "yellow"])
        self.item = canvas.create_oval(x - 2, self.y - 2, x + 2, self.y + 2,
                                        fill=self.color, outline="")

    def update(self):
        self.particles.append(
            Particle(self.canvas, self.x, self.y,
                     random.uniform(-0.3, 0.3), random.uniform(0.4, 1.2),
                     self.color, 12, 2, gravity_scale=0.2)
        )

        self.y += self.vy
        self.vy += GRAVITY * 0.4
        self.canvas.coords(self.item, self.x - 2, self.y - 2, self.x + 2, self.y + 2)

        if self.y <= self.target_y or self.vy >= -1:
            self._explode()
            return False
        return True

    def _explode(self):
        self.canvas.delete(self.item)
        palette = random.choice(PALETTES)
        count = random.randint(50, 80)
        for i in range(count):
            angle = (2 * math.pi / count) * i + random.uniform(-0.08, 0.08)
            speed = random.uniform(2, 6)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            color = random.choice(palette)
            self.particles.append(
                Particle(self.canvas, self.x, self.y, vx, vy, color,
                         random.randint(45, 65), random.randint(2, 3))
            )


class FireworksApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                                 bg=BACKGROUND, highlightthickness=0)
        self.canvas.pack()
        self.rockets = []
        self.particles = []

        self.canvas.bind("<Button-1>", self.on_click)
        self.root.bind("<Escape>", lambda event: self.root.destroy())

        self.root.after(300, self.auto_launch)
        self.animate()

    def launch(self, x=None):
        if x is None:
            x = random.randint(120, WIDTH - 120)
        target_y = random.randint(int(HEIGHT * 0.2), int(HEIGHT * 0.55))
        self.rockets.append(Rocket(self.canvas, x, target_y, self.particles))

    def on_click(self, event):
        self.launch(event.x)

    def auto_launch(self):
        self.launch()
        delay = random.randint(700, 1500)
        self.root.after(delay, self.auto_launch)

    def animate(self):
        self.rockets[:] = [r for r in self.rockets if r.update()]
        self.particles[:] = [p for p in self.particles if p.update()]
        self.root.after(FRAME_DELAY, self.animate)


def main():
    root = tk.Tk()
    root.title("Kembang Api Python")
    root.resizable(False, False)
    FireworksApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()