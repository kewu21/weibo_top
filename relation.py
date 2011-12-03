from weibo_api import get_api
from weibo_user import WeiboUser
from time import sleep

a = get_api()
TOP_100 = WeiboUser.get_top_100_by_foer()


def relationship_top():
    for id in TOP_100:
        print 'analysis id', id
        sleep(1)
        for foer in TOP_100:
            if id != foer and not WeiboUser.get_relation(id, foer)\
                    and not WeiboUser.get_non_relation(id, foer):
                print 'analysis', id, 'and', foer, '...'
                try:
                    e = a.exists_friendship(id,foer)
                except:
                    continue
                if e.friends:
                    print id, 'is followered by', foer, 'saving..'
                    WeiboUser.save_relationship(id, foer)
                else:
                    print id, 'is noe followered by', foer, 'saving..'
                    WeiboUser.save_relationship(id, foer)
                    WeiboUser.save_non_relationship(id, foer)
                sleep(1)

if __name__=='__main__':
    relationship_top()
