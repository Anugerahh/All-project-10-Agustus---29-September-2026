import time
import tkinter as tk


def update_time():
  current_time = time.strftime("%H:%M:%S")
  clock_label.config(text=current_time)
  clock_label.after(1000, update_time)


root = tk.Tk()
root.title("Jam Digital")
root.geometry("350x150")
root.configure(bg="black")

clock_label = tk.Label(
    root, font=("Consolas", 48, "bold"), background="black", foreground="lime"
)
clock_label.pack(anchor="center", expand=True)

update_time()

root.mainloop()    