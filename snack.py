import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from time import sleep


class Snack(tk.Tk):

    def __init__(self, *args, **kwargs):
        self.running = True
        self.height = 20
        self.width = 20
        startingPos = [10, 10]
        self.snake = [startingPos]
        self.direction = [1, 0]
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        self.snakeBits = [Image.open("snackBits/s_background.png"), Image.open("snackBits/s_food.png"),
                          Image.open("snackBits/s_body.png"), Image.open("snackBits/s_head.png")]
        container = tk.Frame(self, width=self.width * 10, height=self.height * 10)
        container.pack(side="top", fill="both", expand=True)
        image = ImageTk.PhotoImage(self.snakeBits[0])
        self.labels = []
        for x in range(0, self.height):
            lbls = []
            for y in range(0, self.width):
                label = ttk.Label(image=image)
                label.image = image
                label.place(x=x * 10, y=y * 10)
                lbls.append(label)
            self.labels.append(lbls)
        self.draw_snack()


    def draw_background(self):
        image = ImageTk.PhotoImage(self.snakeBits[0])
        for x in range(0, self.height):
             for y in range(0, self.width):
                self.labels[x][y].configure(image=image)
                self.labels[x][y].image = image
    def draw_snack(self):
        c = 0
        direction = self.direction
        for bit in self.snake:

            if c == 0:
                image = Image.open("snackBits/s_head.png")
            else:
                image = Image.open("snackBits/s_body.png")
            if direction[1] == 1:
                image = image.rotate(90)
            elif direction[0] == -1:
                image = image.rotate(180)
            elif direction[1] == -1:
                image = image.rotate(270)
            if c+1<len(self.snake):
                direction[0] = bit[0] - self.snake[c + 1][0]
                direction[1] = bit[1] - self.snake[c + 1][1]
            image = ImageTk.PhotoImage(image=image)
            self.labels[bit[0]][bit[1]].configure(image=image)
            self.labels[bit[0]][bit[1]].image = image

    def moveSnake(self):
        for snk in self.snake:
            snk[0] += self.direction[0]
            snk[1] += self.direction[1]
    def start(self):
        while True:
            self.moveSnake()
            self.draw_background()
            self.draw_snack()
            sleep(0.75)

s = Snack()
s.mainloop()
s.start()