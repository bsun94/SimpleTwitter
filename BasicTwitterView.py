"""
Created on Sat Aug 22 16:33:17 2020

Contains the View portion of BasicTwitterBQ
"""

import tkinter as tk
import sys

class View():
    
    def __init__(self, root):
        """
        Reads in the root/base widget onto which to apply all the below view components to a window.

        """
        self.root = root
    
    def displayTweet(self, tweet, username, date):
        """
        Basic format to display tweets/messages comprising the username, time stamp and actual message.

        """
        tk.Label(self.root, text=username, font='Arial 12 bold', justify='left', fg='#1DA1F2', bg='white').pack(anchor='w', padx=12)
        tk.Label(self.root, text=date, font='Arial 8 italic', justify='left', bg='#1DA1F2').pack(anchor='w', padx=12)
        tk.Label(self.root, text=tweet, font='Arial 11', justify='left', bg='#1DA1F2').pack(anchor='w', padx=12, pady=5)
    
    def getUserTweets(self, msg):
        """
        Entry bar with formatting specific to the non-login pages. Event handler bound to the bar to clear current text whenever
        the user clicks into the bar to re-type.

        """
        if not isinstance(msg, tk.StringVar):
            sys.exit('Please provide a tk stringvar to which the entry box can be linked!')
        
        msg.set('Enter tweet here...')
        entry_bar = tk.Entry(self.root, textvariable=msg, font='Arial 12 italic', width=80)
        entry_bar.bind('<Button-1>', lambda event: entry_bar.delete(0, 'end'))
        entry_bar.pack(pady=20)
    
    def loginEntry(self, cred, prompt):
        """
        Grabs user input with formatting specific to the login landing page. Event handler bound to clear text whenever the user
        clicks into the bar to re-type.

        """
        if not isinstance(cred, tk.StringVar):
            sys.exit('Please provide a tk stringvar to which the entry box can be linked!')
            
        cred.set(prompt)
        entry_bar = tk.Entry(self.root, textvariable=cred, font='Arial 12', width=40)
        entry_bar.bind('<Button-1>', lambda event: entry_bar.delete(0, 'end'))
        entry_bar.pack(anchor='s', pady=15)
    
    def clearPage(self, widget_type=None, exclude_names=None):
        """
        Used to clear a base widget to (re)build a window. Can specify widget_type to clear a specific type of widget, and if a
        excludes_names *list* is provided, specifically removes those widgets whose text labels falls within that list.

        """
        if not widget_type:
            for widget in self.root.winfo_children():
                widget.destroy()
        elif not exclude_names:
            for widget in self.root.winfo_children():
                if widget.winfo_class() == widget_type:
                    widget.destroy()
        else:
            for widget in self.root.winfo_children():
                if widget.winfo_class() == widget_type and widget.cget('text') not in exclude_names:
                    widget.destroy()
