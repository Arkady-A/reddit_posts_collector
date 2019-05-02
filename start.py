# -*- coding: utf-8 -*-
import json
import data 
from data.collector import Collector
from data.processor import Processor

credentials = json.load(open('creden.json')) #temporary solution
code = credentials['code']
redirect_uri = credentials['redirect_uri']
user_agent = credentials['user-agent']
state = credentials['state']
client_id = credentials['client_id']
client_secret = credentials['client_secret']
headers = {'User-agent': user_agent},
scope = 'read'

colle = Collector(client_id, client_secret, user_agent, scope)

# for the time being I only collect 5 reddit posts
response = colle.get_reddit_posts(5, 'progresspics')
proc = Processor()
data = proc.process_data(response.json()['data']['children'])