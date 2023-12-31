import csv
import datetime

from row_data import RowData


class SheetData(list):
    """
        Stores a list of RowData and can perform different methods upon said rowData
    """
    def __init__(self):
        super().__init__(self)
        self.cols = []
        self.calcCols = []
        self.stat_blacklist = '-', '', 'Nr'

    def hasData(self):
        if len(self) > 0:
            return True
        return False

    def load(self, path):
        """
            Loads a csv file of a specific format into class
        :param path:
        """
        with open(path) as csv_file:
            counter = 0
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if counter > 0:
                    if row[0] == '':  # Make sure the 0,0 is Empty to verify format
                        continue
                    i = 0
                    colData = {}
                    for item in row:
                        if len(item) > 1 and '-' in item and self.cols[i] != 'Name':
                            if item.split('-')[0] != '':
                                colData[self.cols[i]] = max(item[0], item[2])
                        colData[self.cols[i]] = item
                        i += 1
                    self.append(RowData(self.cols, colData))  #For each row save the data in another object called RowData
                else:
                    self.cols.append('Num') # On the first row read every column label and save them to local object
                    for cat in row:
                        if cat:
                            self.cols.append(cat)
                counter += 1

    def set_cols(self, cols):
        self.cols = cols

    def set_calc_Cols(self, CalcCols):
        self.calcCols = CalcCols

    def get_col_data(self, cols):  # returns in a
        result = {}
        for member in self:
            result[member.get_cells('Num')] = member.get_cells(cols)
        return result

    def get_calc_Cols(self):
        i = 0
        result = []
        while i < len(self.cols):
            try:
                float(self[0].get_cells(self.cols[i]))
            except:
                i += 1
                continue
            if self.cols[i] != 'Num':
                result.append(self.cols[i])
            i += 1
        return result

    def get_col_avg(self, stat, players=[]):
        sum = 0
        if len(players) == 0:
            for member in self:
                if member.get_cells(stat) not in self.stat_blacklist:
                    sum += float(member.get_cells(stat))
            return round((sum / len(self)), 2)
        else:

            for member in self.get_rows(players):
                if member.get_cells(stat) not in self.stat_blacklist:
                    sum += float(member.get_cells(stat))
            return round((sum / len(players)), 2)

    def get_col_sum(self, stat):
        sum = 0
        for member in self:
            if member.get_cells(stat) not in self.stat_blacklist:
                sum += float(member.get_cells(stat))
        return sum

    def get_rows(self, indices):
        if type(indices) == str:
            for member in self:
                if member.get_index() == indices:
                    return member
            return 0
        elif type(indices) == list:
            out = []
            for member in self:
                if member.get_index() in indices:
                    out.append(member)
            return out

    def row_indices(self):
        result = []
        for member in self:
            result.append(member.get_index())
        return result

    def sortLeaderboard(self, pList, ltg):  # ((index,Stat),(index,Stat)...etc)
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

    def get_Sorted_Leaderboard(self, stat: str, least_to_greatest: bool):
        """

        :param stat: defines the col to rank
        :param least_to_greatest: defines which way the list will be ranked
        :return: ((playerNum, stat), (playerNum, stat), ....)
        """
        result = []
        for member in self:
            if member.get_cells(stat) in self.stat_blacklist or member.get_cells(
                    'Name') == 'Opponent':  # Check if there stat is in the blacklist or there name
                continue  # skip that player
            else:
                result.append((member.get_cells('Num'), float(member.get_cells(stat))))

        return self.sortLeaderboard(result, least_to_greatest)

    def printLeaderboard(self, stat, least_to_greatest, unit, sum=False, avg=False, date=str(datetime.date.today)):
        sortedLeaderboard = self.get_Sorted_Leaderboard(stat, least_to_greatest)
        pretty_print = "*   Ranked Average " + stat + " " + date + "*:\n"
        i = 1
        max = 0
        for player in sortedLeaderboard:
            name = len(self.get_rows(player[0]).get_cells('Name'))
            if name > max: max = name
        max += 4
        for player in sortedLeaderboard:
            name = self.get_rows(player[0]).get_cells('Name')
            space = ' ' * (max - len(name))
            pretty_print += (">" + str(int(i)) + ". " + name + space + str(player[1]) + " " + unit + "\n")
            i += 1
        if sum:
            pretty_print += (">Sum. " + space + str(self.get_col_sum(stat)) + " " + unit + "\n")
        if avg:
            pretty_print += (">Average. " + space + str(self.get_col_avg(stat)) + " " + unit + "\n")
        return pretty_print
