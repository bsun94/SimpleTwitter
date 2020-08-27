"""
Created on Tue Aug 11 18:16:43 2020

@author: Brian Sun

A fundamental version of Twitter using tkinter for UI and IBM DB2 for back-end data.
"""

import tkinter as tk
import os

# For importing custom model and view modules - please ensure you've saved all these files in the same directory!
os.chdir(os.getcwd())

import BasicTwitterDB as dt
import BasicTwitterView as vw
import BasicTwitterMain as mn
import BasicTwitterReplies as rep
import BasicTwitterEnum as en

class Controller(object):
    
    # Controls the number of (most recent) tweets loaded on the GUI
    # current only applied to the display of parent tweets on the mainPage
    NUM_TWEETS = 10
    
    def __init__(self):
        """
        Defines the base widget onto which all other widgets (labels, buttons, etc.) are attached.
        In addition to the tkinter Tk() root, a canvas & frame base widget is used to allow for better scrolling.

        Database handler and view class instances are defined here. Username, a tk stringVar, is initialized here to allow
        for transference across all methods. Tweet_msg initialized here to save on code - mainPage and repliesPage tweets are,
        by structure, guaranteed to be separated.        

        """
        self.root = tk.Tk()
        self.root.minsize(1000, 800)
        self.root.maxsize(1000, 800)
        self.root.title('Welcome to Low-Budget Twitter!')
        self.root.iconphoto(False, tk.PhotoImage(file='logo.gif'))
        
        self.canvas = tk.Canvas(self.root, borderwidth=0, bg='#1DA1F2')
        self.frame = tk.Frame(self.canvas, bg='#1DA1F2')
        self.scroll = tk.Scrollbar(self.root, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll.set)
        
        self.scroll.pack(side='right', fill='y')
        self.canvas.pack(fill='both', expand=True)
        
        x0 = self.frame.winfo_screenwidth() / 2
        self.canvas.create_window((x0,5), window=self.frame, anchor='n', tags='self.frame', width=950)
        self.frame.bind('<Configure>', self.onFrameConfigure)
        
        self.tweet_msg = tk.StringVar()
        self.username = tk.StringVar()
        
        self.db = dt.DBHandler()
        self.view = vw.View(self.frame)
        self.replies = rep.RepliesController(self.frame, self.canvas, self.tweet_msg, self.username)
        self.main = mn.MainController(self.frame, self.canvas, self.tweet_msg, self.username, self.replies.repliesPage)
    
    def onFrameConfigure(self, event):
        """
        Mostly used to defined portion of tk.canvas (constituent of base widget) that is scrollable.
        
        """
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    
    def checkLogin(self, username, password):
        """
        Checks the login credentials - username and password - the user has inputted against database records.
        Upon verification, opens up the mainPage.

        """
        pw = self.db.getPassword(username, password)
        
        if pw == en.States.verified:
            self.main.mainPage()
        elif pw == en.States.user_err:
            tk.messagebox.showerror('Login Error', 'Username not recognized; please double-check entry, or create new account.')
        elif pw == en.States.pw_err:
            tk.messagebox.showerror('Login Error', 'Incorrect password! Please try again.')
    
    def checkRegistry(self, username, password):
        """
        Checks if username already exists before proceeding with user registration into db.
        Upon successful registration, opens up the mainPage.

        """
        pw = self.db.getPassword(username, password)
        
        if pw != en.States.user_err:
            tk.messagebox.showerror('Registration Error', 'Username already exists! Please try logging in without registration.')
        else:
            self.db.addUser(username, password)
            self.mn.mainPage()
    
    def startup(self):
        """
        Contains the tkinter mainloop on which the application runs.
        Displays the registry and login buttons, whose linked methods directs the user to the rest of the application's
        features and functions.

        """
        password = tk.StringVar()
        logo = tk.PhotoImage(file="logo.gif")
        tk.Label(self.frame, image=logo, borderwidth=0, highlightthickness=0).pack()
        self.view.loginEntry(self.username, 'Enter username here (limit 50 characters)...')
        self.view.loginEntry(password, 'Enter password here...')
        
        tk.Button(self.frame, wraplength=150,
                  text='Register and login with above credentials',
                  command=lambda: self.checkRegistry(self.username.get(), password.get()),
                  height=2,
                  width=25).pack(pady=2)
        
        tk.Button(self.frame, wraplength=150,
                  text='Login to above account',
                  command=lambda: self.checkLogin(self.username.get(), password.get()),
                  height=2,
                  width=25).pack(pady=2)
        
        self.root.mainloop()


control = Controller()
control.startup()
