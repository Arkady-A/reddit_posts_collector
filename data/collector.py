from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from .processor import Processpics_process
import requests as req
import time
import os.path
import numpy as np
import cv2

class Collector():
    def make_oath_session(self, client_id, client_secret, user_agent):
        '''
        Makes oath session
        '''
        auth = HTTPBasicAuth(client_id, client_secret)
        client = BackendApplicationClient(client_id=client_id)
        self.session = OAuth2Session(client=client, )
        self.session.headers['User-Agent'] = user_agent
        self.time_of_data_req = time.time()
        self.token = self.session.fetch_token(
                token_url='https://www.reddit.com/api/v1/access_token',
                auth=auth, )  
    def __init__ (self, client_id, client_secret, user_agent, scope):
        self.make_oath_session(client_id, 
                               client_secret,
                               user_agent
                               )
    
    def get_reddit_posts(self, subreddit, limit, after=None):
        '''
        Get subreddit's posts
        Parameters
        ----------
        subreddit: str
            name of subreddit
        limit: int
            How much post to download
        after : str
            reddit's post id from which to start
        
        Returns
        -------
        dict
            converted to python's dictionary json response
        '''
        parameters = {'limit':limit, 'raw_json':1}
        if after is not None:
            parameters['after']=after
        time_diff = time.time() - self.time_of_data_req
        if time_diff<1:
            time.sleep(1-time_diff+0.01)
        self.time_of_data_req = time.time()
        return self.session.get(
                'https://oauth.reddit.com/r/{}/new'.format(subreddit),
                params=parameters)


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
        images=[]
        formats = ['.jpg','.png']
        for url,name in list(zip(list_of_urls, list_of_names)):
            response = req.get(url)
            time.sleep(0.5)
            try:
                form = next(filter(lambda x: x in url,formats))
            except StopIteration:
                continue
            nparr = np.fromstring(response.content, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            images.append([name+form, img])
        return images
            
    def get_check_pics_factory(self):
        '''
        Factory function
        Parameters
        ----------
        col : instance of Collector class
            collector with oauth session
        Returns
        -------
        get_check_pics_fn : function
            "apply" function for dataframe (see more in function defenition)
        '''
        col = self
        def get_check_pics_fn(row):
            '''
            Returns row with face boxes if spotted 2 faces in an image
            
            '''
            img = col.get_images([row.image_location['url']],
                           [row.id_post], 
                           'collected_data') # that's stupid, i know.
            row.loc['face_boxes']=False
            if len(img):
                image = img[0][1]
                faces = Processpics_process.detect_faces(image)
                if len(faces)==2:
                    cv2.imwrite(os.path.join('collected_data',img[0][0]), image)
                    print(row)
                    row.loc['face_boxes']=faces
                    return row
            return row
        return get_check_pics_fn     