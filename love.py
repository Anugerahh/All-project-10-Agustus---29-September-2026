import turtle
import math
import time

layar = turtle.Screen()
layar.bgcolor("black")
layar.title("Animasi Hati Cepat Berdenyut")
layar.setup(width=800, height=800)
layar.tracer(0)

pen = turtle.Turtle()
pen.hideturtle()

def koordinat_hati(t):
    x = 16 * (math.sin(t) ** 3)
    y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
    return x, y

warna = [
    "crimson", "deeppink", "magenta", 
    "mediumvioletred", "hotpink", "purple", 
    "gold", "orchid", "darkorange", "white"
]

for frame in range(120):
    pen.clear()
    faktor_ukuran = 1 + 0.06 * math.sin(frame * 0.25)
    
    for layer in range(75, 0, -1):
        skala = layer * 0.26 * faktor_ukuran
        pen.pencolor(warna[(layer + frame) % len(warna)])
        pen.width(2)
        
        pen.penup()
        x0, y0 = koordinat_hati(0)
        pen.goto(x0 * skala, y0 * skala)
        pen.pendown()
        
        i = 0
        while i <= 6.28:
            x, y = koordinat_hati(i)
            pen.goto(x * skala, y * skala)
            i += 0.08
            
    pen.penup()
    
    pen.goto(-3, -23)
    pen.color("cyan")
    pen.write("i love you", align="center", font=("Arial", 42, "bold"))
    
    pen.goto(3, -17)
    pen.color("deeppink")
    pen.write("i love you", align="center", font=("Arial", 42, "bold"))
    
    pen.goto(0, -20)
    pen.color("white")
    pen.write("i love you", align="center", font=("Arial", 42, "bold"))
    
    layar.update()
    time.sleep(0.01)

turtle.done()