import re
import tkinter as tk
from tkinter import Listbox, ttk, messagebox


class PlayerComparison(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.equalities = ['is equal to', 'is greater or equal to', 'is less or equal to', 'is less then', 'is greater then',  'is not']
        self.pOptions = ['Add', 'Remove']
        self.var_pOptions = tk.StringVar()
        self.var_equalities = tk.StringVar()
        self.var_pOptions.set(self.pOptions[0])
        self.var_equalities.set(self.equalities[0])
        self.SHEET = controller.get_sheet_data()
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
        self.list_box.configure(width=int(controller.winfo_width()/3))
        self.list_box.grid(column=0, row=5, columnspan=3, pady=3, padx=3)
        self.label = ttk.Label(self, text="CSV", font=self.controller.LARGEFONT)
        self.label.grid(columnspan=6, column=0, row=0, padx=30, pady=10)
        #button0 = ttk.Button(self, text="-",
                             #command=lambda: self.remove_selected())
        #button0.grid(row=3, column=3, padx=10, pady=10)
        self.button1 = ttk.Button(self, text="Show table",
                                  command=lambda: self.show_selected_table())
        self.button1.grid(row=3, column=2, padx=10, pady=10)
        button2 = ttk.Button(self,
                             text="Ok",
                             command=lambda: self.queryPlayers())
        button2.grid(row=2, column=2, padx=5, pady=10)
        dropChoice = tk.OptionMenu(self, self.var_pOptions, *self.pOptions)
        dropChoice.grid(row=1,column=0,pady=10, padx=5)
        l = ttk.Label(self, text="all players where stat:")
        self.key = ttk.Entry(self, textvariable=self.query)
        l.grid(row=1, column=1, padx=5, pady=10)
        self.key.grid(row=2, column=1, padx=5, pady=10)
        eDrop = tk.OptionMenu(self, self.var_equalities, *self.equalities)
        eDrop.grid(row=2, column=0, padx=5, pady=10)

    def load_sheet(self, filename, sheet):
        self.SHEET = sheet
        self.label.configure(text=filename + " Player Comparison", foreground="grey")
        cols = self.SHEET.cols
        drop = tk.OptionMenu(self, self.cat_c, *cols)
        drop.grid(column=2, row=1, padx=5, pady=10)
        self.tables_saved = []
        self.saved_var.set(self.tables_saved)
        self.list_box.configure(listvariable=self.saved_var)
        self.controller.show_frame(PlayerComparison)

    def queryPlayers(self):
        players = self.SHEET.get_col_data(self.cat_c.get())
        if self.var_pOptions.get()=='Add':
            players_to_add = []
            for num in players.keys():
                player = players.get(num)
                if player != '-':
                    match self.var_equalities.get():
                        case 'is equal to':
                            if player == self.query.get():
                                players_to_add.append(num)
                        case 'is greater or equal to':
                            if float(player) >= float(self.query.get()):
                                players_to_add.append(num)
                        case float('is less or equal to'):
                            if float(player) <= float(self.query.get()):
                                players_to_add.append(num)
                        case 'is less then':
                            if float(player) < float(self.query.get()):
                                players_to_add.append(num)
                        case 'is greater then':
                            if float(player) > float(self.query.get()):
                                players_to_add.append(num)
                        case 'is not':
                            if player != self.query.get():
                                players_to_add.append(num)
            for num in players_to_add:
                if num not in self.PLAYERS.keys():
                    self.PLAYERS[num] = self.SHEET.getPlayer(num).get_stats(self.SHEET.cols)
                    self.tables_saved.append("Player : " + self.SHEET.getPlayer(num).get_stats('Name'))
            self.saved_var.set(self.tables_saved)
            self.list_box.configure(listvariable=self.saved_var)
        elif self.var_pOptions.get()=='Remove':
            players_to_remove = []
            for num in self.PLAYERS.keys():
                player = players.get(num)
                if player != '-':
                    match self.var_equalities.get():
                        case 'is equal to':
                            if player == self.query.get():
                                players_to_remove.append(num)
                        case 'is greater or equal to':
                            if float(player) >= float(self.query.get()):
                                players_to_remove.append(num)
                        case 'is less or equal to':
                            if float(player) <= float(self.query.get()):
                                players_to_remove.append(num)
                        case 'is less then':
                            if float(player) < float(self.query.get()):
                                players_to_remove.append(num)
                        case 'is greater then':
                            if float(player) < float(self.query.get()):
                                players_to_remove.append(num)
                        case 'is not':
                            if player != self.query.get():
                                players_to_remove.append(num)
                else:
                    players_to_remove.append(num)
            for player in players_to_remove:
                print(self.tables_saved)
                self.tables_saved.pop(
                    self.tables_saved.index('Player : ' + self.SHEET.getPlayer(player).get_stats('Name')))
                self.PLAYERS.pop(player)
            self.saved_var.set(self.tables_saved)
            self.list_box.configure(listvariable=self.saved_var)
    def show_selected_table(self):
        if len(self.PLAYERS) < 1:
            messagebox.showwarning('Table Display Error', 'Please add ' + str(2-len(self.PLAYERS)) + " more players")
        else:

            table = self.tables_saved[self.get_selected_index()]
            stats = self.SHEET.get_calc_Cols()
            selectedPlayers = list(self.PLAYERS.keys())
            self.controller.player_compare_data_display_tree(stats, selectedPlayers)


    def get_selected_index(self):
        i = 0
        while i < len(self.tables_saved):
            if self.list_box.selection_includes(i):
                return i
            i += 1
        return -1
