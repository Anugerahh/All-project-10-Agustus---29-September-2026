import turtle
import colorsys

window = turtle.Screen()
window.bgcolor("black")

pen = turtle.Turtle()
pen.speed(0)

for i in range(180):
    rgb = colorsys.hsv_to_rgb(i / 180, 1, 1)
    pen.color(rgb)
    pen.forward(i * 2)
    pen.left(119)

turtle.done()