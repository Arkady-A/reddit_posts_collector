# -*- coding: utf-8 -*-
import json
import requests as req
import requests_oauthlib as req_o

from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

class Collector():
    def make_oath_session(self, client_id, client_secret, user_agent):
        auth = HTTPBasicAuth(client_id, client_secret)
        client = BackendApplicationClient(client_id=client_id)
        self.session = OAuth2Session(client=client, )
        self.session.headers['User-Agent'] = user_agent
        self.token = self.session.fetch_token(
                token_url='https://www.reddit.com/api/v1/access_token',
                auth=auth, )  
    def __init__ (self, client_id, client_secret, user_agent, scope):
        self.make_oath_session(client_id, 
                               client_secret,
                               user_agent
                               )
        print(self.session, self.token.values())
    
    def get_reddit_posts(self, limit, subreddit ,after=None):
        return self.session.get('https://oauth.reddit.com/r/{}/new'.format(subreddit),
                                params={'limit':limit})


        
#user = credentials['user']
#password = credentials['pass']
#code = credentials['code']
#redirect_uri = credentials['redirect_uri']
#user_agent = credentials['user-agent']
#
#client_id = credentials['client_id']
#client_secret = credentials['client_secret']
#
#client_auth = req.auth.HTTPBasicAuth(client_id, client_secret)
#
#response = req.post(url="https://www.reddit.com/api/v1/access_token",
#    headers = {'User-agent': user_agent},
#    params={
#    "grant_type": "authorization_code",
#    "code": code,
#    "redirect_uri": redirect_uri
#  },
#  timeout=2.2,
#  auth = client_auth
#)
#print(response.json())
#access_token = response.json()['access_token']
#url = 'https://oauth.reddit.com/'
#
##test section# 
#
#url_interested = url[:-1]+'/r/progresspics/hot'
#
#response = req.get(url_interested,
#                   headers={"Authorization": "bearer " + access_token,
#                            "user-agent":user_agent,},
#params={'raw_json':1,'limit':7,}
#                   )
#with open('test.json', 'w') as file:
#    file.write(json.dumps(response.json(), indent=4, sort_keys=True))
#print(list(response.json()['data']))
