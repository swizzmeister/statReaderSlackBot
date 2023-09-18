import re
import tkinter as tk
from tkinter import Listbox, ttk, messagebox


class PlayerComparison(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.reader = controller.get_reader()
        self.PLAYERS = {}
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
        self.list_box = Listbox(self, height=6, listvariable=self.saved_var)
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
        players = self.reader.get_column(self.cat_c.get())
        for num in players.keys():
            player = players.get(num)
            if player == self.query.get():
                self.PLAYERS[num] = self.reader.get_Row(num)
                self.tables_saved.append("Player : " + self.reader.get_Row(num)['Name'] + "\t\tCategory Found: " +
                                         str(self.cat_c.get()))
        self.saved_var.set(self.tables_saved)
        self.list_box.configure(listvariable=self.saved_var)

    def show_selected_table(self):
        if len(self.PLAYERS) < 1:
            messagebox.showwarning('Table Display Error', 'Please add ' + str(2-len(self.PLAYERS)) + " more players")
        else:

            table = self.tables_saved[self.get_selected_index()]
            stats = self.reader.calculable_cols()
            selectedPlayers = list(self.PLAYERS.keys())
            self.controller.player_compare_data_display_tree(stats[1], self.controller.stringBool(stats[3]),
                                              self.controller.stringBool(stats[5]), self.controller.stringBool(stats[7]))

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
