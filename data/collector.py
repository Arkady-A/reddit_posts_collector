from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import requests as req
import time
import os.path
import numpy as np

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
        return self.session.get(
                'https://oauth.reddit.com/r/{}/new'.format(subreddit),
                params={'limit':limit, 'raw_json':1})


    def get_images(self, list_of_urls, list_of_names, filepath):
        '''
        Downloads list of images and saves them in a folder
        Parameters
        ----------
        list_of_url : list of str
            urls leading to image
        list_of_naems: list of str
            list of names for downloaded images
        filepath: str
            path to a directory in which the images will be saved
        
        Returns
        -------
        None
        '''
        formats = ['.jpg','.png']
        for url,name in list(zip(list_of_urls, list_of_names)):
            response = req.get(url)
            time.sleep(0.5)
            try:
                form = next(filter(lambda x: x in url,formats))
            except StopIteration:
                continue
            with open(os.path.join(filepath,name+form),'wb') as file:
                file.write(response.content)
            
            