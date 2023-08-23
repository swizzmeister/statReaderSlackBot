import csv


class StatInterpreter:
    def __init__(self, path):
        self.players = {}
        with open(path) as csv_file:
            lin = 0
            var = []
            csv_reader = csv.reader(csv_file, delimiter=',')
            for line in csv_reader:
                print(line)
                if lin > 0:
                    self.players[line[0]] = {}
                    i = 0
                    for l in line:
                        self.players[line[0]][var[i]] = l
                        i += 1
                else:
                    var.append("Num")
                    print(len(line))
                    for cat in line:
                        if cat:
                            print(cat)
                            var.append(cat)
                lin += 1

    def print(self):
        print(self.players)
    def sortLeaderboard(self, pList): #((Name,Stat),(Name,Stat)...etc)
        def partition(array, low, high):

            # choose the rightmost element as pivot
            pivot = array[high][1]

            # pointer for greater element
            i = low - 1

            # traverse through all elements
            # compare each element with pivot
            for j in range(low, high):
                if array[j][1] <= pivot:
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
    def print_LeaderBoard(self,stats = []):
        print("running")
       # activePlayerNames = {}
       # activePlayerStats = []
        test=()
        for stat in stats:
            for curPlayer in self.players:
                curStat = curPlayer[stat]
                if curStat == "-":
                    continue
                elif "-" in curStat:
                    tStat = curStat.split('-')
                    avg = (float(tStat[0])+float(tStat[1]))/2
                  #  activePlayerNames[avg] = curPlayer['Name']
                   # activePlayerStats.append(avg)
                    test.append(curPlayer[1],avg)
                else:
                   # activePlayerNames[curPlayer[stat]] = curPlayer['Name']
                    #activePlayerStats.append(curPlayer[stat])
                    test.append(curPlayer[1], avg)
       # activePlayerStats.sort()
        sortedLeaderboard = self.sortLeaderboard(test)
        pretty_print = "Current Leaderboard:\n"
        print(sortedLeaderboard)





interpret = StatInterpreter("upei_lineups.csv")
interpret.print()
interpret.print_LeaderBoard("min/g")