"""
Created on Tue Aug 11 18:16:43 2020

@author: Brian Sun

A fundamental version of Twitter using tkinter for UI and Google API for back-end data.
"""

import tkinter as tk
from datetime import datetime
import os
import sys
import pickle as pk
import hashlib as hs
from googleapiclient.discovery import build

# TODO: put MVC in diff files
class View(object):
    
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
    

class Model(object):
    
    os.chdir(os.getcwd())  # TODO: inside a method
    SPREADSHEET_ID = '1sLf9UMIP7MdWbcuS9qh3blkpsPBJzkIfZSlTuQ0Ltqg'   # model does not need to know DB
    TWEETS_RANGE = 'Tweets'
    QUERY_RANGE = 'Queries'
    USERS_RANGE = 'Logins'
    TWEET_ID = 'Parameters!B1'
        
    with open('token.pickle', 'rb') as creds:
        CREDENTIALS = pk.load(creds)  # TODO: inside a method
    
    try:
        SERVICE = build('sheets', 'v4', credentials=CREDENTIALS)
    except:
        sys.exit('Either an internet connection or Google servers is unavailable.')
    
    def append(self, input_list):
        if len(input_list) > 2:
            tweetID  = input_list[0]
            tweet    = input_list[1]
            username = input_list[2]
            time     = input_list[3]
            children = input_list[4]
        
            values       = [[tweetID], [tweet], [username], [time], [children]]  # TODO: use map func
            append_range = self.TWEETS_RANGE
        else:
            username = input_list[0]
            password = input_list[1]
            
            values       = [[username], [password]]
            append_range = self.USERS_RANGE
        
        body = {
            'majorDimension': 'COLUMNS',
            'values': values
            }
        
        self.SERVICE.spreadsheets().values().append(spreadsheetId=self.SPREADSHEET_ID,
                                                    range=append_range,
                                                    valueInputOption='USER_ENTERED',
                                                    body=body).execute()
    
    def download(self):
        result = self.SERVICE.spreadsheets().values().batchGet(spreadsheetId=self.SPREADSHEET_ID,
                                                               ranges=self.QUERY_RANGE).execute()
        ranges = result.get('valueRanges', [])
        return ranges[0]['values'][1:]
    
    def DBclear(self, clear_range=QUERY_RANGE+'!A1'):
        self.SERVICE.spreadsheets().values().clear(spreadsheetId=self.SPREADSHEET_ID,
                                                    range=clear_range).execute()
    
    def DBquery(self, num_tweets, tweet_ID=None):
        if not tweet_ID:
            query = f'=query(Tweets!A:E, "select * where E = \'None\' order by D desc limit {num_tweets}")'
        else:
            query = f'=query(Tweets!A:E, "select * where A = {tweet_ID} or E = \'{tweet_ID}\' order by D asc")'
        
        body = {
            'majorDimension': 'COLUMNS',
            'values': [[query]]
            }
        append_range = self.QUERY_RANGE + '!A1'
        self.SERVICE.spreadsheets().values().append(spreadsheetId=self.SPREADSHEET_ID,
                                                    range=append_range,
                                                    valueInputOption='USER_ENTERED',
                                                    body=body).execute()
        
    def getTweetID(self):
        result = self.SERVICE.spreadsheets().values().get(spreadsheetId=self.SPREADSHEET_ID,
                                                          range=self.TWEET_ID).execute()
        return result['values'][0][0]
    
    def getPassword(self, username):
        value_body = {
            'values': [[username]]
            }
        
        self.SERVICE.spreadsheets().values().update(spreadsheetId=self.SPREADSHEET_ID,
                                                    range=self.USERS_RANGE+'!E1',
                                                    valueInputOption='USER_ENTERED',
                                                    body=value_body).execute()
        
        result = self.SERVICE.spreadsheets().values().get(spreadsheetId=self.SPREADSHEET_ID,
                                                          range=self.USERS_RANGE+'!F1').execute()
        return result['values'][0][0]
    
    def sortDB(self):
        basic_filter = {
            'sortRange': {
                'range': {
                'sheetId': 0,
                'startRowIndex': 0,
                'endColumnIndex': 5
                },
            'sortSpecs': [
                {
                'dimensionIndex': 3,
                'sortOrder': 'DESCENDING'
                }
                ]
            }
        }
        
        request = [basic_filter]
        body = {
            'requests': request
            }
        
        self.SERVICE.spreadsheets().batchUpdate(
            spreadsheetId=self.SPREADSHEET_ID,
            body=body).execute()

# model = Model()
# model.DBclear()
# model.DBquery(10)

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
