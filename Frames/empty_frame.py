import tkinter as tk
from tkinter import ttk


class EmptyFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(master=self, text="No Available CSV", font=('Helvetica', 24))
        label.configure(foreground="grey")
        label.place(relx=0.5, rely=0.5, anchor='center')
