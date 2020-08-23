"""
Created on Sat Aug 22 17:02:36 2020

Contains the Model as well as the DB Handling portion of BasicTwitterBQ
"""

import tkinter as tk
import os
import sys
import json
import ibm_db as ibm
import hashlib as hs
from datetime import datetime

class userModel():
    
    def __init__(self, username, password):
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

class tweetModel():
    
    def __init__(self, tweet, username, date, parent_id):
        if not tweet:
            tk.messagebox.showerror('Tweet Error', 'Empty Tweet!')
            sys.exit()
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
        
        if parent_id and not isinstance(parent_id, int):
            tk.messagebox.showerror('Tweet Error', 'Parent ID of the message either has to be empty, or an int!')
            sys.exit()
        else:
            self.parent_id = parent_id

class DBHandler():
    
    DRIVER = '{IBM DB2 ODBC DRIVER}'
    PROTOCOL = 'TCPIP'
    
    def __init__(self):
        os.chdir(os.getcwd())
        with open('credentials.json', 'rb') as file:
            creds = json.load(file)
        
        self.pw       = creds['password']
        self.db       = creds['db']
        self.port     = creds['port']
        self.login    = creds['username']
        self.hostname = creds['hostname']
        
        self.dsn = f'DRIVER={self.DRIVER};\
                    DATABASE={self.db};\
                    HOSTNAME={self.hostname};\
                    PORT={self.port};\
                    PROTOCOL={self.PROTOCOL};\
                    UID={self.login};\
                    PWD={self.pw};'
    
    def connect(self):
        try:
            conn = ibm.connect(self.dsn, "", "")
            # print('Connected to database:', self.db, ' as user:', self.login, ' on host:', self.hostname)
            return conn
        except:
            print('Unable to connect:', ibm.conn_errormsg())
    
    def close(self, conn):
        try:
            ibm.close(conn)
            # print('Connection closed.')
        except:
            print('Unable to close connection, please try again.')
    
    def addUser(self, username, password):  # replaces append for users
        try:
            user = userModel(username, password)
        except:
            return
        
        conn = self.connect()
        
        query = f'''insert into LOGINS ("USERNAME","PASSWORD")\
                values ('{user.username}', '{user.password}');'''
        
        ibm.exec_immediate(conn, query)
                
        self.close(conn)
    
    def addTweet(self, tweet, username, date, parent_id=None):  # replaces append for tweets
        try:
            tweet = tweetModel(tweet, username, date, parent_id)
        except:
            return
        
        tweet_id = self.getTweetID() + 1
        
        conn = self.connect()
        
        # Python None gets converted to a string automatically when passed to IBM DB2; have to make NULL explicit in query statement
        if tweet.parent_id:
            query = f'''insert into TWEETS ("TWEET_ID","TWEET","USERNAME","DATE","PARENT_ID")\
                    values ({tweet_id}, '{tweet.tweet}', '{tweet.username}', '{tweet.date}', {tweet.parent_id});'''
        else:
            query = f'''insert into TWEETS ("TWEET_ID","TWEET","USERNAME","DATE","PARENT_ID")\
                    values ({tweet_id}, '{tweet.tweet}', '{tweet.username}', '{tweet.date}', NULL);'''
        
        ibm.exec_immediate(conn, query)
                
        self.close(conn)
    
    def getTweetID(self):
        conn = self.connect()
        
        query = f'''select max("TWEET_ID") from TWEETS;'''
        run = ibm.exec_immediate(conn, query)
        tweet_id = ibm.fetch_tuple(run)
        
        self.close(conn)
        
        return tweet_id[0]
    
    def getPassword(self, username, password):
        try:
            user = userModel(username, password)
        except:
            return
        
        conn = self.connect()
        
        query = f'''select "PASSWORD" from LOGINS where "USERNAME" = '{user.username}';'''
        try:
            run = ibm.exec_immediate(conn, query)
            pw = ibm.fetch_tuple(run)[0]
        except:
            return 'username error'
        
        self.close(conn)
        
        if pw != user.password:
            return 'password error'
        else:
            return 'verified'        
    
    def DBquery(self, num_tweets=None, tweet_ID=None):
        conn = self.connect()
        
        if not num_tweets and not tweet_ID:
            tk.messagebox.showerror('Query Error', 'Please supply one of num_tweets or tweet_ID - don\'t leave both as None!')
            sys.exit()
        elif tweet_ID and not num_tweets:
            query = f'''select * from TWEETS WHERE "TWEET_ID" = {tweet_ID} OR "PARENT_ID" = {tweet_ID} ORDER BY "DATE";'''
        elif num_tweets and not tweet_ID:
            query = f'''select * from TWEETS WHERE "PARENT_ID" ISNULL ORDER BY "DATE" DESC LIMIT '{num_tweets}';'''
        else:
            tk.messagebox.showerror('Query Error', 'Please supply ONE OF num_tweets or tweet_ID!')
            sys.exit()
        
        run = ibm.exec_immediate(conn, query)
        tup = ibm.fetch_tuple(run)
        
        results_tup = []
        while tup:
            results_tup.append(tup)
            tup = ibm.fetch_tuple(run)
        
        self.close(conn)
        
        return results_tup
