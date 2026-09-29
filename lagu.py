import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()  

title = "Flatline - Justin Bieber"

lyrics = [
    ("Lately, you've been busy", "info"),
    ("Wondering if you miss me", "info"),
    ("Why did you go against me?", "info"),
    ("I just wanna know", "info"),
    ("How come you act so different?", "info"),
    ("Talk to me, I'll listen", "info"),
    ("All the love I'm giving", "info"),
    ("Don't act like you don't know", "error"),
    ("I was out there on the road", "info"),
    ("Life out of control", "info"),
    ("She became a victim", "info"),
    ("To my busy schedule, but", "info"),
    ("And I know that it's not fair", "error"),
    ("That don't mean", "error"),
    ("That I don't care", "error"),
    ("This one's dedicated", "info"),
    ("To the girl out there.", "info"),
]

for text, msg_type in lyrics:
    if msg_type == "info":
        messagebox.showinfo(title, text)
    else:
        messagebox.showerror(title, text)