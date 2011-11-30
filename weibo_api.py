from weibopy.auth import OAuthHandler, BasicAuthHandler
from weibopy.api import API

password = '86842128'
username = 'reg.1@lifeis.ws'
app_key = '3535699815'

def get_api():
    auth = BasicAuthHandler('reg.1@lifeis.ws', '86842128')
    api = API(auth, source = '3535699815')
    return api


