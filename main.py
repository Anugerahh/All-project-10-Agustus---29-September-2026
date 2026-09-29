import tkinter as tk

lyrics_data = [
    (0, "Saying you the one for me"),
    (2000, "I need to face it"),
    (5000, "started when we were younger"),
    (8000, "swear to God that I loved her"),
    (10000, "sorry that your mum found out"),
    (13000, "guess that we just really had the thunder"),
    (15000, "ain't nobody else that I'd be under"),
    (18000, "Beautiful, beautiful life right now"),
    (20000, "beautiful, beautiful night right now"),
    (22000, "no, no, no"),
    (25000, "")
]

def show_lyrics(index):
    if index < len(lyrics_data):
        time_ms, text = lyrics_data[index]
        label.config(text=text)
        
        if index + 1 < len(lyrics_data):
            next_time_ms = lyrics_data[index+1][0]
            delay = next_time_ms - time_ms
            root.after(delay, show_lyrics, index + 1)
        else:
            root.after(2000, root.destroy)

root = tk.Tk()
root.title("Lyric Player - Bazzi (Beautiful)")
root.geometry("700x400")
root.configure(bg="black")

label = tk.Label(
    root, 
    text="Memutar lirik...", 
    font=("Helvetica", 28, "italic"), 
    fg="white", 
    bg="black", 
    justify="center", 
    wraplength=650
)
label.pack(expand=True)

root.after(1000, show_lyrics, 0)
root.mainloop()