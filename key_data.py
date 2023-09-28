from sheetData import SheetData


class KeyData(SheetData):
    """
        Child class of SheetData, contains and provides key information and functionality on based key stat information
    """

    def __init__(self):
        SheetData.__init__(self)

    def get_off_stats(self) -> list:
        """

        :return: List of Offensive stat
        """
        out = []
        for member in self:
            if member.get_cells('Off/Deff') == 'Off':
                out.append(member)
        return out

    def get_def_stats(self) -> list:
        """

        :return: List of defensive stats
        """
        out = []
        for member in self:
            if member.get_cells('Off/Deff') == 'Deff':
                out.append(member)
        return out

    def get_weights(self, stat_name: str | list) -> str | dict:
        """

        :param stat_name: Name of stat(s) querying weights
        :return: Weight(s) for desired stat(s)
        """
        if type(stat_name) == str:
            for stat in self:
                if stat.get_cells('stat') == stat_name:
                    return stat.get_cells('weights')
        elif type(stat_name) == list:
            out = {}
            for m in self:
                if m.get_cells('stat') in stat_name:
                    out[m.get_cells('stat')] = m.get_cells('weights')
            return out

    def statGtL(self, stat):
        """

        :param stat: name of stat you want GtL for
        :return: boolean True of Greatest to Least
        """
        for m in self:
            if m.get_cells('stat') == stat:
                return int(m.get_cells('GtL'))

    def getPlayerStats(self, player_sheet: SheetData) -> dict:
        """
        Gets the weighted values for each player using the csv key
        :param player_sheet: All current players
        :return: unsorted dict[num] = {Ovr, Off, Def}
        """
        pNums = player_sheet.row_indices()
        result = {}
        for num in pNums:
            player = player_sheet.get_rows(num)
            offStats = []
            for stat in self.get_off_stats():
                offStats.append(
                    float(player.get_cells(stat.get_cells('stat'))) * float(self.get_weights(stat.get_cells('stat'))))
            defStats = []
            for stat in self.get_def_stats():
                defStats.append(
                    float(player.get_cells(stat.get_cells('stat'))) * float(self.get_weights(stat.get_cells('stat'))))
            Off = round(sum(offStats), 2)
            Def = round(sum(defStats), 2)
            result[num] = {'Ovr': Off + Def, 'Off': Off, 'Def': Def}
        return result

    def getPlayerOvrRank(self, player_sheet: SheetData) -> list:
        """
        Gets a sorted list of player numbers based of off the weighted score on the key
        :param player_sheet: All current players
        :return: A sorted list off all players
        """
        player_stats = self.getPlayerStats(player_sheet)
        numList = []
        for num in player_stats.keys():
            ovr = player_stats[num]['Ovr']
            if len(numList) == 0:
                numList.append(num)
            elif len(numList) > 0:
                found = 0
                for i in range(0, len(numList)):
                    if float(player_stats[numList[i]]['Ovr']) <= float(ovr):
                        numList.insert(i, num);
                        found = 1
                        break
                if not found: numList.append(num)
        return numList
