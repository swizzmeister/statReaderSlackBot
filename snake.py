import tkinter as tk
from tkinter import ttk
import PIL as p

class Snake(tk.Tk):

    def __init__(self,*args,**kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        self.snakeBits = [p.Image.open("snackBits/s_background.png", p.Image.open("snackBits/s_food.png"), p.Image.open("snackBits/s_body.png"), p.Image.open("snackBits/s_head.png"))]
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        image = p.ImageTk.PhotoImage(self.snakeBits[1])
        for x in range(0, 20):
            for y in range(0, 20):
                label = ttk.Label(image=image)
                label.image = image
                label.place(x,y)

s = Snake()
s.mainloop()
