import csv
import datetime

from PlayerData import PlayerData


class SheetData(list):

    def __init__(self):
        super().__init__(self)
        self.cols = []
        self.calcCols = []
        self.stat_blacklist = '-', '', 'Nr'

    def load(self, path):
        with open(path) as csv_file:
            counter = 0
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if counter > 0:
                    if row[0] == '':
                        continue
                    i = 0
                    colData = {}
                    for item in row:
                        if len(item) > 1 and '-' in item and self.cols[i] != 'Name':
                            if item.split('-')[0] != '':
                                colData[self.cols[i]] = max(item[0], item[2])
                        colData[self.cols[i]] = item
                        i += 1
                    self.append(PlayerData(self.cols, colData))
                else:
                    self.cols.append('Num')
                    for cat in row:
                        if cat:
                            self.cols.append(cat)
                counter += 1

    def set_cols(self, cols):
        self.cols = cols

    def set_calc_Cols(self, CalcCols):
        self.calcCols = CalcCols

    def get_col_data(self, cols):#returns in a
        result = {}
        for member in self:
            result[member.get_stats('Num')] = member.get_stats(cols)
        return result



    def get_calc_Cols(self):
        i = 0
        result = []
        while i < len(self.cols):
            try:
                float(self[0].get_stats(self.cols[i]))
            except:
                i += 1
                continue
            if self.cols[i] != 'Num':
                result.append(self.cols[i])
            i += 1
        return result

    def get_col_avg(self, stat, players=[]):
        sum = 0
        if len(players)==0:
            for member in self:
                if member.get_stats(stat) not in self.stat_blacklist:
                    sum += float(member.get_stats(stat))
            return round((sum / len(self)), 2)
        else:

            for member in self.getPlayers(players):
                if member.get_stats(stat) not in self.stat_blacklist:
                    sum += float(member.get_stats(stat))
            return round((sum / len(players)), 2)
    def get_col_sum(self, stat):
        sum = 0
        for member in self:
            if member.get_stats(stat) not in self.stat_blacklist:
                sum += float(member.get_stats(stat))
        return sum

    def getPlayer(self, num):
        for member in self:
            if member.get_num() == num:
                return member
        return 0
    def getPlayers(self, nums):
        out = []
        for member in self:
            if member.get_num() in nums:
                out.append(member)
        return out

    def getPlayerNums(self):
        result = []
        for member in self:
            result.append(member.get_num)
        return result

    def sortLeaderboard(self, pList, ltg):  # ((Name,Stat),(Name,Stat)...etc)
        def partition(array, low, high):
            pivot = array[high][1]
            i = low - 1
            for j in range(low, high):
                if ltg:
                    if array[j][1] >= pivot:
                        i = i + 1
                        (array[i], array[j]) = (array[j], array[i])
                else:
                    if array[j][1] <= pivot:
                        i = i + 1
                        (array[i], array[j]) = (array[j], array[i])
            (array[i + 1], array[high]) = (array[high], array[i + 1])
            return i + 1

        def quickSort(array, low, high):
            if low < high:
                pi = partition(array, low, high)
                quickSort(array, low, pi - 1)
                quickSort(array, pi + 1, high)

        quickSort(pList, 0, len(pList) - 1)
        return pList

    def get_Sorted_Leaderboard(self, stat, least_to_greatest):
        result = []
        for member in self:
            if member.get_stats(stat) in self.stat_blacklist or member.get_stats('Name') == 'Opponent':  # Check if there stat is in the blacklist or there name
                continue  # skip that player
            else:
                result.append((member.get_stats('Name'), float(member.get_stats(stat))))

        return self.sortLeaderboard(result, least_to_greatest)

    def printLeaderboard(self, stat, least_to_greatest, unit, sum=False, avg=False, date=str(datetime.date.today)):
        sortedLeaderboard = self.get_Sorted_Leaderboard(stat, least_to_greatest)
        pretty_print = "*   Ranked Average " + stat + " " + date + "*:\n"
        i = 1
        max = 0
        for player in sortedLeaderboard:
            if len(player[0]) > max: max = len(player[0])
        max += 4
        for player in sortedLeaderboard:
            space = ' ' * (max - len(player[0]))
            pretty_print += (">" + str(int(i)) + ". " + player[0] + space + str(player[1]) + " " + unit + "\n")
            i += 1
        if sum:
            pretty_print += (">Sum. " + space + str(self.get_col_sum(stat)) + " " + unit + "\n")
        if avg:
            pretty_print += (">Average. " + space + str(self.get_col_avg(stat)) + " " + unit + "\n")
        return pretty_print
