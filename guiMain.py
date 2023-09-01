import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import slack
import re
from slack import WebClient
import bot
import statInterpreter
from tkinter import filedialog, Listbox

LARGEFONT = ("Helvetica", 15)
ACTIVE = False
ICON = "basketball.ico"


def browse_files(page, target):
    path = filedialog.askopenfilename(initialdir="/",
                                      title="Select a csv Stat File",
                                      filetypes=(("CSV files",
                                                  "*.csv*"),
                                                 ("all files",
                                                  "*.*")))
    reader = statInterpreter.StatInterpreter(path)
    print(path)
    reader.load()
    page.set_reader(reader)
    target.load_reader(path.split('/')[-1], reader)


def data_display_tree(leaderboard, stat, orderUp):
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
    i = 1
    print(leaderboard.print_LeaderBoard(stat, orderUp, ' sec'))
    for player in leaderboard.get_Sorted_Leaderboard(stat, orderUp):
        tv_data.insert(parent="",
                       index=tk.END,
                       text=i,
                       values=(player[0], player[1]))
        i += 1
    data_win.mainloop()


def slack_add(page):
    new_window = tk.Tk()
    new_window.title('Connect to API')
    frame = slackAddFrame(new_window, page)
    new_window.iconbitmap(ICON)
    frame.pack()


def slack_test(page):
    new_window = tk.Tk()
    new_window.title('API Connection Test')
    new_window.iconbitmap(ICON)
    frame = SlackTest(new_window, page)
    frame.pack()

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Slack Stats App')
        self.iconbitmap(ICON)
        self.reader = None
        self.SLACKKEY = ""
        container = tk.Frame(self)
        menubar = tk.Menu(self)
        self.configure(menu=menubar, width=300, height=300)
        file_menu = tk.Menu(menubar)
        slack_menu = tk.Menu(menubar)

        container.pack()

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, Page1, Page2, EmptyFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(EmptyFrame)
        file_menu.add_command(label='Open CSV', command=lambda: browse_files(self, self.frames[Page2]))
        slack_menu.add_command(label='Add to Slack', command=lambda: slack_add(self))
        slack_menu.add_command(label='Test Connection', command=lambda: slack_test(self))
        menubar.add_cascade(
            label="File",
            menu=file_menu
        )
        menubar.add_cascade(
            label="Slack",
            menu=slack_menu
        )

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def set_reader(self, reader):
        self.reader = reader
        self.show_frame(Page2)

    def get_reader(self):
        return self.reader

    def set_slack_key(self, k):
        print(k)
        self.SLACKKEY = k
        print(self.SLACKKEY)

    def get_slack_key(self):
        print(self.SLACKKEY)
        return self.SLACKKEY


class slackAddFrame(tk.Frame):
    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.root = root
        self.slack_key_entry = tk.StringVar()
        l = ttk.Label(self, text="Slack Key:")
        self.key = ttk.Entry(self, textvariable=self.slack_key_entry)
        l.grid(row=0, column=0, padx=20, pady=10)
        self.key.grid(row=0, column=1, padx=20, pady=10)
        button1 = ttk.Button(self,
                             text="Set Key",
                             command=lambda: self.assign_slack_key())
        button1.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

    def assign_slack_key(self):
        self.root.set_slack_key = self.slack_key_entry.get()
        global CLIENT;
        CLIENT = slack.WebClient(token=self.slack_key_entry.get())
        if CLIENT.api_test()['ok']:
            global ACTIVE;
            ACTIVE = True
        self.parent.destroy()


class SlackTest(tk.Frame):

    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        print(root.get_slack_key())
        if ACTIVE:
            if CLIENT.api_test()['ok']:
                image = Image.open('img/connected.png')

                text = "Connected"
            else:
                image = Image.open('img/disconnected.png')
                text = "Disconnected"
        else:
            image = Image.open('img/disconnected.png')
            text = "Disconnected"

        image_tk = ImageTk.PhotoImage(master=self, image=image)
        print(image_tk)
        label = ttk.Label(self, image=image_tk)
        label.image = image_tk
        label.grid(row=0, column=0, pady=10, padx=20)
        label1 = ttk.Label(self, text=text)
        label1.grid(row=0, column=2, pady=10, padx=20)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        label = ttk.Label(self, text="Startpage", font=LARGEFONT)

        # putting the grid in its place by using
        # grid
        label.pack(pady=20)

        button1 = ttk.Button(self, text="Config Slack",
                             command=lambda: controller.show_frame(Page1))

        # putting the button in its place by
        # using grid
        button1.pack(pady=40)

        ## button to show frame 2 with text layout2
        button2 = ttk.Button(self, text="Config CSV",
                             command=lambda: controller.show_frame(Page2))

        # putting the button in its place by
        # using grid
        button2.pack(pady=40)


# second window frame page1

class Page1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.slack_key = tk.StringVar()
        self.label = ttk.Label(self, text="OFFLINE", foreground="red", font=LARGEFONT)
        self.label.grid(row=0, column=0, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        l = ttk.Label(self, text="Slack Key:")
        self.key = ttk.Entry(self, textvariable=self.slack_key)
        l.grid(row=1, column=0, padx=10, pady=10)
        self.key.grid(row=1, column=2, columnspan=2, padx=10, pady=10)

        button1 = ttk.Button(self, text="Set Key",
                             command=lambda: self.assign_slack_key())

        # putting the button in its place
        # by using grid
        button1.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button2 = ttk.Button(self, text="Config CSV",
                             command=lambda: controller.show_frame(Page2))

        # putting the button in its place by
        # using grid
        button2.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        button3 = ttk.Button(self, text="Test Slack Connection", command=lambda: self.testSlackKey())
        button3.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def assign_slack_key(self):
        SLACKKEY = self.slack_key.get()
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
        tk.Frame.__init__(self, parent)
        self.reader = controller.get_reader()
        self.cat_c = tk.StringVar()
        self.cat_c.set("Choose Category")
        self.tables_saved = []
        self.saved_var = tk.StringVar(value=self.tables_saved)
        self.ltg = tk.BooleanVar()
        self.ltg.set("False")
        self.list_box = Listbox(self, height=6, listvariable=self.tables_saved)
        print('width:', controller.winfo_width())
        self.list_box.configure(width=int((controller.winfo_width() / 3) - 8))
        self.list_box.grid(column=0, row=3, columnspan=3, pady=3, padx=3)
        self.label = ttk.Label(self, text="", font=LARGEFONT)
        self.label.grid(columnspan=3, column=0, row=0, padx=30, pady=10)
        button0 = ttk.Button(self, text="-",
                             command=lambda: self.remove_selected())
        button0.grid(row=2, column=1, padx=10, pady=10)
        self.button1 = ttk.Button(self, text="Show table",
                                  command=lambda: self.show_selected_table())
        self.button1.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        button2 = ttk.Button(self,
                             text="+",
                             command=lambda: self.save_table())
        button2.grid(row=2, column=0, padx=10, pady=10)

    def load_reader(self, filename, reader):
        self.reader = reader
        self.label.configure(text=filename, foreground="grey")
        cols = self.reader.getCatagories()
        drop = tk.OptionMenu(self, self.cat_c, *cols)
        drop.grid(column=2, row=1, padx=10, pady=10)
        check = ttk.Checkbutton(self, text="Greatest to Least", variable=self.ltg)
        check.grid(column=2, row=2, padx=10, pady=10)
        self.tables_saved = []
        self.saved_var.set(self.tables_saved)
        self.list_box.configure(listvariable=self.saved_var)

    def save_table(self):
        self.tables_saved.append(
            "Category: [" + self.cat_c.get() + "]      Least to Greatest: [" + boolString(self.ltg.get()) + "]")
        self.saved_var.set(self.tables_saved)
        self.list_box.configure(listvariable=self.saved_var)

    def show_selected_table(self):
        table = self.tables_saved[self.get_selected_index()]
        stats = re.split(r'\[(.*?)\]', table)
        print('"' + stats[0] + '"', '"' + stats[1] + '"')
        data_display_tree(self.reader, stats[1], stats[3])

    def remove_selected(self):
        self.tables_saved.pop(self.get_selected_index())
        self.saved_var.set(self.tables_saved)
        self.list_box.configure(listvariable=self.saved_var)

    def get_selected_index(self):
        i = 0
        while i < len(self.tables_saved):
            if self.list_box.selection_includes(i):
                return i
            i += 1


def boolString(bool):
    if bool:
        return "True"
    return "False"


def stringBool(string):
    if string == "True":
        return True
    else:
        return False


class EmptyFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(master=self, text="No Available CSV", font=('Helvetica', 24))
        label.configure(foreground="grey")
        label.place(relx=0.5, rely=0.5, anchor='center')


# Driver Code
app = tkinterApp()
app.mainloop()
