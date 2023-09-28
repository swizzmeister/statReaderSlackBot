import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from Frames.empty_frame import EmptyFrame


class Db_Add_Event(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    def load_sheet(self, filename: str, sheet):
        """
        :param filename: String name of
        :param sheet:
        """
        if sheet.hasData():
            self.sheet_data = sheet
            self.label.configure(text="Add event, " + filename, foreground="grey")
            self.controller.show_frame(Db_Add_Event)
        else:
            messagebox.showwarning('CSV Error', 'Please open a .csv')
            self.controller.show_frame(EmptyFrame)
