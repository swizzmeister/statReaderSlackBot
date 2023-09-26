from sheetData import SheetData


class KeyData(SheetData):

    def __init__(self):
        SheetData.__init__(self)

    def get_off_stats(self):
        out = []
        for member in self:
            if member.get_cells('Off/Deff') == 'Off':
                out.append(member)
        return out

    def get_def_stats(self):
        out = []
        for member in self:
            if member.get_cells('Off/Deff') == 'Deff':
                out.append(member)
        return out

    def get_weights(self, stat_name):
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
        for m in self:
            if m.get_cells('stat')==stat:
                return int(m.get_cells('GtL'))

    def getPlayerStats(self, playerSheet):
        pNums = playerSheet.row_indices()
        result = {}
        for num in pNums:
            player = playerSheet.get_rows(num)
            offStats = []
            for stat in self.get_off_stats():
                offStats.append(float(player.get_cells(stat.get_cells('stat')))* float(self.get_weights(stat.get_cells('stat'))))
            defStats = []
            for stat in self.get_def_stats():
                defStats.append(float(player.get_cells(stat.get_cells('stat'))) * float(self.get_weights(stat.get_cells('stat'))))
            Off = round(sum(offStats)/len(offStats), 2)
            Def = round(sum(defStats)/len(offStats), 2)
            result[num] = {'Ovr': Off + Def,'Off': Off,'Def': Def}
        return result


    def getPlayerOvrRank(self, playerSheet):
        playerstats = self.getPlayerStats(playerSheet)
        numList = []
        for num in playerstats.keys():
            ovr = playerstats[num]['Ovr']
            if len(numList) == 0:
                numList.append(num)
            elif len(numList)>0:
                for i in range(0, len(numList)):
                    if float(playerstats[numList[i]]['Ovr']) <= float(ovr):
                        numList.insert(i, num)
                        break
        return numList
