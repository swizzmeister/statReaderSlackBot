import slack
import os
import sys
import statInterpreter

client = slack.WebClient(token='XXX')
reader = statInterpreter.StatInterpreter('teamdata.csv')
reader.load()
msg = reader.print_LeaderBoard('Max Vert', True)
print(msg)
client.chat_postMessage(channel='#leaderboards', text=msg)
