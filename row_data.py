import array


class RowData:

    def __init__(self, cols, row_data):
        self.colData = row_data
        self.cols = cols
        self.num = row_data[cols[0]]

    def get_cells(self, stat: list | str) -> dict | str:
        """
        Will return cell data
        :param stat: stat(s) to be returned
        :return: data from chosen col(s)
        """
        if type(stat) == str:
            return self.colData[stat]
        elif type(stat) == list:
            out = {}
            for s in stat:
                out[s] = self.colData[s]
            return out
        return 0

    def get_index(self) -> str:
        """

        :return: first item of row
        """
        return self.num

    def __str__(self):
        out = "Name: " + self.colData['Name']
        return out
