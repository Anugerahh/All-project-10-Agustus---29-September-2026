import math
import random
import tkinter as tk


class WarpSpeed:

  def __init__(self, root):
    self.root = root
    self.root.title("Simulasi Hyperspace Warp Speed")
    self.width = 800
    self.height = 600
    self.root.geometry(f"{self.width}x{self.height}")
    self.root.configure(bg="black")

    self.canvas = tk.Canvas(root, bg="black", highlightthickness=0)
    self.canvas.pack(fill=tk.BOTH, expand=True)

    self.cx = self.width // 2
    self.cy = self.height // 2
    self.stars = [self.reset_star() for _ in range(200)]

    self.animate()

  def reset_star(self):
    angle = random.uniform(0, 2 * math.pi)
    speed = random.uniform(1, 3)
    dist = random.uniform(5, 30)
    return {
        "angle": angle,
        "speed": speed,
        "dist": dist,
        "x": self.cx + math.cos(angle) * dist,
        "y": self.cy + math.sin(angle) * dist,
    }

  def animate(self):
    self.canvas.delete("all")

    for star in self.stars:
      star["dist"] += star["speed"]
      star["speed"] *= 1.08

      tail_x = self.cx + math.cos(star["angle"]) * (
          star["dist"] - star["speed"] * 1.5
      )
      tail_y = self.cy + math.sin(star["angle"]) * (
          star["dist"] - star["speed"] * 1.5
      )

      head_x = self.cx + math.cos(star["angle"]) * star["dist"]
      head_y = self.cy + math.sin(star["angle"]) * star["dist"]

      size = max(1, int(star["dist"] / 60))

      self.canvas.create_line(
          tail_x, tail_y, head_x, head_y, fill="#00FFFF", width=size
      )

      if (
          head_x < 0
          or head_x > self.width
          or head_y < 0
          or head_y > self.height
      ):
        star.update(self.reset_star())

    self.root.after(16, self.animate)


root = tk.Tk()
app = WarpSpeed(root)
root.mainloop()