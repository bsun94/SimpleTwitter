"""
Created on Wed Aug 26 23:05:04 2020

Contains the main tweet page portion of the controller
"""

import tkinter as tk
from datetime import datetime
import os

# For importing custom model and view modules - please ensure you've saved all these files in the same directory!
os.chdir(os.getcwd())

import BasicTwitterDB as dt
import BasicTwitterView as vw
import BasicTwitterMain as mn

class RepliesController(object):
    
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
        
        self.db = dt.DBHandler()
        self.view = vw.View(frame)
        self.main = mn.MainController(frame, canvas, tweet_msg, username, self.repliesPage)
    
    def repliesPage(self, tweet_ID):
        """
        Displays the conversation chain for a specific parent tweet, as indicated by the tweet_ID parameter.
        Whenever a user posts a new reply to a parent tweet on this page, that tweet is stored in the db with its
        parent_id parameter equal to the parent tweet's tweet_id.
        
        The page is currently set to refresh every 60sec in its tk .after loop.
        
        """
        self.view.clearPage()            # clear the page to refresh contents
        self.canvas.yview_moveto('0.0')  # defaults scroll to top of page
        
        self.view.getUserTweets(self.tweet_msg)
        tk.Button(self.frame, text='Tweet!', 
                  command=lambda: [self.db.addTweet(
                      self.tweet_msg.get(), 
                      self.username.get(), 
                      datetime.now(), 
                      tweet_ID
                      ),
                      self.frame.after_cancel(repliesAfter),
                      self.repliesPage(tweet_ID)
                      ],
                  height=1,
                  width=15).pack(pady=2)
        
        tk.Button(self.frame, text='Return!', 
                  command=lambda: [self.frame.after_cancel(repliesAfter),
                                   self.main.mainPage()],
                  height=1,
                  width=15).pack(pady=2)
        
        tweets = self.db.getTweet(tweet_ID=tweet_ID)
        
        for _, tweet, user, date, _1 in tweets:
            self.view.displayTweet(tweet, user, date.strftime('%Y/%m/%d %H:%M'))
        
        repliesAfter = self.frame.after(60000, lambda: self.repliesPage(tweet_ID))
