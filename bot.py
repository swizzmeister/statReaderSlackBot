from slack import WebClient
import os
import sys
import statInterpreter


client = WebClient(token='xoxb-5090655667488-5801495975025-c2OLHu6puJJcBqYa8Utpnf2n')
reader = statInterpreter.StatInterpreter('newTeamData.csv')
reader.load()
msg = reader.print_LeaderBoard('Lane Shuttle Left', False, 'sec')
print(msg)
client.chat_postMessage(channel='#random', text=msg)
