import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class Snake(tk.Tk):

    def __init__(self, *args, **kwargs):
        self.running = True
        self.height = 20
        self.width = 20
        startingPos = [10, 10]
        self.snake = [startingPos]
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        self.snakeBits = [Image.open("snackBits/s_background.png"), Image.open("snackBits/s_food.png"),
                          Image.open("snackBits/s_body.png"), Image.open("snackBits/s_head.png")]
        container = tk.Frame(self, width=self.width * 10, height=self.height * 10)
        container.pack(side="top", fill="both", expand=True)
        image = ImageTk.PhotoImage(self.snakeBits[0])
        self.labels = []
        for x in range(0, 20):
            lbls = []
            for y in range(0, 20):
                label = ttk.Label(image=image)
                label.image = image
                label.place(x=x * 10, y=y * 10)
                lbls.append(label)
            self.labels.append(lbls)
        self.snake = snakeBody(self.labels, self, 10, 10)

    def startGame(self):
        self.mainloop()
        dir = -2
        while self.running:
            self.snake.travel(self.labels)
    def getLabel(self,x,y):
        return self.labels[x][y]
    def get_images(self):
        return self.snakeBits
    def get_label_map(self):
        return self.labels


def get_behind_direction_location(dir,x,y):
    new_coord=[x,y]
    if dir == 1 or dir == -1:
        new_coord[0] = new_coord[0] + (dir * -1)
    elif dir == 2:
        new_coord[1] = new_coord[1] + 1
    else:
        new_coord[1] = new_coord[1] - 1
    return new_coord
def get_infront_direction_location(dir,x,y)
    new_coord = [x, y]
    if dir == 1 or dir == -1:
        new_coord[0] = new_coord[0] + dir
    elif dir == 2:
        new_coord[1] = new_coord[1] - 1
    else:
        new_coord[1] = new_coord[1] + 1
    return new_coord
class snakeBody():
    def __init__(self, map, frame, x,y):
        next_lbl_coords = get_infront_direction_location(-2,x,y)
        self.head = snakePart(True, frame, map[x][y], -2, x, y, map[next_lbl_coords[0]][next_lbl_coords[1]])
        self.frame = frame
        self.map = map
    def travel(self,labels):
        self.head.travel(labels)
    def get_length(self):
        s_bit = self.head
        length = 1
        while s_bit.hasNext():
            length += 1
            s_bit = s_bit.next
        return length
    def get_last(self):
        s_bit = self.head
        length = 1
        while s_bit.hasNext():
            s_bit = s_bit.next
        return s_bit
    def add_Bit(self):
        s_bit = self.get_last()
        dir = s_bit.dir
        if dir == 1 or dir == -1:
            x = s_bit.x + (dir*-1)
            y = s_bit.y
        elif dir == 2:
            x = s_bit.x
            y = s_bit.y+1
        else:
            x = s_bit.x
            y = s_bit.y - 1
        s_bit.next = snakePart(False, self.frame, self.map[x][y], s_bit.dir,x,y,s_bit.label)

class snakePart():
    def __init__(self, isHead, frame, label, dir,x, y, nextLabel):
        self.next = None
        self.nextLabel = nextLabel
        self.dir = dir
        self.isHead = isHead
        self.label = label
        self.frame = frame
        self.updatePart(dir)
        self.x=x
        self.y=y
    def kill(self,x,y,label):
        image = Image.open("snackBits/s_background.png")
        image = ImageTk.PhotoImage(image)
        label.configure(image=image)

    def travel(self,labels):
        new_coords = get_infront_direction_location(self.dir,self.x,self.y)
        oldx = self.x
        oldy = self.y
        self.x = new_coords[0]
        self.y = new_coords[1]
        new_next = get_infront_direction_location(self.dir,self.x,self.y)
        labelTemp = self.label
        self.label = self.nextlabel
        self.nextLabel = labels[new_next[0],new_next[1]]
        self.updatePart(self.dir)
        if not self.hasNext():
            self.kill(oldy,oldx,labelTemp)
        else:
            self.next.travel(labels)

    def hasNext(self):
        return type(self.next) is not None

    def setNext(self, next):
        self.next = next

    def getNext(self):
        return self.next

    def setDir(self, dir,newLabel):
        if dir is not self.dir:
            self.dir = dir
            self.nextLabel = newLabel


    def updatePart(self, dir):
        if self.isHead:
            image = Image.open("snackBits/s_head.png")
        else:
            image = Image.open("snackBits/s_body.png")
        if dir == 1:
            image = image.rotate(90)
        elif dir == 2:
            image = image.rotate(180)
        elif dir == -1:
            image = image.rotate(270)
        image = ImageTk.PhotoImage(image)
        self.label.configure(image=image)
        self.label.image = image


s = Snake()
s.startGame()
