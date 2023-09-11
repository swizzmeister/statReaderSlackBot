import re
import tkinter as tk
from tkinter import Listbox, ttk, messagebox


class PlayerComparison(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.reader = controller.get_reader()
        self.controller = controller
        self.cat_c = tk.StringVar()
        self.cat_c.set("Choose Category")
        self.tables_saved = []
        self.query = tk.StringVar()
        self.saved_var = tk.StringVar(value=self.tables_saved)
        self.ltg = tk.BooleanVar()
        self.sum_bool_var = tk.BooleanVar()
        self.avg_bool_var = tk.BooleanVar()
        self.ltg.set("False")
        self.list_box = Listbox(self, height=6, listvariable=self.tables_saved)
        self.list_box.configure(width=int((controller.winfo_width() / 3) - 8))
        self.list_box.grid(column=0, row=4, columnspan=4, pady=3, padx=3)
        self.label = ttk.Label(self, text="CSV", font=self.controller.LARGEFONT)
        self.label.grid(columnspan=4, column=0, row=0, padx=30, pady=10)
        button0 = ttk.Button(self, text="-",
                             command=lambda: self.remove_selected())
        button0.grid(row=3, column=3, padx=10, pady=10)
        self.button1 = ttk.Button(self, text="Show table",
                                  command=lambda: self.show_selected_table())
        self.button1.grid(row=2, column=0, columnspan=2, rowspan=2, padx=10, pady=10)
        button2 = ttk.Button(self,
                             text="+",
                             command=lambda: self.save_table())
        button2.grid(row=2, column=3,columnspan=2, padx=10, pady=10)

        l = ttk.Label(self, text="Add all players where stat:")
        self.key = ttk.Entry(self, textvariable=self.query)
        l.grid(row=1, column=0, padx=10, pady=10)
        self.key.grid(row=1, column=3, columnspan=2, padx=10, pady=10)
        l2 = ttk.Label(self, text="is equal to")
        l2.grid(row=1, column=2, padx=10, pady=10)

    def load_reader(self, filename, reader):
        self.reader = reader
        self.label.configure(text=filename + " Player Comparison", foreground="grey")
        cols = self.reader.getCatagories()
        drop = tk.OptionMenu(self, self.cat_c, *cols)
        drop.grid(column=1, row=1, padx=10, pady=10)
        self.tables_saved = []
        self.saved_var.set(self.tables_saved)
        self.list_box.configure(listvariable=self.saved_var)
        self.controller.show_frame(PlayerComparison)

    def save_table(self):
        players = self.reader.get_Sorted_Leaderboard(self.cat_c.get(), True)
        for player in players:
            print(player[1] == float(self.query.get()))
            if player[1] == float(self.query.get()):
                self.tables_saved.append("Player :" + str(player[0]) + "\t\t Stat : " + str(player[1]))
        self.saved_var.set(self.tables_saved)
        self.list_box.configure(listvariable=self.saved_var)

    def show_selected_table(self):
        if self.get_selected_index() < 0:
            messagebox.showwarning('Slack Client Error', 'Please select a table!')
        else:
            table = self.tables_saved[self.get_selected_index()]
            stats = re.split(r'\[(.*?)\]', table)
            self.controller.data_display_tree(self.reader, stats[1], self.controller.stringBool(stats[3]))

    def remove_selected(self):
        self.tables_saved.pop(self.get_selected_index())
        self.controller.SELECTED.pop(self.get_selected_index())
        self.saved_var.set(self.tables_saved)
        self.list_box.configure(listvariable=self.saved_var)

    def get_selected_index(self):
        i = 0
        while i < len(self.tables_saved):
            if self.list_box.selection_includes(i):
                return i
            i += 1
        return -1
