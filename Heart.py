import turtle
import time

jendela = turtle.Screen()
jendela.title("Animasi Detak Jantung")
jendela.bgcolor("black")
jendela.setup(width=600, height=600)

pena = turtle.Turtle()
pena.color("red")
pena.speed(0)
pena.width(3)
pena.hideturtle()

def gambar_setengah_hati(arah):
    if arah == "kiri":
        for i in range(200):
            pena.right(1)
            pena.forward(1)
    elif arah == "kanan":
        for i in range(200):
            pena.right(1)
            pena.forward(1)

def gambar_hati(ukuran):
    pena.penup()
    pena.goto(0, - ukuran / 2)
    pena.pendown()
    pena.begin_fill()
    pena.left(140)
    pena.forward(ukuran)
    gambar_setengah_hati("kiri")
    pena.left(120)
    gambar_setengah_hati("kanan")
    pena.forward(ukuran)
    pena.end_fill()
    pena.setheading(0)

print("\nJendela gambar sedang dibuka...")
print("Animasi akan dimulai dalam 3 detik...")
time.sleep(3)
print("Memulai animasi...")

pola_denyut = [100, 110, 100, 100, 110, 100, 100, 100, 110, 100]

for denyut in pola_denyut:
    pena.clear()
    
    gambar_hati(denyut)
    
    pena.penup()
    pena.goto(0, -10)
    pena.color("white")
    pena.write("CINTA UNTUKMU", align="center", font=("Courier", 16, "bold"))
    pena.color("red")
    pena.pendown()

    jendela.update()
    
    if denyut == 110:
        time.sleep(0.1)
    else:
        time.sleep(0.3)

print("Animasi selesai. Klik pada jendela gambar untuk menutup.")
turtle.exitonclick()