# -*- coding: utf-8 -*-
import json
import requests as req
import data 
from data.collector import Collector
from data.processor import Processor
credentials = json.load(open('creden.json')) # user and pass are required
code = credentials['code']
redirect_uri = credentials['redirect_uri']
user_agent = credentials['user-agent']
state = credentials['state']
client_id = credentials['client_id']
client_secret = credentials['client_secret']
headers = {'User-agent': user_agent},
scope = 'read'

colle = Collector(client_id, client_secret, user_agent, scope)

response = colle.get_reddit_posts(5, 'progresspics')
proc = Processor()
data = proc.process_data(response.json()['data']['children'])
#response = req.Request('get','https://www.reddit.com/api/v1/authorize',
#        headers = {'User-agent': user_agent},
#        params={
#                'client_id':client_id,
#                'response_type':'code',
#                'state':state,
#                'redirect_uri':redirect_uri,
#                'duration':'temporary',
#                'scope':scope
#                }
#        ).prepare()
#print(response.url)
#code = input()
#
#client_auth = req.auth.HTTPBasicAuth(client_id, client_secret)
#
#response = req.post(url="https://www.reddit.com/api/v1/access_token",
#    headers = {'User-agent': user_agent},
#    params={
##    "username": user,
##    "password": password, # this shoul be put in a file 
#    "grant_type": "client_credentials",
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
with open('test.json', 'w') as file:
    file.write(json.dumps(response.json(), indent=4, sort_keys=True))
print(list(response.json()['data']))
