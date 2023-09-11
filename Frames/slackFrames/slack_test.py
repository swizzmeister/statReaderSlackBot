import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk


class SlackTest(tk.Frame):

    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        if root.ACTIVE:
            if root.CLIENT.api_test()['ok'] and root.CLIENT.auth_test()['ok']:
                image = Image.open('img/connected.png')
                text = "Connected"
            else:
                image = Image.open('img/disconnected.png')
                text = "Disconnected"
        else:
            image = Image.open('img/disconnected.png')
            text = "Disconnected"

        image_tk = ImageTk.PhotoImage(master=self, image=image)
        label = ttk.Label(self, image=image_tk)
        label.image = image_tk
        label.grid(row=0, column=0, pady=10, padx=20)
        label1 = ttk.Label(self, text=text)
        label1.grid(row=0, column=2, pady=10, padx=20)
