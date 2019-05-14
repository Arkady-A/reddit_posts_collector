# -*- coding: utf-8 -*-
import json
import data 
import matplotlib.pyplot as plt
from data.collector import Collector
from data.processor import Post_process
from data.processor import Processpics_process
import os
#delete
import importlib
import time
import cv2
import sys


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
after_id = None

data_posts=[]
for i in range(1):
    response = colle.get_reddit_posts('progresspics', 5, after_id)
    buff,after_id = Post_process.process_data(response.json()['data']['children'])   
    data_posts.extend(buff)
    if colle.session.token['expires_at']-time.time()<100:
        colle = Collector(client_id, client_secret, user_agent, scope)

data_processed = Post_process.to_dataframe(data_posts)
data_processed = data_processed.apply(Processpics_process.parse_factory(),axis=1)

data_processed = data_processed.apply(colle.get_check_pics_factory(),axis=1)
data_processed.to_csv('test.csv')
