"""
Created on Wed Aug 26 23:05:04 2020

Contains the main tweet page portion of the controller
"""

import tkinter as tk
from datetime import datetime
import os

# For importing custom model and view modules - please ensure you've saved all these files in the same directory!
os.chdir(os.path.realpath('..') + '\\Model')
import BasicTwitterDB as dt

os.chdir(os.path.realpath('..') + '\\View')
import BasicTwitterView as vw

class MainController(object):
    
    # Controls the number of (most recent) tweets loaded on the GUI
    # current only applied to the display of parent tweets on the mainPage
    NUM_TWEETS = 10
    
    def __init__(self, frame, canvas, tweet_msg, username):
        """
        Defines the controller for the replies page, showing conversations chains for a particular tweet.       

        """
        self.frame = frame
        self.canvas = canvas
        
        self.tweet_msg = tweet_msg
        self.username = username
        # self.repliesPage = repliesPage
        
        self.db = dt.DBHandler()
        self.view = vw.View(frame)
    
    def mainPage(self, repliesPage):
        """
        Displays the main parent of the app, with the parent/topic tweets posted by different users.
        Whenever a user posts a new tweet, a new tweet_id is assigned, which is determined by max(tweet_id) in the db + 1.
        
        Like the replies page, this page is set to refresh every 60sec currently.

        """
        self.view.clearPage()            # clear the page to refresh contents
        self.canvas.yview_moveto('0.0')  # defaults scroll to top of page
        
        self.view.getUserTweets(self.tweet_msg)
        tk.Button(self.frame, text='Tweet!', 
                  command=lambda: [self.db.addTweet( 
                      self.tweet_msg.get(), 
                      self.username.get(), 
                      datetime.now(),
                      ),
                      self.frame.after_cancel(mainAfter),
                      self.mainPage(repliesPage)
                      ],
                  height=2,
                  width=15).pack(pady=5)
        
        tweets = self.db.getTweet(num_tweets=self.NUM_TWEETS)
        
        for t_id, tweet, user, date, _ in tweets:
            self.view.displayTweet(tweet, user, date.strftime('%Y/%m/%d %H:%M'))
            tk.Button(self.frame, text='See Conversation',
                      command=lambda t_id=t_id: [self.frame.after_cancel(mainAfter),
                                                 repliesPage(self.mainPage, t_id)],
                      height=1,
                      width=15).pack(anchor='w', padx=12, pady=5)
        
        mainAfter = self.frame.after(60000, lambda: self.mainPage(repliesPage))
