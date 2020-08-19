# Basic Twitter
##### A simple version of Twitter, capable of handling user registrations and logins, as well as tweet posting and retrieval/display.
______________________

**Dependencies - please make sure you have the following python packages installed:**
- Regular packages: tkinter, datetime, os, pickle
- Special packages: hashlib, googleapiclient

Please refer to *https://developers.google.com/sheets/api* to set up Google API, which is needed by this functionality to use a Google Sheets document as its database.

Run the **GoogleQuickstart** script in your working directory: it should open up a web browser window asking you to sign in to your Google account. This process generates a **token.pickle** file in your working directory which is used by scripts leveraging Google API to access documents on your Google account. You can find this Quickstart script in the above Google API weblink as well, although the version I've uploaded is slightly modified to generate a token which grants you both *read* and *write* access.

The BasicTwitter script is generally built around the MVC design pattern: its View class contains methods which help build various *tkinter* widgets for the GUI; its Model class leverages *Google API* to manipulate data (user and tweet) in a Google Sheet that you will have created for use by this application (more on the Google Sheet set-up below); and its Controller class handles how the user interacts with the application as a whole, how different views are presented to the user and how data is transported between the application and the database.

In setting up a Google Sheet as the database for this application, please note down its **spreadsheet ID** (which can be found in the Sheet's URL - refer the the Google API documentation above for exact positioning). I would recommend setting up at least 3 tabs: **Tweets** (to store tweets), **Logins** (to store user logins) and **Parameters**.

The *Tweets* tab should be set up with the following columns **in order**: TweetID, Tweet, Username, Time, HasChildren

The *Logins* tab should be set up with the following columns **in order**: Username, Password. In cell F1, it should also vlookup the password of any username entered into cell E1. The script uses this in-sheet lookup to validate logins/registrations.

The *Parameters* tab should have a counta function in cell B2 which counts the number of non-blank cells in column A of the Tweets tab. This helps assign new TweetIDs to new tweets stored.