import tkinter as tk
import math
import random

# =========================================================
# BLACK HOLE INTERAKTIF
# Tidak membutuhkan modul tambahan
# Hanya tkinter + math + random
# =========================================================

WIDTH = 900
HEIGHT = 700

root = tk.Tk()
root.title("BLACK HOLE - Interactive Mathematics")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.configure(bg="black")

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="black",
    highlightthickness=0
)
canvas.pack(fill="both", expand=True)

# ---------------------------------------------------------
# PARAMETER
# ---------------------------------------------------------

zoom = 45
angle = 0
paused = False

# Schwarzschild radius dalam unit visual
RS = 1.0

# Partikel accretion disk
particles = []

random.seed(10)

for i in range(700):
    r = random.uniform(1.6, 6.5)
    theta = random.uniform(0, math.pi * 2)

    particles.append({
        "r": r,
        "theta": theta,
        "speed": 0.025 / (r ** 1.5),
        "size": random.uniform(1, 3)
    })

# ---------------------------------------------------------
# BINTANG
# ---------------------------------------------------------

stars = []

for i in range(250):
    stars.append((
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.choice([1, 1, 1, 2])
    ))

# ---------------------------------------------------------
# ROTASI 3D SEDERHANA
# ---------------------------------------------------------

def rotate_point(x, y, z, ax):
    """
    Rotasi titik 3D terhadap sumbu Y.
    """

    X = x * math.cos(ax) - z * math.sin(ax)
    Z = x * math.sin(ax) + z * math.cos(ax)

    return X, y, Z


# ---------------------------------------------------------
# PROYEKSI 3D -> 2D
# ---------------------------------------------------------

def project(x, y, z):

    # Perspektif
    distance = 8

    factor = distance / (distance + z)

    sx = WIDTH / 2 + x * zoom * factor
    sy = HEIGHT / 2 - y * zoom * factor

    return sx, sy


# ---------------------------------------------------------
# GAMBAR BLACK HOLE
# ---------------------------------------------------------

def draw_blackhole():

    canvas.delete("all")

    # -----------------------------------------------------
    # BINTANG
    # -----------------------------------------------------

    for x, y, size in stars:

        canvas.create_oval(
            x,
            y,
            x + size,
            y + size,
            fill="white",
            outline=""
        )

    # -----------------------------------------------------
    # ACCRETION DISK
    # -----------------------------------------------------

    for p in particles:

        r = p["r"]
        theta = p["theta"]

        # Bentuk disk
        x = r * math.cos(theta)
        z = r * math.sin(theta)

        # Sedikit kemiringan disk
        y = z * 0.18

        # Rotasi kamera
        X, Y, Z = rotate_point(
            x,
            y,
            z,
            angle
        )

        sx, sy = project(X, Y, Z)

        # Warna berdasarkan jarak
        heat = max(
            0,
            min(
                1,
                (6.5 - r) / 5
            )
        )

        red = 255
        green = int(80 + 150 * heat)
        blue = int(10 + 50 * heat)

        color = f"#{red:02x}{green:02x}{blue:02x}"

        size = p["size"]

        canvas.create_oval(
            sx - size,
            sy - size,
            sx + size,
            sy + size,
            fill=color,
            outline=""
        )

    # -----------------------------------------------------
    # PHOTON SPHERE
    # r = 1.5 Rs
    # -----------------------------------------------------

    photon_radius = 1.5 * zoom

    canvas.create_oval(
        WIDTH / 2 - photon_radius,
        HEIGHT / 2 - photon_radius * 0.35,
        WIDTH / 2 + photon_radius,
        HEIGHT / 2 + photon_radius * 0.35,
        outline="#ffcc44",
        width=2
    )

    # -----------------------------------------------------
    # EVENT HORIZON
    # r = Rs
    # -----------------------------------------------------

    horizon = RS * zoom

    canvas.create_oval(
        WIDTH / 2 - horizon,
        HEIGHT / 2 - horizon * 0.35,
        WIDTH / 2 + horizon,
        HEIGHT / 2 + horizon * 0.35,
        fill="black",
        outline="#ff5500",
        width=3
    )

    # -----------------------------------------------------
    # TENGAH BLACK HOLE
    # -----------------------------------------------------

    canvas.create_oval(
        WIDTH / 2 - horizon * 0.75,
        HEIGHT / 2 - horizon * 0.26,
        WIDTH / 2 + horizon * 0.75,
        HEIGHT / 2 + horizon * 0.26,
        fill="black",
        outline=""
    )

    # -----------------------------------------------------
    # TEKS MATEMATIKA
    # -----------------------------------------------------

    canvas.create_text(
        20,
        20,
        anchor="nw",
        fill="white",
        font=("Arial", 14),
        text="BLACK HOLE"
    )

    canvas.create_text(
        20,
        50,
        anchor="nw",
        fill="#aaaaaa",
        font=("Arial", 11),
        text="Schwarzschild radius:  Rs = 2GM/c²"
    )

    canvas.create_text(
        20,
        72,
        anchor="nw",
        fill="#aaaaaa",
        font=("Arial", 11),
        text="Photon sphere:  R = 1.5 Rs"
    )

    canvas.create_text(
        WIDTH - 20,
        HEIGHT - 25,
        anchor="se",
        fill="#aaaaaa",
        font=("Arial", 10),
        text="Drag mouse = rotate   |   Scroll = zoom   |   SPACE = pause"
    )


# ---------------------------------------------------------
# ANIMASI
# ---------------------------------------------------------

def animate():

    global angle

    if not paused:

        angle += 0.015

        for p in particles:
            p["theta"] += p["speed"] * 5

    draw_blackhole()

    root.after(16, animate)


# ---------------------------------------------------------
# MOUSE DRAG
# ---------------------------------------------------------

last_x = None

def mouse_down(event):

    global last_x

    last_x = event.x


def mouse_drag(event):

    global angle, last_x

    if last_x is not None:

        difference = event.x - last_x

        angle += difference * 0.01

        last_x = event.x


canvas.bind("<Button-1>", mouse_down)
canvas.bind("<B1-Motion>", mouse_drag)


# ---------------------------------------------------------
# ZOOM
# ---------------------------------------------------------

def zoom_in(event):
    global zoom
    zoom *= 1.1


def zoom_out(event):
    global zoom
    zoom /= 1.1


canvas.bind("<MouseWheel>", zoom_in)

# Linux
canvas.bind("<Button-4>", zoom_in)
canvas.bind("<Button-5>", zoom_out)


# ---------------------------------------------------------
# PAUSE
# ---------------------------------------------------------

def toggle_pause(event):

    global paused
    paused = not paused


root.bind("<space>", toggle_pause)


# ---------------------------------------------------------
# MULAI
# ---------------------------------------------------------

animate()

root.mainloop()