from .models import Post
class Processor():
    def process_data(self, posts):
        processed_posts_list = []
        for post in posts:
            post_data = post['data']
            if 'preview' in post_data:
                images = post_data['preview']['images']
                if len(images)>0:
                    post_id = post_data['name']
                    title = post_data['title']
                    source_image = images[0]['source']
                    processed_posts_list.append(Post(post_id, title, source_image))
        return processed_posts_list
    
    
    def __init__(self):
        pass