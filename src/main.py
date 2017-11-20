import tweepy, pickle, networkx as nx
import matplotlib.pyplot as plt
from buildRetweetGraph.twitters_retweets.TwittersRetweets import TwittersRetweets
from buildRetweetGraph.endorsementgraph.EndorsementGraph import EndorsementGraph

auth = tweepy.OAuthHandler("", "")
auth.set_access_token("", "")
api = tweepy.API(auth)


if __name__ == '__main__':  
    
    
    tws = TwittersRetweets('2017-11-1','2017-11-10', '#regionali', api)
    
    eg = EndorsementGraph(tws)
    
    print 'please wait...building your DiGraph'
    
    eg.buildEGraph()
    eg.showEGraph()
    
    print 'done'
    
    '''
    with open('../outcomes/#regionali#digraph.pickle','rb') as handle:
        dg = pickle.load(handle)
        print nx.number_of_edges(dg)
        print nx.number_of_nodes(dg)
    '''
    