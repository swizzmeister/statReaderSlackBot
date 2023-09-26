import tkinter as tk
from tkinter import Listbox, ttk, messagebox
import mysql.connector
import datetime
import re


class Db_Add_Player(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.tables_saved = []
        self.saved_players = []
        self.saved_var = tk.StringVar(value=self.tables_saved)
        self.label = ttk.Label(self, text="Add Players", font=controller.LARGEFONT)
        self.label.pack(side=tk.TOP)
        # Players List Label Frame*********
        self.list_lf = ttk.Labelframe(self, text='Players Saved')
        self.list_lf.pack(side=tk.BOTTOM, pady=30)
        # remove player button
        rePlayerBtn = ttk.Button(self.list_lf, text="Remove Selected Player", command=lambda: self.remove_selected())
        rePlayerBtn.grid(row=0, column=1, pady=5, sticky='e')
        # export player button
        exportPlayerBtn = ttk.Button(self.list_lf, text="Export All Players to Database",
                                     command=lambda: self.export_to_database())
        exportPlayerBtn.grid(row=0, column=0, pady=5, sticky='e')
        # listbox
        self.list_box = Listbox(self.list_lf, height=6, listvariable=self.tables_saved)
        self.list_box.configure(width=int((controller.winfo_width() / 3) - 8))
        self.list_box.grid(row=1, columnspan=3, column=0,padx=10, pady=10)

        # Player Entry Label Frame**********
        self.lf = ttk.Labelframe(self, text='Player Entry')
        self.lf.pack()
        self.var_name = tk.StringVar()
        # Name label and entry
        namelbl = ttk.Label(self.lf, text="Name:")
        namelbl.grid(row=0, column=0, padx=0, pady=0, sticky='sw')
        self.nameEntry = ttk.Entry(self.lf, textvariable=self.var_name)
        self.nameEntry.grid(row=1, column=0, padx=10, pady=10)
        # Number Label and Entry
        self.var_num = tk.StringVar()
        numlbl = ttk.Label(self.lf, text="Number:")
        numlbl.grid(row=0, column=1, padx=0, pady=0, sticky='sw')
        print(self.nameEntry.winfo_width())
        self.numEntry = ttk.Entry(self.lf, textvariable=self.var_num,
                                  width=int((self.nameEntry.winfo_reqwidth() / 6) / 2))
        self.numEntry.grid(row=1, column=1, padx=10, pady=10)
        # Slack User Name
        self.var_usrname = tk.StringVar()
        usrNamelbl = ttk.Label(self.lf, text="Slack Username:")
        usrNamelbl.grid(row=0, column=2, padx=0, pady=0, sticky='sw')
        self.usrNameEntry = ttk.Entry(self.lf, textvariable=self.var_usrname)
        self.usrNameEntry.grid(row=1, column=2, padx=10, pady=10)
        # Add Player Button
        addPlayerBtn = ttk.Button(self.lf, text="Add Player", command=lambda: self.save_player())
        addPlayerBtn.grid(row=3, column=2, pady=5, padx=10, sticky='ne')

    def save_player(self):
        num = int(self.var_num.get())
        name = self.var_name.get()
        usrName = self.var_usrname.get()
        self.tables_saved.append("" + name + " num:" + str(num) + " " + usrName + "")
        name = name.split(' ')
        self.saved_players.append((num, name[0], name[1], usrName))
        self.saved_var.set(self.tables_saved)
        self.list_box.configure(listvariable=self.saved_var)

    def remove_selected(self):
        self.tables_saved.pop(self.get_selected_index())
        self.saved_players.pop(self.get_selected_index())
        self.saved_var.set(self.tables_saved)
        self.list_box.configure(listvariable=self.saved_var)

    def get_selected_index(self):
        i = 0
        while i < len(self.tables_saved):
            if self.list_box.selection_includes(i):
                return i
            i += 1
        return -1

    def export_to_database(self):
        mydb = mysql.connector.connect(
            host=self.controller.endpoint,
            user='dbmasteruser',
            password='SaltAndPepper14',
            database='dbmaster'
        )
        sql = "INSERT INTO player (num, first_name, last_name, slackUserID) VALUES (%s, %s, %s, %s)"
        cursor = mydb.cursor()
        try:
            for player in self.saved_players:
                out = (player[0], player[1], player[2], player[3])
                print(out)
                cursor.execute(sql, out)
            mydb.commit()
            messagebox.showinfo('Database', 'Table(s) sent successfully!')
        except Exception:
            messagebox.showwarning('Data Error', Exception)


