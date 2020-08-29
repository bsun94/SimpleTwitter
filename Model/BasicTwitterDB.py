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


# For importing custom model and view modules - please ensure you've saved all these files in the same directory!
os.chdir(os.path.realpath('..') + '\\Model')
import BasicTwitterModel as md
import BasicTwitterTweet as tw
import BasicTwitterEnum as en

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
            return conn
        except:
            print('Unable to connect:', ibm.conn_errormsg())
    
    def close(self, conn):
        """
        Takes in a connection object as parameter, and closes that connection.

        """
        try:
            ibm.close(conn)
        except:
            print('Unable to close connection, please try again.')
    
    def addUser(self, username, password):
        """
        Validates user data using userModel, before storing user information in the LOGINS table on IBM db.

        """
        try:
            user = md.userModel(username, password)
        except:
            return
        
        conn = self.connect()
        
        query = f'''insert into LOGINS ("USERNAME","PASSWORD")\
                values ('{user.username}', '{user.password}');'''
        
        ibm.exec_immediate(conn, query)
                
        self.close(conn)
    
    def addTweet(self, tweet, username, date, parent_id='NULL'):
        """
        Validates tweet data using tweetModel, before storing tweet message info in the TWEETS table on IBM db.

        """
        try:
            tweet = tw.tweetModel(tweet, username, date, parent_id)
        except:
            return
        
        conn = self.connect()
        
        query = f'''insert into TWEETS ("TWEET","USERNAME","DATE","PARENT_ID")\
                values ('{tweet.tweet}', '{tweet.username}', '{tweet.date}', {tweet.parent_id});'''
        
        ibm.exec_immediate(conn, query)
                
        self.close(conn)
    
    def getPassword(self, username, password):
        """
        For a given username passed as parameter, checks if the corresponding password on record in the db table matches
        with the password passed in as parameter. Raises appropriate errors if not.
        Can also be used to see if a username already exists or not in the db.

        """
        password = hs.sha3_256(str.encode(password)).hexdigest()
        
        conn = self.connect()
        
        query = f'''select "PASSWORD" from LOGINS where "USERNAME" = '{username}';'''
        try:
            run = ibm.exec_immediate(conn, query)
            pw = ibm.fetch_tuple(run)[0]
        except:
            return en.States.user_err
        
        self.close(conn)
        
        if pw != password:
            return en.States.pw_err
        else:
            return en.States.verified
    
    def getTweet(self, num_tweets=None, tweet_ID=None):
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
    
    def buildDB(self):
        """
        Helps user build up their database for the application on IBM upon initial startup.
        Makes sure user has not created table already beforehand.

        """
        conn = self.connect()
        
        query = f'''CREATE TABLE IF NOT EXISTS LOGINS
            (USERNAME VARCHAR(50) NOT NULL PRIMARY KEY
            ,PASSWORD CLOB(1048576) NOT NULL);
            CREATE TABLE IF NOT EXISTS TWEETS
            (TWEET_ID INTEGER NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1)
            ,TWEET CLOB(1048576) NOT NULL
            ,USERNAME VARCHAR(50) NOT NULL
            ,DATE TIMESTAMP(12)
            ,PARENT_ID INTEGER);'''
        
        ibm.exec_immediate(conn, query)
        
        self.close(conn)
