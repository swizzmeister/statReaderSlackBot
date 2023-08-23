import slack
import os

client = slack.WebClient(token='xoxb-5090655667488-5801495975025-r2azMqHQJ9gGviWT6NvUQxDU')
client.chat_postMessage(channel="#random", text="\tCurrent Leaders\n\t\t#1 Logan\n\t\t#2 Logan")