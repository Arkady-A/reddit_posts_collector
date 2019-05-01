from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

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
        return self.session.get('https://oauth.reddit.com/r/{}/new'.format(subreddit),
                                params={'limit':limit})


