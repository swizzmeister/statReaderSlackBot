import slack
import os
import sys
import statInterpreter

client = slack.WebClient(token='xoxb-5090655667488-5801495975025-WOfYgxv0IAWTfrrvqRUakJ17')
if len(sys.argv) < 2:
    interpret = statInterpreter.StatInterpreter("upei_lineups.csv")
    catagories = interpret.getCatagories()
    badCat = ['Name', 'Yr', 'Pos']
    for stat in catagories:
        if stat not in badCat:
            client.chat_postMessage(channel="#random", text=interpret.print_LeaderBoard(stat))
elif len(sys.argv) == 2:
    client.chat_postMessage(channel="#random", text=interpret.print_LeaderBoard(argv[1]))
else:
    for x in sys.argv:
        if '.' not in x:
            client.chat_postMessage(channel="#random", text=interpret.print_LeaderBoard(x))
