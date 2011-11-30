from weibo_user import WeiboUser
from weibo_api import get_api

api = get_api()

def fetch():
    top_user = api.friends_ids().ids
    for id in top_user[-2:]:
        u = api.get_user(id)
        WeiboUser.save_weibo_api(u)

if __name__ == '__main__':
    fetch()

