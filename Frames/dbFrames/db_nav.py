import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class Db_Nav(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
