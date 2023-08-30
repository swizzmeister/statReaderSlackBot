from slack import WebClient
import os
import sys
import statInterpreter

class Bot(WebClient):
    def __init__(self, token):
        self.__init__(token)
    def is_running(self):
        return '"ok":true' in self.api_test()

    def post_message(self,channel,text):
        self.chat_postMessage(channel=channel, text=text)
#client = WebClient(token='XXX')
#reader = statInterpreter.StatInterpreter('newTeamData.csv')
#reader.load()
#msg = reader.print_LeaderBoard('Lane Shuttle Left', False, 'sec')
#print(msg)
#client.chat_postMessage(channel='#random', text=msg)
