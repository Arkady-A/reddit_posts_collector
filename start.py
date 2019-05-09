# -*- coding: utf-8 -*-
import json
import data 
from data.collector import Collector
from data.processor import Post_process
from data.processor import Processpics_process

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
data = []
for i in range(3):
    response = colle.get_reddit_posts('progresspics', 25, after_id)
    buff,after_id = Post_process.process_data(response.json()['data']['children'])   
    data.extend(buff)
data_processed = Post_process.to_dataframe(data)
data_processed = data_processed.apply(Processpics_process.parse_factory(),axis=1)
data_processed.to_csv('test.csv')
