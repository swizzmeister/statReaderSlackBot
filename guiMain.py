import slack
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

from Frames.statFunctionFrames.weighted_stat_output import WeightedStatOutput
from sheetData import SheetData
from Frames.statFunctionFrames.PlayerComparison import PlayerComparison
from Frames.statFunctionFrames.csv_leaderboard import csvPicker
from Frames.dbFrames.db_add_player import Db_Add_Player
from Frames.empty_frame import EmptyFrame
from Frames.slackFrames.slack_add_frame import slackAddFrame
from Frames.slackFrames.slack_test import SlackTest


class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.endpoint = "ls-0422de67b1c71a340b3cfe2c7eb96e5a06bd3503.c8l0afdxuj5t.ca-central-1.rds.amazonaws.com"
        self.LARGEFONT = ("Helvetica", 15)
        self.ACTIVE = False
        self.ICON = "basketball.ico"
        self.SELECTED = []
        self.SHEET = SheetData()
        self.CLIENT = object
        self.CHANNEL = ""
        self.FILENAME = ""
        self.DATE = ""
        self.SUMLINE = False
        self.AVGLINE = False
        self.title('StatSync')
        self.iconbitmap(self.ICON)
        self.SLACKKEY = ""
        self.container = tk.Frame(self)
        self.container.anchor = tk.CENTER
        self.container.pack()
        self.init_menu()
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (csvPicker, EmptyFrame, PlayerComparison, Db_Add_Player, WeightedStatOutput):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(EmptyFrame)
        self.activeFrame = EmptyFrame

    def init_menu(self):
        """
        Initilizes Menu for main tkinter root
        """
        menubar = tk.Menu(self)
        self.configure(menu=menubar, width=300, height=300)
        file_menu = tk.Menu(menubar)
        function_menu = tk.Menu(menubar)
        slack_menu = tk.Menu(menubar)
        database_menu = tk.Menu(menubar)
        function_menu.add_command(label='Player Comparison', command=lambda: self.frames[
            PlayerComparison].load_sheet(self.FILENAME, self.SHEET))
        function_menu.add_command(label='Single Stat Leaderboard', command=lambda: self.csv_check(csvPicker))
        function_menu.add_command(label='Weighted Stat Output',
                                  command=lambda: self.frames[WeightedStatOutput].load_sheet(self.FILENAME, self.SHEET))
        file_menu.add_command(label='Open CSV', command=lambda: self.browse_files(self, self.frames[csvPicker]))
        file_menu.add_command(label='Export to Slack', command=lambda: self.export_to_slack())
        slack_menu.add_command(label='Connect to Slack', command=lambda: self.slack_add())
        slack_menu.add_command(label='Test Connection', command=lambda: self.slack_test())
        database_menu.add_command(label='Base Player Entry', command=lambda: self.show_frame(Db_Add_Player))
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
        menubar.add_cascade(
            label="Database Functions",
            menu=database_menu
        )

    def csv_check(self, frame: tk.Frame):

        if self.SHEET.hasData():
            self.show_frame(frame)
        else:
            messagebox.showwarning('CSV Error', 'Please open a .csv')
            self.show_frame(EmptyFrame)

    def show_frame(self, cont: tk.Frame):
        """

        :param cont: Frame inwhich the root is swithcing to
        """
        frame = self.frames[cont]
        self.activeFrame = cont
        frame.tkraise()
        frame.grid()

    def get_sheet_data(self):
        return self.SHEET

    def set_slack_key(self, k):
        self.SLACKKEY = k

    def set_date(self, date):
        self.DATE = date

    def export_to_slack(self):
        # Export as CSV Picker-------------
        if self.activeFrame == csvPicker:
            if not self.ACTIVE:
                messagebox.showwarning('Slack Client Error', 'Please connect to a Slack Workspace')
            else:
                try:
                    for entry in self.SELECTED:
                        self.CLIENT.chat_postMessage(channel=self.CHANNEL,
                                                     text=self.SHEET.printLeaderboard(stat=entry[0],
                                                                                      least_to_greatest=entry[1],
                                                                                      unit="", date=self.DATE,
                                                                                      avg=entry[2], sum=entry[3]))
                except slack.errors.SlackApiError as e:
                    messagebox.showerror('Slack Client Error', 'Table was not sent successfully!\n' + str(e))
                else:
                    messagebox.showinfo('Slack Bot', 'Table(s) sent successfully!')
        # Export as Player comparison--------------------------------
        elif self.activeFrame == PlayerComparison:
            if not self.ACTIVE:
                messagebox.showwarning('Slack Client Error', 'Please connect to a Slack Workspace')
            else:
                None
        # Export as weighted output---------------------------------------
        elif self.activeFrame == WeightedStatOutput:
            weightedFrame = self.frames.get(WeightedStatOutput)
            image_path = weightedFrame.outputImagePath
            rank_list = weightedFrame.key_sheet_data.getPlayerOvrRank(self.SHEET)
            userIDs = weightedFrame.getPlayerUserIDs(rank_list)
            try:
                self.CLIENT.files_upload(
                    channels=self.CHANNEL,
                    initial_comment="Leaderboard from latest practice!",
                    file=image_path
                )
                for num in userIDs.keys():
                    self.CLIENT.chat_postMessage(channel=userIDs[num],
                                                 text=weightedFrame.pp_PlayerRankedOutput(num))
            except slack.errors.SlackApiError as e:
                messagebox.showerror('Slack Client Error', 'Table was not sent successfully!\n' + str(e))
            else:
                messagebox.showinfo('Slack Bot', 'Image of table sent successfully!')

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
        path = filedialog.askopenfilename(initialdir="C:\\Users\\Logan\\Desktop",
                                          title="Select a csv Stat File",
                                          filetypes=(("CSV files",
                                                      "*.csv"),
                                                     ("all files",
                                                      "*.*")))
        self.SHEET.load(path)
        self.show_frame(csvPicker)
        self.FILENAME = path.split('/')[-1]
        target.load_sheet(filename=self.FILENAME, sheet_data=self.SHEET)

    @staticmethod
    def leaderboard_data_display_tree(sheet: SheetData, stat: str, order_up: bool, sm: bool, avg: bool):
        """

        :param avg: Will show avg row if true
        :param sm: Will show sum row if true
        :param order_up: Greatest to least if true
        :param stat: The stat in which you would like to rank
        :param sheet: Sheet data to create leaderboard from
        """
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
        for player in sheet.get_Sorted_Leaderboard(stat, order_up):
            tv_data.insert(parent="",
                           index=tk.END,
                           text=i,
                           values=(sheet.get_rows(player[0]).get_cells('Name'), player[1]))
            i += 1
        if sm:
            tv_data.insert(parent="", index=tk.END,
                           text="SUM", values=(' ', '=' + str(sheet.get_col_sum(stat))))
        if avg:
            tv_data.insert(parent="", index=tk.END,
                           text="AVG", values=(' ', '=' + str(sheet.get_col_avg(stat))))
        tv_data.pack(fill=tk.BOTH, expand=True)

    def player_compare_data_display_tree(self, cols, selectedPlayers):
        """

        :param cols: Columns you wish to compare
        :param selectedPlayers: Players you wish to compare
        """
        data_win = tk.Toplevel()
        data_win.title('Player Comparison')
        tv_data = ttk.Treeview(data_win)
        tv_data.configure(columns=cols)
        i = 0
        for col in cols:
            if i == 0:
                tv_data.heading('#0', text="Names")
            tv_data.heading(col, text=col)
            tv_data.column(col, minwidth=20, width=50)
            i += 1
        i = 1
        for player in self.SHEET.get_rows(selectedPlayers):
            stat_list = [stats for stats in player.get_stats(cols).items()]
            pName = ""
            i = 0
            while i < len(stat_list):
                stat = stat_list[i]
                if stat[0] == 'Name':
                    pName = stat[1]
                    stat_list.remove(stat)
                    i -= 1
                elif stat[0] not in cols:
                    stat_list.remove(stat)
                    i -= 1
                else:
                    if stat[1] != '-':
                        if self.SHEET.get_col_avg(stat[0], selectedPlayers) < float(stat[1]):
                            stat_list[stat_list.index(stat)] = "+" + str(
                                round(float(stat[1]) - self.SHEET.get_col_avg(stat[0], selectedPlayers), 2))
                        else:
                            stat_list[stat_list.index(stat)] = str(
                                round(float(stat[1]) - self.SHEET.get_col_avg(stat[0], selectedPlayers), 2))
                    else:
                        stat_list[stat_list.index(stat)] = '-'
                i += 1
            pName = player.get_stats('Name')
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
