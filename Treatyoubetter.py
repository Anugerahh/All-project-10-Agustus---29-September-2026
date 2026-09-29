import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()

title = "Lyric Popup"

lyrics = [
    ("give", "info"),
    ("give me", "info"),
    ("give me a sign,", "info"),
    ("take my hand,", "error"),
    ("we'll be", "info"),
    ("we'll be fine", "info"),
    ("pro", "info"),
    ("promise", "info"),
    ("i", "error"),
    ("i won't let", "info"),
    ("i won't let you down", "info"),
    ("just", "info"),
    ("just know", "info"),
    ("just know that you", "error"),
    ("just know that you don't", "info"),
    ("just know that you don't have to do", "info"),
    ("this alone", "error"),
    ("pro", "info"),
    ("promise", "info"),
    ("i'll never", "info"),
    ("i'll never let you down", "error"),
]

for text, msg_type in lyrics:
    if msg_type == "info":
        messagebox.showinfo(title, text)
    else:
        messagebox.showerror(title, text)