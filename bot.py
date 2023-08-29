from slack import WebClient
import os
import sys
import statInterpreter


client = WebClient(token='XXX')
reader = statInterpreter.StatInterpreter('newTeamData.csv')
reader.load()
msg = reader.print_LeaderBoard('Lane Shuttle Left', False, 'sec')
print(msg)
client.chat_postMessage(channel='#random', text=msg)
