import array


class RowData:

    def __init__(self, cols, row_data):
        self.colData = row_data
        self.cols = cols
        self.num = row_data[cols[0]]

    def get_cells(self, stat):
        if type(stat) == str:
            return self.colData[stat]
        elif type(stat) == list:
            out = {}
            for s in stat:
                out[s] = self.colData[s]
            return out
        return 0

    def get_index(self):
        return self.num

    def __str__(self):
        out = "*/----/*\n"
        for c in self.cols:
            out += str(c) + ": " + self.colData[c] + "\n"
        out += "*/----/*"
        return out