"""
Created on Tue Aug 11 18:16:43 2020

@author: Brian Sun

A fundamental version of Twitter using tkinter for UI and Google API for back-end data.
"""

import tkinter as tk
from datetime import datetime
import os
import pickle as pk
from googleapiclient.discovery import build

class View(object):
    
    def displayTweet(self, root, tweet, username, date):
        tk.Label(root, text=username, font='Arial 12 bold', justify='left', bg='white').pack(anchor='w', padx=12)
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
    
    os.chdir(os.getcwd())
    SPREADSHEET_ID = '1sLf9UMIP7MdWbcuS9qh3blkpsPBJzkIfZSlTuQ0Ltqg'
    TWEETS_RANGE = 'Tweets'
    USERS_RANGE = 'Logins'
    TWEET_ID = 'Parameters!B1'
        
    with open('token.pickle', 'rb') as creds:
        CREDENTIALS = pk.load(creds)
    
    SERVICE = build('sheets', 'v4', credentials=CREDENTIALS)
    
    def append(self, input_list):
        if len(input_list) > 2:
            tweetID  = input_list[0]
            tweet    = input_list[1]
            username = input_list[2]
            time     = input_list[3]
            children = input_list[4]
        
            values       = [[tweetID], [tweet], [username], [time], [children]]
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
    
    def download(self, num_tweets):
        result = self.SERVICE.spreadsheets().values().batchGet(spreadsheetId=self.SPREADSHEET_ID,
                                                          ranges=self.TWEETS_RANGE).execute()
        ranges = result.get('valueRanges', [])
        return ranges[0]['values'][1:num_tweets + 1]
    
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
                'dimensionIndex': 0,
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
# model.getPassword('amir')

class Controller(object):
    
    ROOT = tk.Tk()
    ROOT.minsize(1000, 800)
    ROOT.title('Welcome to Low-Budget Twitter!')
    ROOT.configure(bg='#1DA1F2')
    ROOT.iconphoto(False, tk.PhotoImage(file='logo.gif'))
    
    # fix scrollbar
    # tk.Scrollbar(ROOT).pack(side='right', fill='y')
    
    model = Model()
    view = View()
    
    def __init__(self):
        self.tweet_msg = tk.StringVar()
        self.username = tk.StringVar()
    
    def clearPage(self, widget_type=None):
        if not widget_type:
            for widget in self.ROOT.winfo_children():
                widget.destroy()
        else:
            for widget in self.ROOT.winfo_children():
                if widget.winfo_class() == widget_type:
                    widget.destroy()
    
    def refreshMainPage(self):
        self.clearPage('Label')
        
        tweets = self.model.download(5)
        
        for _, tweet, user, date, _1 in tweets:
            self.view.displayTweet(self.ROOT, tweet, user, date)
            
        self.ROOT.after(60000, self.refreshMainPage)
    
    def mainPage(self):
        self.view.getUserTweets(self.ROOT, self.tweet_msg)
        tk.Button(self.ROOT, text='Tweet!', 
                  command=lambda: [self.model.append([
                      self.model.getTweetID(), 
                      self.tweet_msg.get(), 
                      self.username.get(), 
                      datetime.now().strftime('%Y/%m/%d %H:%M'), 
                      'None'
                      ]),
                      self.model.sortDB()
                      ],
                  height=2,
                  width=15).pack(pady=5)
        
        tweets = self.model.download(5)
        
        for _, tweet, user, date, _1 in tweets:
            self.view.displayTweet(self.ROOT, tweet, user, date)
            # work on replies??
            # tk.Button(root, text='See Conversation', state='disabled', height=1, width=15).pack(anchor='w', padx=12, pady=5)
        
        self.ROOT.after(60000, self.refreshMainPage)
    
    def checkLogin(self, password):
        pw = self.model.getPassword(self.username.get())
        
        if password == pw:
            self.clearPage()
            self.mainPage()
        elif pw == '#N/A':
            tk.messagebox.showerror('Login Error', 'Username not recognized; please double-check entry, or create new account.')
        else:
            tk.messagebox.showerror('Login Error', 'Incorrect password! Please try again.')
    
    def checkRegistry(self, username, password):
        pw = self.model.getPassword(username)
        
        if pw != '#N/A':
            tk.messagebox.showerror('Registration Error', 'Username already exists! Please try logging in without registration.')
        else:
            self.model.append([username, password])
            self.clearPage()
            self.mainPage()
    
    def startup(self):
        password = tk.StringVar()
        logo = tk.PhotoImage(file="logo.gif").subsample(2, 2)
        tk.Label(self.ROOT, image=logo, borderwidth=0, highlightthickness=0).pack()
        self.view.loginEntry(self.ROOT, self.username, 'Enter username here...')
        self.view.loginEntry(self.ROOT, password, 'Enter password here...')
        
        tk.Button(self.ROOT, wraplength=150,
                  text='Register and login with above credentials',
                  command=lambda: self.checkRegistry(self.username.get(), password.get()),
                  height=2,
                  width=25).pack(pady=2)
        
        tk.Button(self.ROOT, wraplength=150,
                  text='Login to above account',
                  command=lambda: self.checkLogin(password.get()),
                  height=2,
                  width=25).pack(pady=2)
        
        self.ROOT.mainloop()

control = Controller()
control.startup()
