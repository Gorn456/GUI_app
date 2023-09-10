from tkinter import *
from time import time
start = time()

def counter():
    global start
    playtime = 60
    current = playtime - (time() - start)
    label.config(text=f"{round(current, 1)}")
    if current < 0:
        return label.config(text="End!")
    root.after(100, counter)

root = Tk()
label = Label(root)
label.pack()

counter()

root.mainloop()