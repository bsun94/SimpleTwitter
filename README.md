# Basic Twitter
##### A simple version of Twitter, capable of handling user registrations and logins, tweet posting/replies and retrieval/display.
______________________

**Dependencies - please make sure you have the following python packages installed:**
- Regular packages: tkinter, datetime, os, sys, json, pickle
- Special packages: hashlib, *ibm_db*

Between yourself and your friends, someone should sign up for an IBM Cloud account; with a Lite plan, you can get free database access (up to 200MB storage).

[Click here to sign-up](https://cloud.ibm.com/catalog/services/db2)

Once you're on the Db main page after setting up the Lite plan, click on the "Credentials" tab and create new credentials. Paste the credentials provided in the drop-down of your created project (which should look to be in a JSON/dictionary format) into the empty credentials file provided). If IBM doesn't take you automatically to your DB2 service main page, after you've created a Cloud account, click on the menu button in the top-left corner of the screen (three long dashes), then click on "Resources." Under "Storage" in your resources list, you should see a Db2 link taking you to the Db main page.

Next, run the buildDB() method in the BasicTwitterDB script to set up the necessary db tables for you. Then you're set! The overall Twitter script starts-up from BasicTwitterController script.