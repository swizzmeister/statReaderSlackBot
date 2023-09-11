import ssl
import tkinter as tk
from tkinter import ttk

import certifi
import slack


class slackAddFrame(tk.Frame):
    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.root = root
        self.slack_key_entry = tk.StringVar()
        self.slack_key_entry.set("Hello")
        self.slack_channel_entry = tk.StringVar()
        l = ttk.Label(self, text="Slack Key:")
        self.key = ttk.Entry(self, textvariable=self.slack_key_entry)
        l.grid(row=0, column=0, padx=20, pady=10)
        self.key.grid(row=0, column=1, padx=20, pady=10)
        l = ttk.Label(self, text="Channel:")
        self.channel = ttk.Entry(self, textvariable=self.slack_channel_entry)
        l.grid(row=1, column=0, padx=20, pady=10)
        self.channel.grid(row=1, column=1, padx=20, pady=10)
        button1 = ttk.Button(self,
                             text="Set Key",
                             command=lambda: self.assign_slack_key())
        button1.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

    def assign_slack_key(self):
        self.root.set_slack_key = self.key.get()
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.root.CLIENT = slack.WebClient(token=self.key.get(), ssl=ssl_context)
        self.root.CHANNEL = self.channel.get()
        if self.root.CLIENT.api_test()['ok'] and self.root.CLIENT.auth_test()['ok']:
            self.root.ACTIVE = True
        self.parent.destroy()
