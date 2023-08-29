from tkinter import *
import tkinter as tk
from tkinter import Menu
from tkinter import filedialog
from tkinter import ttk
import statInterpreter


def browseFiles():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a csv Stat File",
                                          filetypes=(("CSV files",
                                                      "*.csv*"),
                                                     ("all files",
                                                      "*.*")))

    # Change label contents
    filename.label_file_explorer.configure(text="File Opened: " + filename)
    reader = statInterpreter.StatInterpreter(filename)
    print(filename)
    reader.load()
    return reader.getCatagories()





window.title("Leaderboard Spreadsheets")
menu = Menu(window)
new_item = Menu(menu)
new_item.add_command(label='New')
new_item.add_separator()
new_item.add_command(label='Edit')
menu.add_cascade(label='File', menu=new_item)
cata = []
button_explore = Button(window,
                        text="Browse Files",
                        command=lambda: cata==browseFiles())
label_file_explorer.grid(column=1, row=1)

button_explore.grid(column=1, row=2)
window.config(menu=menu)
window.mainloop()



