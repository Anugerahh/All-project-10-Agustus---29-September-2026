import tkinter as tk
import random
import math

class Particle:
    """Kelas untuk mendefinisikan sifat dan pergerakan setiap partikel (bola)."""
    def __init__(self, canvas, x, y, radius, color):
        self.canvas = canvas
        # Menggambar bola di canvas
        self.id = canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color, outline="white", width=2)
        self.x = x
        self.y = y
        self.radius = radius
        # Kecepatan awal acak (vektor X dan Y)
        self.vx = random.uniform(-8, 8)
        self.vy = random.uniform(-8, 8)
        self.mass = radius ** 2 # Massa berbanding lurus dengan luas bola

    def move(self, width, height, gravity=0.3, friction=0.99):
        """Fungsi untuk menggerakkan partikel dengan efek gravitasi dan gesekan."""
        self.vy += gravity  # Efek gravitasi menarik ke bawah
        self.vx *= friction # Gesekan udara melambatkan partikel
        self.vy *= friction

        self.x += self.vx
        self.y += self.vy

        # --- Deteksi Tabrakan dengan Dinding ---
        bounce_loss = -0.85 # Efek pantulan (kehilangan sedikit energi saat menabrak dinding)

        # Dinding Kiri & Kanan
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx *= bounce_loss
        elif self.x + self.radius > width:
            self.x = width - self.radius
            self.vx *= bounce_loss

        # Dinding Atas & Bawah (Lantai)
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy *= bounce_loss
        elif self.y + self.radius > height:
            self.y = height - self.radius
            self.vy *= bounce_loss

        # Memperbarui posisi gambar di layar
        self.canvas.coords(self.id, self.x-self.radius, self.y-self.radius, self.x+self.radius, self.y+self.radius)

class Simulation:
    """Kelas utama untuk menjalankan simulasi dan mengatur canvas."""
    def __init__(self, root, width=900, height=700):
        self.root = root
        self.width = width
        self.height = height
        
        # Membuat layar hitam
        self.canvas = tk.Canvas(root, width=width, height=height, bg="#0d1117", highlightthickness=0)
        self.canvas.pack()
        self.particles = []

        # Deteksi klik mouse untuk menambah partikel baru
        self.canvas.bind("<Button-1>", self.add_particle_event)
        
        # Teks instruksi di layar
        self.canvas.create_text(width//2, 30, text="✨ KLIK LAYAR UNTUK MENAMBAH PARTIKEL ✨", 
                                fill="#ffffff", font=("Helvetica", 14, "bold"))

        # Menambahkan 30 partikel awal secara acak
        for _ in range(30):
            self.add_particle(random.randint(100, width-100), random.randint(100, height-200))

        # Memulai loop animasi
        self.update()

    def add_particle(self, x, y):
        """Membuat partikel baru dengan warna neon acak."""
        neon_colors = ["#FF0055", "#00FF66", "#00DDFF", "#FFDD00", "#B200FF", "#FF6600"]
        radius = random.randint(15, 40)
        color = random.choice(neon_colors)
        self.particles.append(Particle(self.canvas, x, y, radius, color))

    def add_particle_event(self, event):
        """Memicu fungsi add_particle saat mouse diklik."""
        self.add_particle(event.x, event.y)

    def check_collisions(self):
        """Deteksi tabrakan antar partikel menggunakan Teorema Pythagoras."""
        for i in range(len(self.particles)):
            for j in range(i + 1, len(self.particles)):
                p1 = self.particles[i]
                p2 = self.particles[j]
                
                # Menghitung jarak antar dua titik tengah lingkaran
                dx = p1.x - p2.x
                dy = p1.y - p2.y
                distance = math.hypot(dx, dy)
                min_distance = p1.radius + p2.radius

                # Jika jarak lebih kecil dari gabungan radius, berarti mereka bertabrakan!
                if distance < min_distance:
                    # Menghitung sudut tabrakan
                    angle = math.atan2(dy, dx)
                    
                    # Memisahkan partikel agar tidak saling menyatu (overlap)
                    target_x = p2.x + math.cos(angle) * min_distance
                    target_y = p2.y + math.sin(angle) * min_distance
                    
                    # Gaya pantul sederhana
                    ax = (target_x - p1.x) * 0.05
                    ay = (target_y - p1.y) * 0.05

                    p1.vx -= ax
                    p1.vy -= ay
                    p2.vx += ax
                    p2.vy += ay

    def update(self):
        """Fungsi yang dipanggil terus-menerus untuk membuat frame animasi."""
        self.check_collisions()
        for p in self.particles:
            p.move(self.width, self.height)
        
        # Mengulang fungsi update setiap 16 milidetik (~60 Frame Per Second)
        self.root.after(16, self.update)

if __name__ == "__main__":
    # Menginisiasi jendela aplikasi utama
    root = tk.Tk()
    root.title("Simulasi Fisika Partikel Super Keren")
    root.resizable(False, False)
    
    app = Simulation(root)
    
    # Menjalankan aplikasi
    root.mainloop()