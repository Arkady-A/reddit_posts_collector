from .models import Post
import pandas as pd 

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
                    processed_posts_list.append(Post(id_post, title, source_image))
        return processed_posts_list
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