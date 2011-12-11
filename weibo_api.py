from weibopy.auth import OAuthHandler, BasicAuthHandler
from weibopy.api import API

password = 'your password'
username = 'your username'
app_key = 'your appkey'

def get_api():
    auth = BasicAuthHandler(username, password)
    api = API(auth, source = app_key)
    return api


