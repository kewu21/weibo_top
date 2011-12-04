from weibo_user import WeiboUser
from datetime import date
import networkx as nx
import matplotlib.pyplot as plt

def build_graph():
    pair_list = WeiboUser.get_top_100_pair()
    DG = nx.DiGraph()
    DG.add_edges_from([(foer, twitter_user) for twitter_user, foer in
        pair_list])
    for twitter_id in DG.nodes():
        t = WeiboUser.get_by_id(twitter_id)
        node = DG.node[twitter_id]
        node['weibo_id'] = t.user_id
        node['label'] = t.scrn_name
        node['scrn_name'] = t.scrn_name
        node['name'] = t.name
        node['follower_count'] = t.foer_cnt
        node['friend_count'] = t.friend_cnt
        node['status_count'] = t.status_cnt
        node['description']  = t.desc
        node['location'] = t.location
        node['created_at'] = str(t.created_at)
        node['verified'] = t.verified
        node['twitter_age'] = (date.today() - t.created_at).days
        node['daily_tweet'] = t.status_cnt*1.0/node['twitter_age']
        node['follower_count_top100'] = len([(id, foer) for id, foer 
            in pair_list if id == twitter_id])
        node['friend_count_top100'] = len([(id, foer) for id, foer 
            in pair_list if foer == twitter_id])

    return DG

def build_graph_encoded():
    pair_list = WeiboUser.get_top_100_pair()
    print
    DG = nx.DiGraph()
    DG.add_edges_from(pair_list)
    for twitter_id in DG.nodes():
        t = WeiboUser.get_by_id(twitter_id)
        node = DG.node[twitter_id]
        node['weibo_id'] = t.user_id
        node['label'] = t.scrn_name.encode('utf-8')
        node['screen_name'] = t.scrn_name.encode('utf-8')
        node['name'] = t.name.encode('utf-8')
        node['follower_count'] = t.foer_cnt
        node['friend_count'] = t.friend_cnt
        node['status_count'] = t.status_cnt
        node['description']  = t.desc.encode('utf-8')
        node['location'] = t.location.encode('utf-8')
        node['created_at'] = str(t.created_at)
        node['verified'] = t.verified
        node['twitter_age'] = (date.today() - t.created_at).days
        node['daily_tweet'] = t.status_cnt*1.0/node['twitter_age']
        node['follower_count_top100'] = len([(id, foer) for id, foer 
            in pair_list if id == twitter_id])
        node['friend_count_top100'] = len([(id, foer) for id, foer 
            in pair_list if foer == twitter_id])

    return DG
    
if __name__ == '__main__':
    G = build_graph()
    nx.write_graphml(G, 'weibo.graphml')
    plt.draw()
