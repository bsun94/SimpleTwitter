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
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class View(object):
    
    def displayTweet(self, root, tweet, username, date):
        tk.Label(root, text=username, font='Arial 12 bold', justify='left', bg='#1DA1F2').pack(anchor='w', padx=12)
        tk.Label(root, text=date, font='Arial 8 italic', justify='left', bg='#1DA1F2').pack(anchor='w', padx=12)
        tk.Label(root, text=tweet, font='Arial 11', justify='left', bg='#1DA1F2').pack(anchor='w', padx=12, pady=5)
        
        # eventually will work on if statement checking for children
        # tk.Button(root, text='See Conversation', state='disabled', height=1, width=15).pack(anchor='w', padx=12, pady=5)
    
    def getUserTweets(self, root, msg):
        msg.set('Enter tweet here...')
        entry_bar = tk.Entry(root, textvariable=msg, font='Arial 12 italic', width=80)
        entry_bar.bind('<Button-1>', lambda event: entry_bar.delete(0, 'end'))
        entry_bar.pack(pady=20)
    


class Model(object):
    
    os.chdir(os.getcwd())
    SPREADSHEET_ID = '1sLf9UMIP7MdWbcuS9qh3blkpsPBJzkIfZSlTuQ0Ltqg'
    TWEETS_RANGE = 'Tweets'
    TWEET_ID = 'Parameters!B1'
        
    with open('token.pickle', 'rb') as creds:
        CREDENTIALS = pk.load(creds)
    
    SERVICE = build('sheets', 'v4', credentials=CREDENTIALS)
    
    def append(self, tweet_list):
        tweetID  = tweet_list[0]
        tweet    = tweet_list[1]
        username = tweet_list[2]
        time     = tweet_list[3]
        children = tweet_list[4]
        
        values = [[tweetID], [tweet], [username], [time], [children]]
        body = {
            'majorDimension': 'COLUMNS',
            'values': values
            }
        result = self.SERVICE.spreadsheets().values().append(spreadsheetId=self.SPREADSHEET_ID,
                                                             range=self.TWEETS_RANGE,
                                                             valueInputOption='USER_ENTERED',
                                                             body=body).execute()
        updates = result.get('updates').get('updatedCells')
        print(f'{updates} cells updated.')
    
    def download(self, num_tweets):
        result = self.SERVICE.spreadsheets().values().batchGet(spreadsheetId=self.SPREADSHEET_ID,
                                                          ranges=self.TWEETS_RANGE).execute()
        ranges = result.get('valueRanges', [])
        return ranges[0]['values'][1:num_tweets + 1]
    
    def getTweetID(self):
        result = self.SERVICE.spreadsheets().values().get(spreadsheetId=self.SPREADSHEET_ID,
                                                          range=self.TWEET_ID).execute()
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
# model.download()

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
        self.username = 'bsun94'
    
    def refreshMainPage(self):
        for widget in self.ROOT.children.values():
            if widget.winfo_class() == 'Label':
                widget.pack_forget()
        
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
                      self.username, 
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
        
        self.ROOT.after(60000, self.refreshMainPage)
    
    def runTwitter(self):
        self.mainPage()
        
        self.ROOT.mainloop()

control = Controller()
control.runTwitter()
