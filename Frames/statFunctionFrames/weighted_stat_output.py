import tkinter as tk
from tkinter import Listbox, ttk, messagebox, filedialog

from Frames.empty_frame import EmptyFrame
from key_data import KeyData


class WeightedStatOutput(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.sheet_data = object
        self.key_sheet_data = KeyData()
        self.key_name = ""
        self.label = ttk.Label(self, text="Error", font=controller.LARGEFONT)
        self.label.pack(side=tk.TOP)
        # Key Entry
        list_lf = ttk.Labelframe(self, text='Stat Key')
        list_lf.pack()
        self.lbl_key = ttk.Label(list_lf, text="Please enter a key")
        btn_key = ttk.Button(list_lf, text="Get key csv", command=lambda: self.get_key())
        btn_key.grid(column=0, row=0, padx=10, pady=10)
        self.lbl_key.grid(column=1, row=0, padx=10, pady=10)
        # Players to contact
        self.list = []

    def get_key(self):
        path = filedialog.askopenfilename(initialdir='C:\\Users\\Logan\\Desktop',
                                          title="Select a csv Stat File",
                                          filetypes=(("CSV files",
                                                      "*.csv"),
                                                     ("all files",
                                                      "*.*")))
        self.key_sheet_data.load(path)
        self.key_name = path.split('/')[-1]
        self.lbl_key.configure(text="Found key: " + str(self.key_name))

    def load_sheet(self, filename, sheet):
        if sheet.hasData():
            self.sheet_data = sheet
            self.label.configure(text=filename + " weighted output", foreground="grey")
            self.controller.show_frame(WeightedStatOutput)
        else:
            messagebox.showwarning('CSV Error', 'Please open a .csv')
            self.controller.show_frame(EmptyFrame)
