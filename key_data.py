from sheetData import SheetData


class KeyData(SheetData):

    def __init__(self):
        SheetData.__init__(self)
        self.stats = {}
        for member in self:
            self.stats[member.get_stats('stat')] = member

    def hasStat(self, stat):
        if stat in self.stats.keys():
            return True
        return False

    def get_off_stats(self):
        out = []
        for member in self:
            if member.get_stats('Off/Deff') == 'Off':
                out.append(member)
        return out

    def get_def_stats(self):
        out = []
        for member in self:
            if member.get_stats('Off/Deff') == 'Deff':
                out.append(member)
        return out

    def get_weights(self, stat):
        if type(stat) == str:
            return self.stats[stat]
        elif type(stat) == list:
            out = {}
            for m in stat:
                out[m] = self.stats[m]
            return out

    def getPlayerStats(self, playerSheet):
        pNums = playerSheet.getPlayerNums()
        result = {}
        for num in pNums:
            player = playerSheet.getPlayer(num)
            offStats = []
            for stat in self.get_off_stats():
                offStats.append(player.getStats(stat)*self.get_weights(stat))
            defStats = []
            for stat in self.get_def_stats():
                defStats.append(player.getStats(stat) * self.get_weights(stat))
            Off = round(sum(offStats)/len(offStats), 2)
            Def = round(sum(defStats)/len(offStats), 2)
            result[num] = {'Ovr': Off + Def,'Off': Off,'Def': Def}
        return result


