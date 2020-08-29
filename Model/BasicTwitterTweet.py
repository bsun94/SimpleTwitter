"""
Created on Tue Aug 25 21:31:04 2020

Contains the tweet model class
"""

from datetime import datetime
import tkinter as tk
import sys

class tweetModel():
    
    def __init__(self, tweet, username, date, parent_id):
        """
        Validates tweet msgs, username, date and parent tweet id before passing it to db. Checks all parameters for blanks/Nones.
        Specifically, ensure that the date parameter is indeed a datetime object, and that parent_id is either None (for parent
        tweets) or an int for child tweets.

        """
        if not tweet:
            tk.messagebox.showerror('Tweet Error', 'Empty Tweet!')
            sys.exit()
        elif tweet.find("'") != -1:
            tweet = tweet.replace("'", "''")
            self.tweet = tweet
        else:
            self.tweet = tweet
        
        if not username:
            tk.messagebox.showerror('Tweet Error', 'Username not passed for database handling!')
            sys.exit()
        else:
            self.username = username
        
        if not isinstance(date, datetime):
            tk.messagebox.showerror('Tweet Error', 'Time of tweet creation not indicated!')
            sys.exit()
        else:
            self.date = date.strftime('%Y-%m-%d-%H.%M.%S')
        
        if parent_id != 'NULL' and not isinstance(parent_id, int):
            tk.messagebox.showerror('Tweet Error', 'Parent ID of the message either has to be "NULL", or an int!')
            sys.exit()
        else:
            self.parent_id = parent_id

