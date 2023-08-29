import tkinter as tk
from tkinter import ttk
import statInterpreter
from tkinter import filedialog

LARGEFONT = ("Verdana", 15)


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

        button1 = ttk.Button(self, text="Page 1",
                             command=lambda: controller.show_frame(Page1))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=0, padx=10, pady=10)

        ## button to show frame 2 with text layout2
        button2 = ttk.Button(self, text="Page 2",
                             command=lambda: controller.show_frame(Page2))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=0, padx=10, pady=10)


# second window frame page1

class Page1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 1", font=LARGEFONT)
        label.grid(row=0, column=0, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="StartPage",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place
        # by using grid
        button1.grid(row=1, column=0, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button2 = ttk.Button(self, text="Page 2",
                             command=lambda: controller.show_frame(Page2))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=0, padx=10, pady=10)


# third window frame page2
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        self.reader = None
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Lbl", font=LARGEFONT)
        label.grid(row=0, column=0, padx=10, pady=10)
        button0 = ttk.Button(self, text="Page 1",
                             command=lambda: controller.show_frame(Page1))
        button0.grid(row=3, column=0, padx=10, pady=10)
        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Show table",
                             command=lambda: dataDisplayTree(self.reader, "fg/g", True))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=0, padx=10, pady=10)

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





# Driver Code
app = tkinterApp()
app.mainloop()
