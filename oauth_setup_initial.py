from __future__ import unicode_literals
from requests_oauthlib import OAuth1
from urlparse import parse_qs

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


