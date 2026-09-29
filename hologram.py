import math
import tkinter as tk

class Hologram3D:
    def __init__(self, root):
        self.root = root
        self.root.title("3D Wireframe Engine - Pure Python")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        self.canvas = tk.Canvas(root, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.vertices = [
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
            [-1, -1,  1], [1, -1,  1], [1, 1,  1], [-1, 1,  1]
        ]

        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]

        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0

        self.animate()

    def animate(self):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width < 10 or height < 10:
            width, height = 800, 600

        cx, cy = width // 2, height // 2
        projected_points = []

        for x, y, z in self.vertices:
            rad_x = math.radians(self.angle_x)
            y1 = y * math.cos(rad_x) - z * math.sin(rad_x)
            z1 = y * math.sin(rad_x) + z * math.cos(rad_x)

            rad_y = math.radians(self.angle_y)
            x2 = x * math.cos(rad_y) + z1 * math.sin(rad_y)
            z2 = -x * math.sin(rad_y) + z1 * math.cos(rad_y)

            distance = 3.5
            fov = 350
            z_eff = z2 + distance
            
            x_screen = int(cx + (x2 * fov) / z_eff)
            y_screen = int(cy + (y1 * fov) / z_eff)

            projected_points.append((x_screen, y_screen))

        for p1, p2 in self.edges:
            x1, y1 = projected_points[p1]
            x2, y2 = projected_points[p2]
            
            self.canvas.create_line(x1, y1, x2, y2, fill="cyan", width=3)
            self.canvas.create_oval(x1-4, y1-4, x1+4, y1+4, fill="magenta", outline="")

        self.angle_x += 1.2
        self.angle_y += 1.8
        self.angle_z += 0.5

        self.root.after(20, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = Hologram3D(root)
    root.mainloop()