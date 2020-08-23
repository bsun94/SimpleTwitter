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
            print('Connected to database:', self.db, ' as user:', self.login, ' on host:', self.hostname)
            return conn
        except:
            print('Unable to connect:', ibm.conn_errormsg())
    
    def close(self, conn):
        try:
            ibm.close(conn)
            print('Connection closed.')
        except:
            print('Unable to close connection, please try again.')
    
    def addUser(self, username, password):
        try:
            user = userModel(username, password)
        except:
            return
        
        conn = self.connect()
        
        query = f'''insert into LOGINS ("USERNAME","PASSWORD")\
                values ('{user.username}', '{user.password}');'''
        
        ibm.exec_immediate(conn, query)
                
        self.close(conn)
    
    # def append(self, input_list):
    #     return None
    
    # def download(self):
    #     result = self.SERVICE.spreadsheets().values().batchGet(spreadsheetId=self.SPREADSHEET_ID,
    #                                                            ranges=self.QUERY_RANGE).execute()
    #     ranges = result.get('valueRanges', [])
    #     return ranges[0]['values'][1:]
    
    # def DBclear(self, clear_range=QUERY_RANGE+'!A1'):
    #     self.SERVICE.spreadsheets().values().clear(spreadsheetId=self.SPREADSHEET_ID,
    #                                                 range=clear_range).execute()
    
    # def DBquery(self, num_tweets, tweet_ID=None):
    #     if not tweet_ID:
    #         query = f'=query(Tweets!A:E, "select * where E = \'None\' order by D desc limit {num_tweets}")'
    #     else:
    #         query = f'=query(Tweets!A:E, "select * where A = {tweet_ID} or E = \'{tweet_ID}\' order by D asc")'
        
    #     body = {
    #         'majorDimension': 'COLUMNS',
    #         'values': [[query]]
    #         }
    #     append_range = self.QUERY_RANGE + '!A1'
    #     self.SERVICE.spreadsheets().values().append(spreadsheetId=self.SPREADSHEET_ID,
    #                                                 range=append_range,
    #                                                 valueInputOption='USER_ENTERED',
    #                                                 body=body).execute()
        
    # def getTweetID(self):
    #     result = self.SERVICE.spreadsheets().values().get(spreadsheetId=self.SPREADSHEET_ID,
    #                                                       range=self.TWEET_ID).execute()
    #     return result['values'][0][0]
    
    # def getPassword(self, username):
    #     value_body = {
    #         'values': [[username]]
    #         }
        
    #     self.SERVICE.spreadsheets().values().update(spreadsheetId=self.SPREADSHEET_ID,
    #                                                 range=self.USERS_RANGE+'!E1',
    #                                                 valueInputOption='USER_ENTERED',
    #                                                 body=value_body).execute()
        
    #     result = self.SERVICE.spreadsheets().values().get(spreadsheetId=self.SPREADSHEET_ID,
    #                                                       range=self.USERS_RANGE+'!F1').execute()
    #     return result['values'][0][0]

db = DBHandler()
db.addUser('bsun94', 'Helga')
# conn = db.connect()
# query=''
# ibm.exec_immediate(conn, query)
# db.close(conn)
