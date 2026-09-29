import turtle
import math
import colorsys

layar = turtle.Screen()
layar.setup(width=900, height=900)
layar.title("Mahakarya Geometri Kosmik")
turtle.colormode(255)
layar.bgcolor(0, 0, 0)
layar.tracer(15) 

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()
pen.pensize(1)

def ambil_warna(sudut, putaran):
    hue = (sudut / 360.0) + (putaran / 10.0)
    hue = hue - int(hue)
    r, g, b = colorsys.hsv_to_rgb(hue, 0.95, 1.0)
    return int(r * 255), int(g * 255), int(b * 255)

print("Memulai Fase 1: Merajut Jaring Fraktal Luar...")
for putaran in range(8):
    radius_utama = 400 - (putaran * 45)
    for sudut in range(0, 360, 2):
        pen.penup()
        pen.goto(0, 0)
        pen.setheading(sudut + (putaran * 12))
        pen.forward(radius_utama)
        pen.pendown()
        
        pen.pencolor(ambil_warna(sudut, putaran))
        
        for langkah in range(3):
            pen.right(110 + (putaran * 3))
            pen.forward(radius_utama * 0.7)
            pen.right(120)
            pen.forward(radius_utama * 0.35)

print("Memulai Fase 2: Membentuk Kurva Mawar Kuantum...")
for sudut_bunga in range(1440):
    pen.penup()
    pen.goto(0, 0)
    pen.setheading(sudut_bunga / 4.0)
    pen.pendown()
    
    warna_bunga = ambil_warna(sudut_bunga, 12)
    pen.pencolor(warna_bunga)
    
    rumus_matematika = sudut_bunga * 7 * math.pi / 180
    panjang = 280 * math.sin(rumus_matematika)
    
    if panjang < 0:
        panjang = panjang * -1
        
    pen.forward(panjang)
    pen.left(90)
    pen.circle(panjang * 0.15, 180)
    pen.left(90)
    pen.forward(panjang)

print("Memulai Fase 3: Menyusun Inti Bintang Golden Ratio...")
pen.penup()
for titik in range(2500):
    sudut_emas = titik * 137.508
    radius_emas = math.sqrt(titik) * 4.5
    
    x = radius_emas * math.cos(sudut_emas * math.pi / 180)
    y = radius_emas * math.sin(sudut_emas * math.pi / 180)
    
    pen.goto(x, y)
    pen.pendown()
    
    warna_inti = ambil_warna(titik, 20)
    pen.pencolor(warna_inti)
    
    pen.dot(max(1, 6 - (titik / 500)))
    pen.penup()

print("Selesai! Mahakarya Kosmik telah tercipta.")
layar.update()
turtle.done()