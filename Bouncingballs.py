import random
import tkinter as tk


class BouncingBalls:

  def __init__(self, root):
    self.root = root
    self.root.title("Simulasi Partikel Membal")
    self.root.geometry("600x500")
    self.root.configure(bg="black")

    self.canvas = tk.Canvas(root, bg="black", highlightthickness=0)
    self.canvas.pack(fill=tk.BOTH, expand=True)

    self.balls = []
    colors = ["cyan", "magenta", "yellow", "lime", "orange", "red", "white"]

    for _ in range(30):
      r = random.randint(10, 20)
      x = random.randint(r, 580 - r)
      y = random.randint(r, 480 - r)
      dx = random.choice([-4, -3, -2, 2, 3, 4])
      dy = random.choice([-4, -3, -2, 2, 3, 4])
      color = random.choice(colors)
      ball = self.canvas.create_oval(
          x - r, y - r, x + r, y + r, fill=color, outline=""
      )
      self.balls.append({"id": ball, "dx": dx, "dy": dy})

    self.animate()

  def animate(self):
    for b in self.balls:
      self.canvas.move(b["id"], b["dx"], b["dy"])
      pos = self.canvas.coords(b["id"])

      if pos[0] <= 0 or pos[2] >= 600:
        b["dx"] = -b["dx"]

      if pos[1] <= 0 or pos[3] >= 500:
        b["dy"] = -b["dy"]

    self.root.after(20, self.animate)


root = tk.Tk()
app = BouncingBalls(root)
root.mainloop()