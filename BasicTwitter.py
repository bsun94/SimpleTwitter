"""
Created on Tue Aug 11 18:16:43 2020

@author: Brian Sun

A fundamental version of Twitter using tkinter for UI and Google API for back-end data.
"""

import tkinter as tk
from datetime import datetime

class Twitter(object):
    
    root = tk.Tk()
    root.minsize(1000, 800)
    root.title('Welcome to Low-Budget Twitter!')
    root.configure(bg='#1DA1F2')
    root.iconphoto(False, tk.PhotoImage(file='logo.gif'))
    tk.Scrollbar(root).pack(side='right', fill='y')
    
    def __init__(self):
        self.tweet_msg = tk.StringVar()
        self.username = 'bsun94'
    
    def displayTweet(self, tweet, username, time):
        tk.Label(self.root, text=username, font='Arial 12 bold', justify='left', bg='#1DA1F2').pack(anchor='w', padx=12)
        tk.Label(self.root, text=time, font='Arial 8 italic', justify='left', bg='#1DA1F2').pack(anchor='w', padx=12)
        tk.Label(self.root, text=tweet, font='Arial 11', justify='left', bg='#1DA1F2').pack(anchor='w', padx=12, pady=5)
        
        # eventually will work on if statement checking for children
        tk.Button(self.root, text='See Conversation', state='disabled', height=1, width=15).pack(anchor='w', padx=12, pady=5)
    
    def getUserTweets(self):
        self.tweet_msg.set('Enter tweet here...')
        entry_bar = tk.Entry(self.root, textvariable=self.tweet_msg, font='Arial 12 italic', width=80)
        entry_bar.bind('<Button-1>', lambda event: entry_bar.delete(0, 'end'))
        entry_bar.pack(pady=20)
    
    def mainPage(self):
        self.getUserTweets()
        tk.Button(self.root, text='Tweet!', command=lambda: print(self.username, self.tweet_msg.get(), datetime.now()), height=2, width=15).pack(pady=5)
        
        tweets = [('Hello World', 'bsun94', '20200530'), 
                  ('I have milkshake', 'till_l', '20190503'), 
                  ('Reise, reise', 'angmerkel', '20200615'), 
                  ('All I ever wanted', 'eric_b', '20200130'), 
                  ('Stockholm', 'zaralarsson', '20180531'),]
        
        for tweet, user, date in tweets:
            self.displayTweet(tweet, user, date)
        
        self.root.mainloop()

twit1 = Twitter()
twit1.mainPage()
