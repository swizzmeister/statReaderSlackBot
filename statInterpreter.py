import csv


class StatInterpreter:
    def __init__(self, path):
        self.players = {}
        self.cata = []
        with open(path) as csv_file:
            lin = 0
            csv_reader = csv.reader(csv_file, delimiter=',')
            for line in csv_reader:
                print(line)
                if lin > 0:
                    self.players[line[0]] = {}
                    i = 0
                    for l in line:
                        self.players[line[0]][ self.cata[i]] = l
                        i += 1
                else:
                    self.cata.append("Num")
                    print(len(line))
                    for cat in line:
                        if cat:
                            print(cat)
                            self.cata.append(cat)
                lin += 1

    def print(self):
        print(self.players)
    def getCatagories(self):
        return self.cata
    def sortLeaderboard(self, pList): #((Name,Stat),(Name,Stat)...etc)
        def partition(array, low, high):

            # choose the rightmost element as pivot
            pivot = array[high][1]

            # pointer for greater element
            i = low - 1

            # traverse through all elements
            # compare each element with pivot
            for j in range(low, high):
                if array[j][1] >= pivot:
                    # If element smaller than pivot is found
                    # swap it with the greater element pointed by i
                    i = i + 1

                    # Swapping element at i with element at j
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
        quickSort(pList,0,len(pList)-1)
        return pList
    def print_LeaderBoard(self,stat):
        print("running")
       # activePlayerNames = {}
       # activePlayerStats = []
        test= []
        for curPlayer in self.players.items():
            curStat = curPlayer[1][stat]
            curName = curPlayer[1]["Name"]
            print(curStat)
            if curStat == "-" or curName == 'Opponent':
                print(curName)
                continue
            elif "-" in curStat:
                tStat = curStat.split('-')
                print(tStat)
                avg = (float(tStat[0])+float(tStat[1]))/2
                test.append((curName,round(avg,2)))
            else:
                test.append((curName, float(curStat)))
                print(curName)
       # activePlayerStats.sort()
        print(test)
        sortedLeaderboard = self.sortLeaderboard(test)
        pretty_print = "*   Ranked " + stat + "*:\n"
        print(sortedLeaderboard)
        i =1
        max=0
        for player in sortedLeaderboard:
            if len(player[0]) > max: max = len(player[0])
        max += 4
        print(max)
        for player in sortedLeaderboard:
            space = ""
            space = ' ' * (max - len(player[0]))
            pretty_print += (">" + str(int(i)) + ". " + player[0] + space + str(player[1]) + " " + stat + "\n")
            i+=1
        print(pretty_print)
        return pretty_print





interpret = StatInterpreter("upei_lineups.csv")
interpret.print()
interpret.print_LeaderBoard("fg/g")
