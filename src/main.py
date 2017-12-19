import tweepy
from rwc import utilities
import networkx as nx
import matplotlib.pyplot as plt
from bsddb.dbshelve import HIGHEST_PROTOCOL

auth = tweepy.OAuthHandler("gG7Uto0Blfozze6eJFUUfCxtB", "IiTxDx6oX6YujOyDAqG2ORBFziEcSRAjHny5oT4G88XNysBxhZ")
auth.set_access_token("928998853361176578-zfPgfVajCvmIp8JoHxwSC7MfDf0lfgL", "G5r0R3iyO8ZOFYEK1UyIWJhWA4vWJoKkq5d2fcSz2EoOp")
api = tweepy.API(auth)


if __name__ == '__main__':  
    
    #from one month earlier to a week later the election date in Sicily
    '''
    tws = TwittersRetweets('2017-10-05','2017-11-12', '#regionali', api)
    
    eg = EndorsementGraph(tws)
    
    print 'please wait...building your DiGraph'
    
    digraph = eg.buildEGraph()
    
    nx.draw_random(digraph)
    plt.show()
    
    print 'done'
    '''
    
    G = nx.random_partition_graph([80,80],.30,.001, directed=True)
    
    nx.write_gpickle(G, '../outcomes/parted_graph.pickle', protocol=HIGHEST_PROTOCOL)
    
    nx.draw(G)
    plt.show()
    
    