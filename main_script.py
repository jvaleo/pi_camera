#!/usr/local/bin/python
"""" 
To Do List:
1 - Clean up imports, not sure if i need most to the email. imports
2 - Import the twitter username from an external file
3 - Have the last tweet function return the last tweet twitpic link
4 - Have the send_reply_email be a function that takes in mail_list 
5 - Clean up the get email functions
6 - Add logging
7 - Add error handling for both gmail and twitter response codes
 """

from __future__ import unicode_literals
from requests_oauthlib import OAuth1
from urlparse import parse_qs
import simplejson
import json
import re
import requests
from twython import Twython
import subprocess
import string
import random
import os
from time import *
import imaplib
import smtplib
import email
from email import Encoders
from email.mime.text import MIMEText
from email.parser import HeaderParser
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.Utils import COMMASPACE, formatdate

from email_cred import *
from keys import * #import APP_KEY, APP_SECRET,  OAUTH_TOKEN, OAUTH_TOKEN_SECRET
from urls import * #import REQUEST_TOKEN_URL, AUTHORIZE_URL, ACCESS_TOKEN_URL
from cameraconfig import *
from known_addresses import *

twitter = Twython(APP_KEY, APP_SECRET,  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
imap_server = imaplib.IMAP4_SSL("imap.gmail.com",993)
imap_server.login(USERNAME, PASSWORD)
imap_server.select('INBOX')

basestring=string.lowercase+string.digits
randomfile = ''.join(random.sample(basestring,25)) 
filename = '/home/pi/photos/' + randomfile + '.jpg'
	
def get_oauth():
    oauth = OAuth1(APP_KEY, client_secret=APP_SECRET, resource_owner_key=OAUTH_TOKEN, resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth

def last_tweet():
	oauth = get_oauth()
	rawapireturn = requests.get(url="https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=rosieandbuckley&count=1", auth=oauth)
	contentreturn = rawapireturn.content
	jsonreturn = simplejson.loads(contentreturn)
	for item in jsonreturn:
		last_tweet = item['text']
		return last_tweet
		
		
def post_text_tweet():
	oauth = get_oauth()
	tweet = 'this is a new test'
	requests.post("https://api.twitter.com/1.1/statuses/update.json?screen_name=rosieandbuckley&status=" + tweet, auth=oauth)
	
def post_media_tweet():
	photo = open(filename, 'rb')
	twitter.update_status_with_media(status='Herro', media=photo)	

def take_picture():
	if camera_type == 'pi':
		subprocess.call(["raspistill", "-o", filename])
	elif camera_type == 'web':
		subprocess.call(["fswebcam", "-r", "960x720", "-d", "/dev/video0", filename])
	else:
		exit()

def get_senders(email_ids):
    senders_list = []
    for e_id in email_ids[0].split(): 
    	resp, data = imap_server.fetch(e_id, '(RFC822)')
    	perf = HeaderParser().parsestr(data[0][1])	 
    	senders_list.append(perf['From'])	
    return senders_list

def check_email():
    status, email_ids = imap_server.search(None, '(UNSEEN)')  
    if email_ids == ['']:
        print('No Unread Emails')
        mail_list = []
    else:
		mail_list = get_senders(email_ids)
		for from_address in mail_list:
			from_address_formatted=from_address[from_address.find("<")+1:from_address.find(">")]
			if from_address_formatted in known_addresses:
				print 'Known Address: ' + from_address_formatted
				#take_picture()
				#post_media_tweet()
				server = smtplib.SMTP('smtp.gmail.com:587')  
				server.starttls()  
				server.login(USERNAME,PASSWORD)  
				server.sendmail(USERNAME, from_address_formatted, 'last_tweet(last_tweet``)')  
				server.quit()
			else:
				print 'UNKNOWN ADDRESS: ' + from_address_formatte
				
if __name__ == "__main__":		
	check_email()


