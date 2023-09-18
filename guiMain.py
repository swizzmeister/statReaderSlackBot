import slack
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import statInterpreter
from Frames.PlayerComparison import PlayerComparison
from Frames.csv_leaderboard import csvPicker
from Frames.empty_frame import EmptyFrame
from Frames.slackFrames.slack_add_frame import slackAddFrame
from Frames.slackFrames.slack_test import SlackTest


class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.LARGEFONT = ("Helvetica", 15)
        self.ACTIVE = False
        self.ICON = "basketball.ico"
        self.SELECTED = []
        self.READER = object
        self.READ = object
        self.CLIENT = object
        self.CHANNEL = ""
        self.FILENAME = ""
        self.DATE = ""
        self.SUMLINE = False
        self.AVGLINE = False
        self.title('StatSync')
        self.iconbitmap(self.ICON)
        self.reader = None
        self.SLACKKEY = ""
        self.container = tk.Frame(self)
        self.container.pack()
        self.init_menu()
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (csvPicker, EmptyFrame, PlayerComparison):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(EmptyFrame)

    def init_menu(self):
        menubar = tk.Menu(self)
        self.configure(menu=menubar, width=300, height=300)
        file_menu = tk.Menu(menubar)
        function_menu = tk.Menu(menubar)
        slack_menu = tk.Menu(menubar)
        function_menu.add_command(label='Player Comparison', command=lambda: self.frames[
            PlayerComparison].load_reader(self.FILENAME, self.READ))
        function_menu.add_command(label='Single Stat Leaderboard', command=lambda: self.show_frame(csvPicker))
        file_menu.add_command(label='Open CSV', command=lambda: self.browse_files(self, self.frames[csvPicker]))
        file_menu.add_command(label='Export to Slack', command=lambda: self.export_to_slack())
        slack_menu.add_command(label='Connect to Slack', command=lambda: self.slack_add())
        slack_menu.add_command(label='Test Connection', command=lambda: self.slack_test())

        menubar.add_cascade(
            label="File",
            menu=file_menu
        )
        menubar.add_cascade(
            label="Slack",
            menu=slack_menu
        )
        menubar.add_cascade(
            label="Stat Functions",
            menu=function_menu
        )

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.grid()

    def set_reader(self, reader):
        self.reader = reader
        self.show_frame(csvPicker)

    def get_reader(self):
        return self.reader

    def set_slack_key(self, k):
        self.SLACKKEY = k

    def get_slack_key(self):
        return self.SLACKKEY

    def set_date(self, date):
        self.DATE = date

    def export_to_slack(self):
        if not self.ACTIVE:
            messagebox.showwarning('Slack Client Error', 'Please connect to a Slack Workspace')
        else:
            try:
                for entry in self.SELECTED:
                    self.CLIENT.chat_postMessage(channel=self.CHANNEL,
                                                 text=self.reader.print_LeaderBoard(stat=entry[0], ltg=entry[1],
                                                                                    unit=entry[0], date=self.DATE,
                                                                                    avg=entry[2], sum=entry[3]))
            except slack.errors.SlackApiError as e:
                messagebox.showerror('Slack Client Error', 'Table was not sent successfully!\n' + str(e))
            else:
                messagebox.showinfo('Slack Bot', 'Table(s) sent successfully!')

    def slack_test(self):
        new_window = tk.Toplevel()
        new_window.title('API Connection Test')
        new_window.iconbitmap(self.ICON)
        frame = SlackTest(new_window, self)
        frame.pack()

    def slack_add(self):
        new_window = tk.Toplevel()
        new_window.title('Connect to API')
        frame = slackAddFrame(new_window, self)
        new_window.iconbitmap(self.ICON)
        frame.pack()

    def browse_files(self, page, target):
        path = filedialog.askopenfilename(initialdir="/",
                                          title="Select a csv Stat File",
                                          filetypes=(("CSV files",
                                                      "*.csv"),
                                                     ("all files",
                                                      "*.*")))
        reader = statInterpreter.StatInterpreter(path)
        reader.load()
        page.set_reader(reader)
        self.READ = reader
        self.FILENAME = path.split('/')[-1]
        target.load_reader(path.split('/')[-1], reader)
    @staticmethod
    def leaderboard_data_display_tree(leaderboard, stat, orderUp, sum, avg):
        data_win = tk.Toplevel()
        data_win.geometry('600x600')
        data_win.title(stat + ' Leaderboard')
        tv_data = ttk.Treeview(data_win)
        c_names = 'name', 'stat'
        tv_data.configure(columns=c_names)
        tv_data.heading('name', text='Name')
        tv_data.heading('#0', text='Rank')
        tv_data.heading('stat', text=stat)
        i = 1
        for player in leaderboard.get_Sorted_Leaderboard(stat, orderUp):
            tv_data.insert(parent="",
                           index=tk.END,
                           text=i,
                           values=(player[0], player[1]))
            i += 1
        if sum:
            tv_data.insert(parent="", index=tk.END,
                            text="SUM", values=(' ', '=' + str(leaderboard.getCatagorySum(stat))))
        if avg:
            tv_data.insert(parent="", index=tk.END,
                               text="AVG", values=(' ', '=' + str(leaderboard.getCatagoryAvg(stat))))
        tv_data.pack(fill=tk.BOTH, expand=True)


    def player_compare_data_display_tree(self, stat, orderUp, sum, avg):
        data_win = tk.Toplevel()
        data_win.geometry('600x600')
        data_win.title('Player Comparison')
        tv_data = ttk.Treeview(data_win)
        c_names = self.READ.calculable_cols()
        print('c_names', c_names)
        tv_data.configure(columns=c_names)
        i=0
        for col in c_names:
            if i == 0:
                tv_data.heading('#0', text="Names")
            tv_data.heading(col, text=col)
            tv_data.column(col, minwidth=5, width=20)
            i += 1
        i = 1
        print(len(self.READ.players))
        for num in self.READ.playerNums:
            player = self.READ.players[num]
            print('PLayer', player)
            stat_list = [stats for stats in player.items()]
            print(len(stat_list))
            pName = ""
            i=0
            while i < len(stat_list):
                stat = stat_list[i]
                print('Stat', stat[0])
                if stat[0] == 'Name':
                    pName = stat[1]
                    stat_list.remove(stat)
                    i -= 1
                elif stat[0] not in c_names:
                    stat_list.remove(stat)
                    i -= 1
                else:
                    print(stat[0])
                    stat_list[stat_list.index(stat)] = self.READ.getCatagoryAvg(stat[0]) - float(stat[1].split('-')[0])
                i+=1
            print(stat_list , i)
            tv_data.insert(parent="",
                           index=tk.END,
                           text=pName,
                           values=stat_list)
            i += 1
        tv_data.pack(fill=tk.BOTH, expand=True)

    @staticmethod
    def boolString(b):
        if b:
            return "True"
        return "False"

    @staticmethod
    def stringBool(s):
        if s == "True":
            return True
        else:
            return False


# Driver Code
app = tkinterApp()
app.mainloop()
