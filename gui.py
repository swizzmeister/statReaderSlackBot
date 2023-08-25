from tkinter import *
import tkinter as tk
from tkinter import Menu
from tkinter import filedialog
from tkinter import ttk
import statInterpreter
class dataDisplayTree():

    def __init__(self, leaderBoard, stat):

        self.data_win = Tk()
        self.data_win.geometry('600x600')
        self.data_win.title(stat + ' Leaderboard')
        self.tv_data = ttk.Treeview(self.data_win)
        self.tv_data.pack(fill=tk.BOTH, expand=True)
        self.stat = stat
        self.c_names = 'name', 'stat'
        self.tv_data.configure(columns=self.c_names)
        self.tv_data.heading('name', text='Name')
        self.tv_data.heading('#0', text='Rank')
        self.tv_data.heading('stat', text=stat)
        i=1
        for player in leaderBoard:
            self.tv_data.insert(parent="",
                                index=tk.END,
                                text=i,
                                values=(player[0], player[1]))
            i+=1
        self.data_win.mainloop()
activeLeaderboardFile
window = Tk()
window.geometry('620x200')
label_file_explorer = Label(window,
                            text="File Explorer using Tkinter",
                            width=100, height=4,
                            fg="blue")


def browseFiles():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a csv Stat File",
                                          filetypes=(("CSV files",
                                                      "*.csv*"),
                                                     ("all files",
                                                      "*.*")))

    # Change label contents
    label_file_explorer.configure(text="File Opened: " + filename)
    reader = statInterpreter.StatInterpreter(filepath)
    print(filepath)
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



