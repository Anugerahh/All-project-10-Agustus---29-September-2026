import turtle

layar = turtle.Screen()
layar.bgcolor("black")
layar.title("Pola Bintang Optik")

p = turtle.Turtle()
p.speed(0)
p.hideturtle()
p.width(2)

warna = ["cyan", "magenta", "yellow", "lime", "orange", "red", "violet", "white"]

for x in range(210):
    p.color(warna[x % len(warna)])
    p.forward(x * 2)
    p.left(137)

turtle.done()