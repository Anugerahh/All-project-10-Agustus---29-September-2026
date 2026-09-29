"""
KARYA SENI: THE GRAND BOTANICAL MANDALA
Tema: Flora, Geometri Alam, Biomimikri, dan Fraktal
Skala: Ekstra Detail, Sangat Kompleks

Program ini menggunakan berbagai persamaan parametrik untuk meniru
bentuk organik dari daun, kelopak bunga, sulur merambat, dan serbuk sari.
"""

import colorsys
import math
import random
import turtle

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1200

def setup_window():
    """
    Menginisialisasi jendela utama turtle dan kanvas render.
    Latar belakang diatur ke warna hijau hutan yang sangat gelap (hampir hitam)
    untuk menonjolkan warna bunga yang cerah.
    """
    screen = turtle.Screen()
    screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
    screen.bgcolor((0.02, 0.04, 0.02))
    screen.title("The Grand Botanical Mandala - Ultra Detailed")
    screen.tracer(0)
    return screen

def create_artist():
    """
    Membuat dan mengonfigurasi objek turtle utama untuk menggambar.
    Kecepatan diatur ke maksimum.
    """
    artist = turtle.Turtle()
    artist.hideturtle()
    artist.speed(0)
    artist.pensize(1)
    return artist

def get_floral_color(progress, lightness=0.5, saturation=0.9):
    """
    Menghasilkan palet warna gradien menggunakan model HSL.
    Warna akan berotasi menghasilkan transisi pelangi organik.
    """
    r, g, b = colorsys.hls_to_rgb(progress % 1.0, lightness, saturation)
    return (r, g, b)

def move_to(t, x, y):
    """
    Memindahkan posisi pena tanpa meninggalkan jejak garis.
    """
    t.penup()
    t.goto(x, y)
    t.pendown()

def draw_floating_pollen(t, count=600):
    """
    Menggambar serbuk sari ajaib yang melayang di udara (latar belakang).
    Serbuk sari ini berupa titik-titik kecil bercahaya dengan warna
    kuning, emas, dan hijau muda.
    """
    half_w = SCREEN_WIDTH // 2
    half_h = SCREEN_HEIGHT // 2

    for _ in range(count):
        x = random.randint(-half_w, half_w)
        y = random.randint(-half_h, half_h)
        size = random.uniform(0.5, 3.0)
        
        hue = random.uniform(0.1, 0.3)
        lightness = random.uniform(0.3, 0.8)
        color = get_floral_color(hue, lightness=lightness, saturation=1.0)
        
        move_to(t, x, y)
        t.color(color)
        t.begin_fill()
        t.circle(size)
        t.end_fill()

def draw_perimeter_vines(t, radius, waves=24, amplitude=40):
    """
    Menggambar bingkai sulur merambat yang mengelilingi kanvas.
    Menggunakan gelombang sinusoid untuk menciptakan efek melilit.
    """
    t.pensize(2)
    steps = 720
    
    for i in range(steps + 1):
        angle = math.radians(i * (360 / steps))
        
        wave_offset = amplitude * math.sin(waves * angle)
        current_radius = radius + wave_offset
        
        x = current_radius * math.cos(angle)
        y = current_radius * math.sin(angle)
        
        if i == 0:
            move_to(t, x, y)
        else:
            hue = 0.25 + 0.1 * math.sin(waves * angle)
            t.color(get_floral_color(hue, lightness=0.4, saturation=0.8))
            t.goto(x, y)
            
        if i % 30 == 0:
            draw_small_leaf(t, x, y, math.degrees(angle) + 90, size=15)
            move_to(t, x, y)

def draw_small_leaf(t, x, y, heading, size):
    """
    Menggambar daun kecil tunggal pada koordinat tertentu.
    Digunakan sebagai ornamen pada sulur merambat.
    """
    move_to(t, x, y)
    t.setheading(heading)
    t.color((0.1, 0.6, 0.2))
    t.begin_fill()
    t.circle(size, 60)
    t.left(120)
    t.circle(size, 60)
    t.end_fill()

def draw_fractal_fern(t, length, depth, max_depth, angle):
    """
    Fungsi rekursif untuk menggambar daun pakis (fern).
    """
    if depth == 0:
        return

    pensize = max(1, depth - 2)
    t.pensize(pensize)
    
    green_val = 0.3 + (depth / max_depth) * 0.4
    t.color((0.05, green_val, 0.1))
    
    t.forward(length)
    
    t.left(angle)
    draw_fractal_fern(t, length * 0.6, depth - 1, max_depth, angle)
    
    t.right(angle * 2)
    draw_fractal_fern(t, length * 0.6, depth - 1, max_depth, angle)
    
    t.left(angle)
    
    t.forward(length * 0.3)
    t.left(angle * 1.5)
    draw_fractal_fern(t, length * 0.4, depth - 1, max_depth, angle)
    t.right(angle * 3.0)
    draw_fractal_fern(t, length * 0.4, depth - 1, max_depth, angle)
    t.left(angle * 1.5)
    
    t.backward(length * 1.3)

def generate_background_ferns(t):
    """
    Menempatkan 8 daun pakis raksasa yang menyebar dari pusat
    sebagai latar belakang mandala.
    """
    directions = [0, 45, 90, 135, 180, 225, 270, 315]
    distance_from_center = 80
    
    for angle in directions:
        rad = math.radians(angle)
        x = distance_from_center * math.cos(rad)
        y = distance_from_center * math.sin(rad)
        
        move_to(t, x, y)
        t.setheading(angle)
        draw_fractal_fern(t, length=100, depth=6, max_depth=6, angle=25)

def draw_parametric_chrysanthemum(t, max_radius, petals=36):
    """
    Menggambar bunga krisan raksasa menggunakan persamaan kurva parametrik polar.
    r = a + b * cos(k * theta)
    """
    steps = 1500
    move_to(t, max_radius, 0)
    t.pensize(1)
    
    for i in range(steps + 1):
        theta = i * (2 * math.pi * petals / steps)
        
        radius = max_radius * math.cos(petals * theta / 4)
        
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        
        hue = (i / steps) * 1.0
        t.color(get_floral_color(hue, lightness=0.6, saturation=0.9))
        t.goto(x, y)

def draw_overlapping_lotus_base(t, layers, petals_per_layer):
    """
    Menggambar kelopak besar yang saling tumpang tindih untuk membentuk
    dasar dari bunga teratai (lotus).
    """
    for layer in range(layers, 0, -1):
        radius = layer * 55
        angle_step = 360 / petals_per_layer
        
        for i in range(petals_per_layer):
            angle = i * angle_step + (layer * 15)
            rad = math.radians(angle)
            
            x = radius * math.cos(rad)
            y = radius * math.sin(rad)
            
            move_to(t, x, y)
            t.setheading(angle + 45)
            
            hue = 0.7 + (layer / layers) * 0.3
            t.color(get_floral_color(hue, lightness=0.4, saturation=1.0))
            t.begin_fill()
            t.circle(radius * 0.6, 90)
            t.left(90)
            t.circle(radius * 0.6, 90)
            t.end_fill()
            
            t.color((1.0, 1.0, 1.0))
            t.pensize(1)
            t.circle(radius * 0.6, 90)
            t.left(90)
            t.circle(radius * 0.6, 90)

def draw_spirograph_petals(t, R, r, d, steps, hue_offset):
    """
    Menggunakan rumus Hypotrochoid untuk menciptakan kelopak bunga
    geometris yang sangat presisi di bagian tengah.
    """
    move_to(t, (R - r) + d, 0)
    t.pensize(1)

    for i in range(steps + 1):
        theta = math.radians(i * 1.5)
        x = (R - r) * math.cos(theta) + d * math.cos((R - r) * theta / r)
        y = (R - r) * math.sin(theta) - d * math.sin((R - r) * theta / r)

        hue = hue_offset + (i / steps) * 0.5
        t.color(get_floral_color(hue, lightness=0.7, saturation=0.9))
        t.goto(x, y)

def draw_sharp_dahlia_petals(t, radius, points=24):
    """
    Menggambar kelopak tajam berulang khas bunga dahlia.
    """
    angle_step = 360 / points
    
    for i in range(points):
        start_angle = math.radians(i * angle_step)
        x1 = radius * math.cos(start_angle)
        y1 = radius * math.sin(start_angle)
        
        peak_radius = radius * 1.4
        peak_angle = math.radians((i + 0.5) * angle_step)
        px = peak_radius * math.cos(peak_angle)
        py = peak_radius * math.sin(peak_angle)
        
        end_angle = math.radians((i + 1) * angle_step)
        x2 = radius * math.cos(end_angle)
        y2 = radius * math.sin(end_angle)
        
        move_to(t, x1, y1)
        t.color((0.9, 0.2, 0.4))
        t.begin_fill()
        t.goto(px, py)
        t.goto(x2, y2)
        t.goto(0, 0)
        t.end_fill()
        
        t.color((1.0, 0.6, 0.7))
        t.goto(px, py)

def draw_rose_spiral_core(t, loops=15, max_radius=80):
    """
    Menggambar inti bunga mawar menggunakan kurva spiral Archimedean.
    Menciptakan ilusi kelopak mawar yang menggulung ke dalam.
    """
    steps = 400
    t.pensize(2)
    
    for i in range(steps):
        t_val = i / steps
        current_radius = max_radius * (1 - t_val)
        theta = i * loops * math.pi * 2 / steps
        
        x = current_radius * math.cos(theta)
        y = current_radius * math.sin(theta)
        
        if i == 0:
            move_to(t, x, y)
        else:
            hue = 0.9 + (i / steps) * 0.15
            t.color(get_floral_color(hue, lightness=0.4 + 0.4 * t_val, saturation=0.9))
            t.goto(x, y)

def draw_sunflower_phyllotaxis_seeds(t, count=450, scaling_factor=3.0):
    """
    Menggambar serbuk sari bunga matahari menggunakan Rasio Emas (Golden Ratio).
    Sudut emas = 137.508 derajat.
    Ini menghasilkan pola biji bunga matahari yang sempurna di pusat mandala.
    """
    golden_angle = 137.508

    for i in range(count):
        r_dist = scaling_factor * math.sqrt(i)
        theta = math.radians(i * golden_angle)

        x = r_dist * math.cos(theta)
        y = r_dist * math.sin(theta)

        move_to(t, x, y)

        hue = 0.1 + (i / count) * 0.15
        lightness = 0.3 + (i / count) * 0.5
        t.color(get_floral_color(hue, lightness=lightness, saturation=1.0))

        t.begin_fill()
        t.circle(1.5 + (i / count) * 3.0)
        t.end_fill()

def draw_orbiting_daisies(t, count, orbit_radius):
    """
    Menggambar bunga aster (daisy) kecil yang mengelilingi bunga utama.
    """
    for i in range(count):
        angle = math.radians(i * (360 / count))
        
        cx = orbit_radius * math.cos(angle)
        cy = orbit_radius * math.sin(angle)
        
        for petal in range(12):
            p_angle = math.radians(petal * 30)
            px = cx + 20 * math.cos(p_angle)
            py = cy + 20 * math.sin(p_angle)
            
            move_to(t, cx, cy)
            t.color((0.9, 0.9, 1.0))
            t.begin_fill()
            t.goto(px, py)
            
            np_angle = math.radians((petal + 0.5) * 30)
            npx = cx + 22 * math.cos(np_angle)
            npy = cy + 22 * math.sin(np_angle)
            t.goto(npx, npy)
            t.goto(cx, cy)
            t.end_fill()
            
        move_to(t, cx, cy - 8)
        t.color((1.0, 0.8, 0.0))
        t.begin_fill()
        t.circle(8)
        t.end_fill()

def draw_floral_energy_rays(t, radius, rays=72):
    """
    Menggambar sinar energi (putik/benang sari raksasa) yang memancar dari pusat.
    """
    for i in range(rays):
        angle = math.radians(i * (360 / rays))
        x1 = (radius * 0.3) * math.cos(angle)
        y1 = (radius * 0.3) * math.sin(angle)
        
        x2 = radius * math.cos(angle)
        y2 = radius * math.sin(angle)
        
        move_to(t, x1, y1)
        t.color((1.0, 0.9, 0.5))
        t.pensize(1)
        t.goto(x2, y2)
        
        t.begin_fill()
        t.circle(3)
        t.end_fill()

def main_render_pipeline():
    """
    Fungsi utama yang memanggil seluruh komponen gambar secara berurutan.
    Proses dilakukan dari latar belakang hingga titik pusat terdepan.
    """
    screen = setup_window()
    artist = create_artist()

    print("Memulai Render Latar Belakang Serbuk Sari Kosmik...")
    draw_floating_pollen(artist, count=800)

    print("Menggambar Sulur Merambat Geometris di Tepi...")
    draw_perimeter_vines(artist, radius=480, waves=36, amplitude=25)

    print("Menggambar Fraktal Daun Pakis (Background)...")
    generate_background_ferns(artist)

    print("Menyusun Lapisan Bunga Krisan Raksasa...")
    draw_parametric_chrysanthemum(artist, max_radius=380, petals=48)

    print("Menggambar Bunga Aster Pengorbit...")
    draw_orbiting_daisies(artist, count=16, orbit_radius=410)

    print("Membangun Dasar Kelopak Teratai...")
    draw_overlapping_lotus_base(artist, layers=6, petals_per_layer=16)

    print("Merender Kelopak Tajam Dahlia...")
    draw_sharp_dahlia_petals(artist, radius=220, points=32)

    print("Memancarkan Benang Sari Energi...")
    draw_floral_energy_rays(artist, radius=280, rays=64)

    print("Menambahkan Detail Spirograf Kelopak Dalam...")
    draw_spirograph_petals(artist, R=180, r=55, d=90, steps=800, hue_offset=0.8)
    draw_spirograph_petals(artist, R=120, r=35, d=60, steps=600, hue_offset=0.1)

    print("Menggulung Spiral Mawar di Pusat...")
    draw_rose_spiral_core(artist, loops=12, max_radius=90)

    print("Menanam Biji Bunga Matahari (Pola Emas Phyllotaxis)...")
    draw_sunflower_phyllotaxis_seeds(artist, count=350, scaling_factor=3.5)

    print("Render Super Detail Selesai. Silakan nikmati The Grand Botanical Mandala!")
    screen.update()
    screen.exitonclick()

if __name__ == "__main__":
    main_render_pipeline()