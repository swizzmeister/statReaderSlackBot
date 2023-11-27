import tkinter as tk
import datetime
from tkinter import filedialog, messagebox
from tkinter import ttk

import mysql

from Frames.empty_frame import EmptyFrame


class DbAddEvent(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
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
        # Date
        self.date_set = tk.StringVar()
        self.date_set.set(self.date)
        date_lbl = ttk.Label(event_set, text="Change Date")
        dateEntry = ttk.Entry(event_set, textvariable=self.date_set)
        dateEntry.grid(row=0, column=1, pady=10, padx=10, sticky='sw')
        date_lbl.grid(row=0, column=0, padx=10, pady=10, sticky='sw')
        # Name
        self.name_set = tk.StringVar()
        self.name_set.set("")
        name_lbl = ttk.Label(event_set, text="Change Name")
        name_entry = ttk.Entry(event_set, textvariable=self.name_set)
        name_entry.grid(row=1, column=1, pady=10, padx=10, sticky='sw')
        name_lbl.grid(row=1, column=0, padx=10, pady=10, sticky='sw')
        # Event Type
        query = "SELECT name FROM event_type"
        self.db_cursor.execute(query)
        eventsTypes = []
        for name in self.db_cursor:
            eventsTypes.append(name[0])
            print(eventsTypes[0], " Length:", str(len(eventsTypes)))
        drop_lbl = ttk.Label(event_set, text="Event Type:")
        drop_lbl.grid(column=0, row=2,padx=10, pady=10)
        drop = tk.OptionMenu(event_set, tk.StringVar(value=eventsTypes[0]), *eventsTypes)
        drop.grid(column=1, row=2, padx=10, pady=10)
        # Send Button
        sendBtn = tk.Button(event_set, text="Save")
        sendBtn.grid(column=0, row=3, columnspan=2, pady=10, padx=10, sticky='s')


    def setDate(self):
        self.controller.set_date(date=self.date_set.get())

    def load_sheet(self, filename, sheet_data):
        if sheet_data.hasData():

            self.sheet_data = sheet_data
            self.label.configure(text=filename + " to Database", foreground="grey")
            self.controller.show_frame(DbAddEvent)
        else:
            messagebox.showwarning('CSV Error', 'Please open a .csv')
            self.controller.show_frame(EmptyFrame)
