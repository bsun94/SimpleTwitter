"""
Created on Tue Aug 25 21:28:12 2020

Contains the user model class
"""

import tkinter as tk
import hashlib as hs
import sys

class userModel():
    
    def __init__(self, username, password):
        """
        Takes in username and password as parameters. Check is username is not empty, and if its len does not exceed 50 char,
        which is the limit in the db table.
        Password, if not None, is hashed here before being passed to the db.

        """
        if len(username) > 50:
            tk.messagebox.showerror('User Info Error', 'Username too long! Please limit usernames to 50 characters or below.')
            sys.exit()
        if not username:
            tk.messagebox.showerror('User Info Error', 'Please enter a username!')
            sys.exit()
        else:
            self.username = username
        
        if password:
            self.password = hs.sha3_256(str.encode(password)).hexdigest()
        else:
            tk.messagebox.showerror('User Info Error', 'Please enter a password!')
            sys.exit()

