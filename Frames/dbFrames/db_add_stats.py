import tkinter as tk
import datetime
from tkinter import filedialog, messagebox
from tkinter import ttk

import mysql

from Frames.empty_frame import EmptyFrame
from key_data import KeyData


class Db_Add_Stats(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.key_sheet_data = KeyData()
        self.mydb = mysql.connector.connect(
            host=self.controller.endpoint,
            user='dbmasteruser',
            password='SaltAndPepper14',
            database='dbmaster'
        )
        self.db_cursor = self.mydb.cursor()
        self.sheet_data = controller.get_sheet_data()
        self.date = "YYYY/MM/DD"
        self.label = ttk.Label(self, text="", font=self.controller.LARGEFONT)
        event_set = ttk.Labelframe(self, text='Set Event')
        self.label.pack(side=tk.TOP)
        event_set.pack(pady=50)
        self.lbl_key = ttk.Label(event_set, text="Please enter a key")
        btn_key = ttk.Button(event_set, text="Get key csv", command=lambda: self.get_key())
        btn_key.grid(column=0, row=0, padx=10, pady=10)
        self.lbl_key.grid(column=1, row=0, padx=10, pady=10)


    def get_key(self):
        path = filedialog.askopenfilename(initialdir='C:\\Users\\Logan\\Downloads',
                                          title="Select a csv Stat File",
                                          filetypes=(("CSV files",
                                                      "*.csv"),
                                                     ("all files",
                                                      "*.*")))
        self.key_sheet_data.load(path)
        self.key_name = path.split('/')[-1]
        stat_names_key = []
        for row in self.key_sheet_data:
            stat_names_key.append(row.get_cells('stat'))
        self.lbl_key.configure(text="Found key: " + str(self.key_name))
        query = "SELECT statName FROM stat"
        self.db_cursor.execute(query)
        saved_stats = []
        for statName in self.db_cursor:
            saved_stats.append(statName[0])
        to_be_removed = [x for x in stat_names_key if x in saved_stats]
        outlist = "("
        for x in to_be_removed:
            outlist += "\"" + str(x) + "\" ,"
        outlist = outlist[:-1] + ')'
        if len(to_be_removed) > 0:
            query = "DELETE FROM stat WHERE statName IN" + outlist
            print(query)
            self.db_cursor.execute(query)
        query = ""
        for row in self.key_sheet_data:
            OD = 0
            if row.get_cells('Off/Deff') == "Off": OD = 1
            else: OD = 2
            name = row.get_cells('stat')
            weight = row.get_cells('weights')
            gtl = row.get_cells('GtL')
            query += "INSERT INTO stat (statName, GtL, weight, idstattype) VALUES (\"" + name + "\"," + gtl + "," + weight + "," + str(OD) + ");\n"
        print(query)
        self.db_cursor.execute(query, multi=True)
        print(self.db_cursor)



    def load_sheet(self, filename, sheet_data):
        if sheet_data.hasData():

            self.sheet_data = sheet_data
            self.label.configure(text=filename + " to Database", foreground="grey")
            self.controller.show_frame(Db_Add_Stats)
        else:
            messagebox.showwarning('CSV Error', 'Please open a .csv')
            self.controller.show_frame(EmptyFrame)
