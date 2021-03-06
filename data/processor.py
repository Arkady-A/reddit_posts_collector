from .models import Post
import pandas as pd 
import re
import cv2
import sys

class Post_process():
    @staticmethod
    def process_data(posts):
        '''
        From list of dictionaries to list of post instances
        Parameters
        ----------
        posts : dict 
            json file that've been returned by get
        
        Returns
        -------
        list of models.Post 
        '''
        processed_posts_list = []
        for post in posts:
            post_data = post['data']
            if 'preview' in post_data:
                images = post_data['preview']['images']
                if len(images)>0:
                    id_post = post_data['name']
                    title = post_data['title']
                    source_image = images[0]['source']
                    processed_posts_list.append(Post(id_post, title, 
                                                     source_image))
        last_id = posts[-1]['data']['name']
        return processed_posts_list,last_id
    @staticmethod
    def to_dataframe(list_of_posts):
        '''
        Process the list of posts and return a dataframe
        '''
        dict_list = []
        for post in list_of_posts:
            dict_list.append(vars(post))
        return pd.DataFrame(dict_list)
            
    
    def __init__(self):
        pass

class Processpics_process():

    @staticmethod
    def detect_faces(image):
        '''
        This function returns images of detected faces if any
        Parameters
        ----------
        image : file
            an image in which to find a face
        
        Returns
        -------
        faces : list of lists  [x,y,w,h]
        
        None
        '''
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # TO RUN THE LINE BELOW YOU NEED TO PLACE 
        # haarcascade_frontalface_default.xml
        # IN THE FOLDER WITH start.py FILE
        faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=3,
            minSize=(30, 30)
        )
        return faces
    #TODO
    # ADD DOCUMENTATION        
    @staticmethod
    def parse_factory(regex = [r'(.)/(.{1,2})/(.*)\[(.*)>(.*)=',
                               r'(.)/(.{1,2})/(.*)\[(.*)>(.*)>',
                               r'(.)/(.{1,2})/(.*)\[(.*)[<>](.*)]',
                               ]):
        def parse_data(row):

            grp = re.match(regex[0], row.title)
            if grp is None:
                for reg in regex:
                    grp = re.match(reg, row.title)
                    if grp is not None:
                        break
            try:
                row.loc['gender'] = grp.group(1)
                row.loc['age'] = grp.group(2)
                row.loc['height'] = grp.group(3)
                row.loc['weight_before'] = grp.group(4)
                row.loc['weight_after'] = grp.group(5)
                row.loc['stripped_title'] = row.title[:60]
            except AttributeError as e:
                print(e)
                print(row.title[:80])
            return row
        return parse_data 
            