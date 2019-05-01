class Post():
    
    def __str__(self):
        return '[{}] {}'.format(self.post_id,self.title)
    
    def __init__(self, post_id, title, image_location):
        self.post_id = post_id
        self.image_location = image_location
        self.title = title