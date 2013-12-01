from __future__ import unicode_literals
from requests_oauthlib import OAuth1
from urlparse import parse_qs
import simplejson
import json
import requests
from twython import Twython
import subprocess
import string
import random
import time
import os
from time import sleep, strftime
from subprocess import *
from subprocess import call
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.parser import HeaderParser
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.Utils import COMMASPACE, formatdate
from email import Encoders
#########################################################################
from email_cred import *
from keys import * #import APP_KEY, APP_SECRET,  OAUTH_TOKEN, OAUTH_TOKEN_SECRET
from urls import * #import REQUEST_TOKEN_URL, AUTHORIZE_URL, ACCESS_TOKEN_URL
def setup_oauth():
    """Authorize your app via identifier."""
    # Request token
    oauth = OAuth1(APP_KEY, client_secret=APP_SECRET)
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)

    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]

    # Authorize
    authorize_url = AUTHORIZE_URL + resource_owner_key
    print 'Please go here and authorize: ' + authorize_url

    verifier = raw_input('Please input the verifier: ')
    oauth = OAuth1(APP_KEY,
                   client_secret=APP_SECRET,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=verifier)

    # Finally, Obtain the Access Token
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    token = credentials.get('oauth_token')[0]
    secret = credentials.get('oauth_token_secret')[0]

    return token, secret


