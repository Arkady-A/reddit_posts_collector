class Post():
    
    def __str__(self):
        return '[{}] {}'.format(self.id_post,self.title)
    
    def __init__(self, id_post, title, image_location):
        self.id_post = id_post
        self.image_location = image_location
        self.title = title