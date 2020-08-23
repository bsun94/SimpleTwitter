"""
Created on Sat Aug 22 16:33:17 2020

Contains the View portion of BasicTwitterBQ
"""

import tkinter as tk

# TODO: input checks on all the methods
class View():
    
    def displayTweet(self, root, tweet, username, date):
        tk.Label(root, text=username, font='Arial 12 bold', justify='left', fg='#1DA1F2', bg='white').pack(anchor='w', padx=12)
        tk.Label(root, text=date, font='Arial 8 italic', justify='left', bg='#1DA1F2').pack(anchor='w', padx=12)
        tk.Label(root, text=tweet, font='Arial 11', justify='left', bg='#1DA1F2').pack(anchor='w', padx=12, pady=5)
    
    def getUserTweets(self, root, msg):
        msg.set('Enter tweet here...')
        entry_bar = tk.Entry(root, textvariable=msg, font='Arial 12 italic', width=80)
        entry_bar.bind('<Button-1>', lambda event: entry_bar.delete(0, 'end'))
        entry_bar.pack(pady=20)
    
    def loginEntry(self, root, cred, prompt):
        cred.set(prompt)
        entry_bar = tk.Entry(root, textvariable=cred, font='Arial 12', width=40)
        entry_bar.bind('<Button-1>', lambda event: entry_bar.delete(0, 'end'))
        entry_bar.pack(anchor='s', pady=15)
