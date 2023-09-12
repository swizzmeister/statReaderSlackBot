import csv
import datetime


class StatInterpreter:
    def __init__(self, path):
        self.players = {}
        self.cata = []
        self.path = path
        self.stat_blacklist = '-', '', 'Nr'

    def print(self):
        print(self.players)

    def load(self):
        self.players = {} #Store players in a dictionary where there number is there key
        self.cata = []#store catagorys in an array
        with open(self.path) as csv_file:
            lin = 0
            csv_reader = csv.reader(csv_file, delimiter=',') # parse the csv
            for line in csv_reader: # read the csv row by row
                if lin > 0:
                    if line[0] == "":
                        continue
                    self.players[line[0]] = {} #Index each new dictionary with the players number
                    i = 0
                    for l in line:
                        self.players[line[0]][self.cata[i]] = l #Index each stat with the string name of the catagory
                        i += 1
                else:
                    self.cata.append("Num") #If it's the catagory row make save the catagory into cata
                    for cat in line:
                        if cat:
                            self.cata.append(cat)
                lin += 1

    def getCatagories(self):
        return self.cata
    def getCatagorySum(self, stat):
        sum = 0
        for key in self.players.keys():
            p = self.players[key]
            if p[stat] in self.stat_blacklist or p['Name'] in self.stat_blacklist:
                continue
            elif "-" in p[stat]:
                stats = p[stat].split('-')
                stat = max(stats[0], stats[1])
                sum += (float(p[stat]))
            else:
                sum += float(p[stat])
        return round(sum, 2)
    def getCatagoryAvg(self,stat):
        sum =0
        stats_used =0
        for key in self.players.keys():
            p = self.players[key]
            if p[stat] in self.stat_blacklist or p['Name'] in self.stat_blacklist:
                continue
            elif "-" in p[stat]:
                stats = p[stat].split('-')
                stat = max(stats[0],stats[1])
                sum += float(p[stat])
                stats_used += 1
            else:
                sum += float(p[stat])
                stats_used += 1

        return round(sum/stats_used)


    def hasData(self):
        return len(self.players) > 0
    def sortLeaderboard(self, pList, ltg):  # ((Name,Stat),(Name,Stat)...etc)
        def partition(array, low, high):

            # choose the rightmost element as pivot
            pivot = array[high][1]

            # pointer for greater element
            i = low - 1

            # traverse through all elements
            # compare each element with pivot
            for j in range(low, high):
                if ltg:
                    if array[j][1] >= pivot:
                        i = i + 1
                        (array[i], array[j]) = (array[j], array[i])
                else:
                    if array[j][1] <= pivot:
                        i = i + 1
                        (array[i], array[j]) = (array[j], array[i])

            # Swap the pivot element with the greater element specified by i
            (array[i + 1], array[high]) = (array[high], array[i + 1])

            # Return the position from where partition is done
            return i + 1

        def quickSort(array, low, high):
            if low < high:
                # Find pivot element such that
                # element smaller than pivot are on the left
                # element greater than pivot are on the right
                pi = partition(array, low, high)

                # Recursive call on the left of pivot
                quickSort(array, low, pi - 1)

                # Recursive call on the right of pivot
                quickSort(array, pi + 1, high)

        quickSort(pList, 0, len(pList) - 1)
        return pList

    def get_Sorted_Leaderboard(self, stat, ltg):
        test = []
        for curPlayer in self.players.items(): #for every player
            cur_stat = curPlayer[1][stat]   #Take the stat in question and name
            cur_name = curPlayer[1]["Name"]
            if cur_stat in self.stat_blacklist or cur_name == 'Opponent': #Check if there stat is in the blacklist or there name
                continue #skip that player
            elif "-" in cur_stat:#if there are two stats split by '-' take the average and append that
                t_stat = cur_stat.split('-')
                avg = (float(t_stat[0]) + float(t_stat[1])) / 2
                test.append((cur_name, round(avg, 2)))
            else:
                test.append((cur_name, float(cur_stat)))
        return self.sortLeaderboard(test, ltg) # return a sorted 2D tuple

    def print_LeaderBoard(self, stat, ltg, unit, sum = False, avg = False, date = str(datetime.date.today())):
        sortedLeaderboard = self.get_Sorted_Leaderboard(stat, ltg) #Save current sorted leaderboard stored in tuples to sortedLeaderBoard
        pretty_print = "*   Ranked Average " + stat + " " + date + "*:\n"#Save heading into output string
        i = 1
        max = 0
        for player in sortedLeaderboard:
            if len(player[0]) > max: max = len(player[0])
        max += 4
        for player in sortedLeaderboard:
            space = ""
            space = ' ' * (max - len(player[0]))
            pretty_print += (">" + str(int(i)) + ". " + player[0] + space + str(player[1]) + " " + unit +"\n")
            i += 1
        if sum:
            pretty_print += (">Sum. "+ space + str(self.getCatagorySum(stat)) + " "  + unit +"\n")
        if avg:
            pretty_print += (">Average. " + space + str(self.getCatagoryAvg(stat)) + " " + unit + "\n")
        return pretty_print
