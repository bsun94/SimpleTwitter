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

class tweetModel():
    
    def __init__(self, tweet, username, date, parent_id):
        """
        Validates tweet msgs, username, date and parent tweet id before passing it to db. Checks all parameters for blanks/Nones.
        Specifically, ensure that the date parameter is indeed a datetime object, and that parent_id is either None (for parent
        tweets) or an int for child tweets.

        """
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
    
    # Parameters specific to connecting to IBM DB2
    DRIVER = '{IBM DB2 ODBC DRIVER}'
    PROTOCOL = 'TCPIP'
    
    def __init__(self):
        """
        Reads in credentials, stored in the same working directory, to access the IBM db.

        """
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
        """
        Manages establishing a connection to the IBM db. Returns a connection object.

        """
        try:
            conn = ibm.connect(self.dsn, "", "")
            # print('Connected to database:', self.db, ' as user:', self.login, ' on host:', self.hostname)
            return conn
        except:
            print('Unable to connect:', ibm.conn_errormsg())
    
    def close(self, conn):
        """
        Takes in a connection object as parameter, and closes that connection.

        """
        try:
            ibm.close(conn)
            # print('Connection closed.')
        except:
            print('Unable to close connection, please try again.')
    
    def addUser(self, username, password):
        """
        Validates user data using userModel, before storing user information in the LOGINS table on IBM db.

        """
        try:
            user = userModel(username, password)
        except:
            return
        
        conn = self.connect()
        
        query = f'''insert into LOGINS ("USERNAME","PASSWORD")\
                values ('{user.username}', '{user.password}');'''
        
        ibm.exec_immediate(conn, query)
                
        self.close(conn)
    
    def addTweet(self, tweet, username, date, parent_id=None):
        """
        Validates tweet data using tweetModel, before storing tweet message info in the TWEETS table on IBM db.

        """
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
        """
        Used to assign IDs to new tweets; grabs the max ID int in the TWEETS table, and adds 1 to that.

        """
        conn = self.connect()
        
        query = f'''select max("TWEET_ID") from TWEETS;'''
        run = ibm.exec_immediate(conn, query)
        tweet_id = ibm.fetch_tuple(run)
        
        self.close(conn)
        
        return tweet_id[0]
    
    def getPassword(self, username, password):
        """
        For a given username passed as parameter, checks if the corresponding password on record in the db table matches
        with the password passed in as parameter. Raises appropriate errors if not.
        Can also be used to see if a username already exists or not in the db.

        """
        pw = hs.sha3_256(str.encode(password)).hexdigest()
        
        conn = self.connect()
        
        query = f'''select "PASSWORD" from LOGINS where "USERNAME" = '{username}';'''
        try:
            run = ibm.exec_immediate(conn, query)
            pw = ibm.fetch_tuple(run)[0]
        except:
            return 'username error'
        
        self.close(conn)
        
        if pw != password:
            return 'password error'
        else:
            return 'verified'        
    
    def postTweet(self, num_tweets=None, tweet_ID=None):
        """
        Used to query either all parent tweets or tweets specific to a single conversation chain for the current application.
        Takes in a num_tweets parameters, limiting the number of displayed results (mainly for presentation purposes), and a
        tweet_id to indicate a specific conversation chain.

        """
        conn = self.connect()
        
        if not num_tweets and not tweet_ID:
            tk.messagebox.showerror('Query Error', 'Please supply one of num_tweets or tweet_ID - don\'t leave both as None!')
            sys.exit()
        elif tweet_ID and not num_tweets:
            query = f'''select * from TWEETS WHERE "TWEET_ID" = {tweet_ID} OR "PARENT_ID" = {tweet_ID} ORDER BY "DATE";'''
        elif num_tweets and not tweet_ID:
            query = f'''select * from TWEETS WHERE "PARENT_ID" ISNULL ORDER BY "DATE" DESC LIMIT '{num_tweets}';'''
        else:
            query = f'''select * from TWEETS WHERE "TWEET_ID" = {tweet_ID} OR "PARENT_ID" = {tweet_ID} ORDER BY "DATE" DESC LIMIT '{num_tweets}';'''
        
        run = ibm.exec_immediate(conn, query)
        tup = ibm.fetch_tuple(run)
        
        results_tup = []
        while tup:
            results_tup.append(tup)
            tup = ibm.fetch_tuple(run)
        
        self.close(conn)
        
        return results_tup
