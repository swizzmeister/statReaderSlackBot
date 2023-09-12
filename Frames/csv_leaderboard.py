import datetime
import re
import tkinter as tk
from tkinter import Listbox, ttk, messagebox


class csvPicker(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.reader = controller.get_reader()
        self.date = datetime.date.today().strftime("%Y/%m/%d")
        self.cat_c = tk.StringVar()
        self.date_set = tk.StringVar()
        self.date_set.set(self.date)
        self.cat_c.set("Choose Category")
        self.tables_saved = []
        self.saved_var = tk.StringVar(value=self.tables_saved)
        self.ltg = tk.BooleanVar()
        self.sum_bool_var = tk.BooleanVar();
        self.sum_bool_var.set("False")
        self.avg_bool_var = tk.BooleanVar();
        self.avg_bool_var.set("False")
        self.ltg.set("False")
        self.list_box = Listbox(self, height=6, listvariable=self.tables_saved)
        self.list_box.configure(width=int((controller.winfo_width() / 3) - 8))
        self.list_box.grid(column=0, row=5, columnspan=3, pady=3, padx=3)
        self.label = ttk.Label(self, text="", font=self.controller.LARGEFONT)
        self.label.grid(columnspan=3, column=0, row=0, padx=30, pady=10)
        button0 = ttk.Button(self, text="-",
                             command=lambda: self.remove_selected())
        button0.grid(row=2, column=1, rowspan=3, padx=10, pady=10)
        self.button1 = ttk.Button(self, text="Show table",
                                  command=lambda: self.show_selected_table())
        self.button1.grid(row=6, column=2, columnspan=2, padx=10, pady=10)
        button2 = ttk.Button(self,
                             text="+",
                             command=lambda: self.save_table())
        button2.grid(row=2, column=0, rowspan=3, padx=10, pady=10)
        dateBtn = ttk.Button(self,
                             text="Change Date",
                             command=lambda: self.setDate())
        dateEntry = ttk.Entry(self, textvariable=self.date_set)
        dateEntry.grid(row=1, column=1, pady=10)
        dateBtn.grid(row=1, column=0, padx=10, pady=10)

        check = ttk.Checkbutton(self, text="Greatest to Least", variable=self.ltg)
        check.grid(column=2, row=2, padx=10, pady=3)
        check1 = ttk.Checkbutton(self, text="Average Line", variable=self.sum_bool_var)
        check1.grid(column=2, row=3, padx=10, pady=3)
        check2 = ttk.Checkbutton(self, text="Sum Line", variable=self.avg_bool_var)
        check2.grid(column=2, row=4, padx=10, pady=3)

    def setDate(self):
        self.controller.set_date(date=self.date_set.get())

    def load_reader(self, filename, reader):
        self.reader = reader
        self.label.configure(text=filename + " to Leaderboard", foreground="grey")
        cols = self.reader.getCatagories()
        drop = tk.OptionMenu(self, self.cat_c, *cols)
        drop.grid(column=2, row=1, padx=10, pady=10)
        self.tables_saved = []
        self.saved_var.set(self.tables_saved)
        self.list_box.configure(listvariable=self.saved_var)

    def save_table(self):
        self.tables_saved.append(
            "Category:[" + self.cat_c.get() + "]Greatest to Least:[" + self.controller.boolString(
                self.ltg.get()) + "]Avg:[" + self.controller.boolString(self.avg_bool_var.get()) +
            "]Sum:[" + self.controller.boolString(self.sum_bool_var.get()) + "]")
        self.controller.SELECTED.append((self.cat_c.get(), self.ltg.get(),
                                         self.avg_bool_var.get(), self.sum_bool_var.get()))
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
