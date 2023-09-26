import tkinter as tk
from tkinter import Listbox, ttk, messagebox, filedialog

import mysql
from PIL import Image, ImageTk

from Frames.empty_frame import EmptyFrame
from image_write import ImageWrite
from key_data import KeyData


class WeightedStatOutput(tk.Frame):

    def __init__(self, parent, controller: tk.Tk):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.sheet_data = object
        self.key_sheet_data = KeyData()
        self.outputImagePath = ""
        self.key_name = ""
        self.image_path = ""
        self.label = ttk.Label(self, text="Error", font=controller.LARGEFONT)
        self.label.pack(side=tk.TOP)
        # Key Entry
        list_lf = ttk.Labelframe(self, text='Stat Key')
        list_lf.pack()
        self.lbl_key = ttk.Label(list_lf, text="Please enter a key")
        btn_key = ttk.Button(list_lf, text="Get key csv", command=lambda: self.get_key())
        btn_key.grid(column=0, row=0, padx=10, pady=10)
        self.lbl_key.grid(column=1, row=0, padx=10, pady=10)
        # Players to contact
        self.list = []

    def get_key(self):
        path = filedialog.askopenfilename(initialdir='C:\\Users\\Logan\\Desktop',
                                          title="Select a csv Stat File",
                                          filetypes=(("CSV files",
                                                      "*.csv"),
                                                     ("all files",
                                                      "*.*")))
        self.key_sheet_data.load(path)
        self.key_name = path.split('/')[-1]
        self.lbl_key.configure(text="Found key: " + str(self.key_name))
        rank_list = self.key_sheet_data.getPlayerOvrRank(self.controller.SHEET)
        print('Rank List', rank_list)
        fullRankList = rank_list
        stat_list = self.key_sheet_data.getPlayerStats(self.controller.SHEET)
        if len(rank_list) > 5:
            rank_list = rank_list[:5]
        key_data = []
        for num in rank_list:
            key_data.append((round(stat_list[num]["Ovr"]), self.controller.SHEET.get_rows(num).get_cells('Name'),
                             round(stat_list[num]["Def"]), round(stat_list[num]["Off"])))
        i = ImageWrite(key_data)
        print(i.get_img_path())
        image = Image.open(i.get_img_path())
        image = image.resize((250, 300))
        image_tk = ImageTk.PhotoImage(master=self, image=image)
        label = ttk.Label(self, image=image_tk)
        self.outputImagePath = i.get_img_path()
        label.image = image_tk
        label.pack(pady=15)
        self.getPlayerUserIDs(fullRankList)

    def load_sheet(self, filename: str, sheet):
        """
        :param filename: String name of
        :param sheet:
        """
        if sheet.hasData():
            self.sheet_data = sheet
            self.label.configure(text=filename + " weighted output", foreground="grey")
            self.controller.show_frame(WeightedStatOutput)
        else:
            messagebox.showwarning('CSV Error', 'Please open a .csv')
            self.controller.show_frame(EmptyFrame)

    def getPlayerRankedOutput(self, num):
        """

        :param num: number of player
        :return: dict[stat] = (rank, value)
        """
        stats = self.key_sheet_data.get_col_data('stat')
        stats = stats.items()
        print(stats)
        out = {}
        for s in stats:
            x = self.controller.SHEET.get_Sorted_Leaderboard(s[1], self.key_sheet_data.statGtL(s[1]))
            for i in range(0, len(x)-1):
                if int(x[i][0]) == num:
                    out[s[1]] = (str(i+1), str(x[i][1]))
        return out

    def pp_PlayerRankedOutput(self, num):
        """

        :param num: number of player
        :return: pretty print of players stats
        """
        stat = self.getPlayerRankedOutput(num)
        name = self.controller.SHEET.get_rows(str(num)).get_cells('Name')
        out = name + (" <event> <date> \n"
                      "Stat, Rank, Value\n")
        print(stat, name)
        for k in stat.keys():
            stats = stat[k]
            print(stats)
            out += ">" + str(k) + " " + str(stats[0]) + " " + str(stats[1]) + "\n"
        return out


    def getPlayerUserIDs(self, player_numbers: list) -> dict:
        """

        :param player_numbers: List of player numbers
        :return: out: dict[num]=playerUserID
        """
        mydb = mysql.connector.connect(
            host=self.controller.endpoint,
            user='dbmasteruser',
            password='SaltAndPepper14',
            database='dbmaster'
        )
        strOut = str(player_numbers)
        strOut = "(" + strOut.strip('[]') + ")"
        sql = "SELECT num,slackUserID FROM player WHERE num IN " + strOut + ";"
        print(sql)
        cursor = mydb.cursor()
        cursor.execute(sql)
        r = cursor.fetchall()
        out = {}
        for x in r:
            out[x[0]] = x[1]
        return out

