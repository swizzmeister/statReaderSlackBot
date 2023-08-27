import slack
import os
import sys
import statInterpreter

client = slack.WebClient(token='XXX')
reader = statInterpreter.StatInterpreter('newTeamData.csv')
reader.load()
msg = reader.print_LeaderBoard('Lane Shuttle Left', False)
print(msg)
client.chat_postMessage(channel='#leaderboards', text=msg)
