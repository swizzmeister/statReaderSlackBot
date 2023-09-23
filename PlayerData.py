import array


class PlayerData:

    def __init__(self, cols, colData):
        self.colData = colData
        self.cols = cols
        self.OVR = float
        self.DEF = float
        self.OFF = float
        self.num = colData[cols[0]]

    def get_stats(self, stat):
        if type(stat) == str:
            return self.colData[stat]
        elif type(stat) == list:
            out = {}
            for s in stat:
                out[s] = self.colData[s]
            return out
        return 0

    def get_num(self):
        return self.num

    def __str__(self):
        out = "*/----/*\n"
        for c in self.cols:
            out += str(c) + ": " + self.colData[c] + "\n"
        out += "*/----/*"
        return out