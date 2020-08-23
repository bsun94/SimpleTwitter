"""
Created on Tue Aug 11 18:16:43 2020

@author: Brian Sun

A fundamental version of Twitter using tkinter for UI and Google API for back-end data.
"""

import tkinter as tk
from datetime import datetime
import hashlib as hs

class Controller(object):
        
    NUM_TWEETS = 10
    
    model = Model()
    view = View()
    
    def __init__(self):
        
        # base ("root") tkinter widget/window on which all other widgets are attached
        self.root = tk.Tk()
        self.root.minsize(1000, 800)
        self.root.maxsize(1200, 800)
        self.root.title('Welcome to Low-Budget Twitter!')
        self.root.iconphoto(False, tk.PhotoImage(file='logo.gif'))
        
        self.canvas = tk.Canvas(self.root, borderwidth=0, bg='#1DA1F2')
        self.frame = tk.Frame(self.canvas, bg='#1DA1F2')
        self.scroll = tk.Scrollbar(self.root, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll.set)
        
        self.scroll.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)
        self.canvas.create_window((480,4), window=self.frame, anchor='n', tags='self.frame', width=950)
        self.frame.bind('<Configure>', self.onFrameConfigure)
        
        self.tweet_msg = tk.StringVar()
        self.username = tk.StringVar()
    
    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    
    def clearPage(self, widget_type=None, exclude_names=None):
        if not widget_type:
            for widget in self.frame.winfo_children():
                widget.destroy()
        elif not exclude_names:
            for widget in self.frame.winfo_children():
                if widget.winfo_class() == widget_type:
                    widget.destroy()
        else:
            for widget in self.frame.winfo_children():
                if widget.winfo_class() == widget_type and widget.cget('text') not in exclude_names:
                    widget.destroy()
    
    def repliesPage(self, tweet_ID):
        self.clearPage()
        self.canvas.yview_moveto('0.0')
        
        self.view.getUserTweets(self.frame, self.tweet_msg)
        tk.Button(self.frame, text='Tweet!', 
                  command=lambda: [self.model.append([
                      self.model.getTweetID(), 
                      self.tweet_msg.get(), 
                      self.username.get(), 
                      datetime.now().strftime('%Y/%m/%d %H:%M'), 
                      tweet_ID
                      ]),
                      self.model.sortDB(),
                      self.frame.after_cancel(repliesAfter),
                      self.repliesPage(tweet_ID)
                      ],
                  height=1,
                  width=15).pack(pady=2)
        
        tk.Button(self.frame, text='Return!', 
                  command=lambda: [self.frame.after_cancel(repliesAfter),
                                   self.mainPage()],
                  height=1,
                  width=15).pack(pady=2)
        
        self.model.DBclear()
        self.model.DBquery(None, tweet_ID=tweet_ID)
        tweets = self.model.download()
        
        for _, tweet, user, date, _1 in tweets:
            self.view.displayTweet(self.frame, tweet, user, date)
        
        repliesAfter = self.frame.after(60000, lambda: self.repliesPage(tweet_ID))
    
    def mainPage(self):
        self.clearPage()
        self.canvas.yview_moveto('0.0')
        
        self.view.getUserTweets(self.frame, self.tweet_msg)
        tk.Button(self.frame, text='Tweet!', 
                  command=lambda: [self.model.append([
                      self.model.getTweetID(), 
                      self.tweet_msg.get(), 
                      self.username.get(), 
                      datetime.now().strftime('%Y/%m/%d %H:%M'), 
                      'None'
                      ]),
                      self.frame.after_cancel(mainAfter),
                      self.mainPage()
                      ],
                  height=2,
                  width=15).pack(pady=5)
        
        self.model.DBclear()
        # make num tweets a constant
        self.model.DBquery(self.NUM_TWEETS)
        tweets = self.model.download()
        
        for t_id, tweet, user, date, _ in tweets:
            self.view.displayTweet(self.frame, tweet, user, date)
            tk.Button(self.frame, text='See Conversation',
                      command=lambda t_id=t_id: [self.frame.after_cancel(mainAfter),
                                                 self.repliesPage(t_id)],
                      height=1,
                      width=15).pack(anchor='w', padx=12, pady=5)
        
        mainAfter = self.frame.after(60000, lambda: self.mainPage())
    
    def checkLogin(self, password):
        pw = self.model.getPassword(self.username.get())
        hash_pw = hs.sha3_256(str.encode(password)).hexdigest()
        
        if hash_pw == pw:
            self.mainPage()
        elif pw == '#N/A':
            tk.messagebox.showerror('Login Error', 'Username not recognized; please double-check entry, or create new account.')
        else:
            tk.messagebox.showerror('Login Error', 'Incorrect password! Please try again.')
    
    def checkRegistry(self, username, password):
        pw = self.model.getPassword(username)
        hash_pw = hs.sha3_256(str.encode(password)).hexdigest()
        
        if pw != '#N/A':
            tk.messagebox.showerror('Registration Error', 'Username already exists! Please try logging in without registration.')
        else:
            self.model.append([username, hash_pw])
            self.mainPage()
    
    def startup(self):
        password = tk.StringVar()
        logo = tk.PhotoImage(file="logo.gif").subsample(2, 2)
        tk.Label(self.frame, image=logo, borderwidth=0, highlightthickness=0).pack()
        self.view.loginEntry(self.frame, self.username, 'Enter username here...')
        self.view.loginEntry(self.frame, password, 'Enter password here...')
        
        tk.Button(self.frame, wraplength=150,
                  text='Register and login with above credentials',
                  command=lambda: self.checkRegistry(self.username.get(), password.get()),
                  height=2,
                  width=25).pack(pady=2)
        
        tk.Button(self.frame, wraplength=150,
                  text='Login to above account',
                  command=lambda: self.checkLogin(password.get()),
                  height=2,
                  width=25).pack(pady=2)
        
        self.root.mainloop()

control = Controller()
control.startup()
