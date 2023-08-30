import tkinter as tk
from tkinter import ttk

import slack
from slack import WebClient
import bot
import statInterpreter
from tkinter import filedialog

LARGEFONT = ("Verdana", 15)
SLACKKEY = ""


def browseFiles(page):
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a csv Stat File",
                                          filetypes=(("CSV files",
                                                      "*.csv*"),
                                                     ("all files",
                                                      "*.*")))

    # Change label contents

    reader = statInterpreter.StatInterpreter(filename)
    print(filename)
    reader.load()
    page.set_reader(reader)
    if reader.hasData():
        page.set_table_button_visible()
        page.insert_list_box(reader.getCatagories())


def dataDisplayTree(leaderBoard, stat, dir):
    data_win = tk.Tk()
    data_win.geometry('600x600')
    data_win.title(stat + ' Leaderboard')
    tv_data = ttk.Treeview(data_win)
    tv_data.pack(fill=tk.BOTH, expand=True)
    c_names = 'name', 'stat'
    tv_data.configure(columns=c_names)
    tv_data.heading('name', text='Name')
    tv_data.heading('#0', text='Rank')
    tv_data.heading('stat', text=stat)
    i=1
    print(leaderBoard.print_LeaderBoard(stat, dir,' sec'))
    for player in leaderBoard.get_Sorted_Leaderboard(stat, dir):
        tv_data.insert(parent="",
                   index=tk.END,
                   text=i,
                   values=(player[0], player[1]))
        i+=1
    data_win.mainloop()
class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1, Page2):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# first window frame startpage

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        label = ttk.Label(self, text="Startpage", font=LARGEFONT)

        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=0, padx=10, pady=10)

        button1 = ttk.Button(self, text="Config Slack",
                             command=lambda: controller.show_frame(Page1))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=0, padx=10, pady=10)

        ## button to show frame 2 with text layout2
        button2 = ttk.Button(self, text="Config CSV",
                             command=lambda: controller.show_frame(Page2))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=0, padx=10, pady=10)



# second window frame page1

class Page1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.Slackkey = tk.StringVar()
        self.label = ttk.Label(self, text="OFFLINE",foreground="red", font=LARGEFONT)
        self.label.grid(row=0, column=0, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        l = ttk.Label(self,text="Slack Key:")
        self.key = ttk.Entry(self,textvariable=self.Slackkey)
        l.grid(row=1, column=0, padx=10, pady=10)
        self.key.grid(row=1, column=2, columnspan=2, padx=10, pady=10)

        button1 = ttk.Button(self, text="Set Key",
                             command=lambda: self.assignSlackKey())

        # putting the button in its place
        # by using grid
        button1.grid(row=2, column=0,columnspan=2, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button2 = ttk.Button(self, text="Config CSV",
                             command=lambda: controller.show_frame(Page2))

        # putting the button in its place by
        # using grid
        button2.grid(row=3, column=0,columnspan=2, padx=10, pady=10)

        button3 = ttk.Button(self, text="Test Slack Connection", command=lambda: self.testSlackKey())
        button3.grid(row=4, column=0,columnspan=2, padx=10, pady=10)
    def assignSlackKey(self):
        SLACKKEY = self.Slackkey.get()
        global CLIENT
        CLIENT = slack.WebClient(token=SLACKKEY)
        self.label.configure(foreground="black", text="Key-Set")
        self.label.grid(row=0, column=0, padx=10, pady=10)
        print(CLIENT)

    def testSlackKey(self):
        print(CLIENT.api_test()['ok'])
        if CLIENT.api_test()['ok']:
            print('true')
            self.label.configure(foreground="green", text="Online")
            self.label.grid(row=0, column=0, padx=10, pady=10)



# third window frame page2
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        self.reader = None
        self.cat_c = tk.StringVar()
        self.cat_c.set("Choose Category")
        self.ltg = tk.BooleanVar()
        self.ltg.set("False")
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Lbl", font=LARGEFONT)
        label.grid(columnspan=2, column=0, row=0, padx=10, pady=10)
        button0 = ttk.Button(self, text="Config Slack",
                             command=lambda: controller.show_frame(Page1))
        button0.grid(row=3, column=0, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        self.button1 = ttk.Button(self, text="Show table",
                             command=lambda: dataDisplayTree(self.reader, self.cat_c.get(), self.ltg.get()))

        # putting the button in its place by
        # using grid


        # button to show frame 3 with text
        # layout3

        button2 = ttk.Button(self,
                        text="Choose File",
                        command=lambda : browseFiles(self))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=0, padx=10, pady=10)

    def set_reader(self, reader):
        self.reader = reader

    def set_table_button_visible(self):
        self.button1.grid(row=1, column=0, padx=10, pady=10)
    def insert_list_box(self,cols):
        drop = tk.OptionMenu(self, self.cat_c, *cols)
        drop.grid(column=2, row=1,padx=10,pady=10)
        check = ttk.Checkbutton(self, text="Greatest to Least", variable=self.ltg)
        check.grid(column=2, row=2,padx=10,pady=10)



# Driver Code
app = tkinterApp()
app.mainloop()
