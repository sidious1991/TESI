import tweepy, pickle, networkx as nx
import matplotlib.pyplot as plt
from buildRetweetGraph.twitters_retweets.TwittersRetweets import TwittersRetweets
from buildRetweetGraph.endorsementgraph.EndorsementGraph import EndorsementGraph

auth = tweepy.OAuthHandler("", "")
auth.set_access_token("", "")
api = tweepy.API(auth)


if __name__ == '__main__':  
    
    tws = TwittersRetweets('2017-10-20','2017-11-23', '#regionali', api)
    
    eg = EndorsementGraph(tws)
    
    print 'please wait...building your DiGraph'
    
    digraph = eg.buildEGraph()
   
    nx.draw_random(digraph)
    plt.show()
    
    print 'done'

    
    
