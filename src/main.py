import tweepy, pickle
from buildRetweetGraph.twitters_retweets.TwittersRetweets import TwittersRetweets
from buildRetweetGraph.endorsementgraph.EndorsementGraph import EndorsementGraph

auth = tweepy.OAuthHandler("", "")
auth.set_access_token("", "")
api = tweepy.API(auth)


if __name__ == '__main__':  
    
    tws = TwittersRetweets('2017-11-1','2017-11-10', 'regionali sicilia', api)
    
    eg = EndorsementGraph(tws)
    
    print 'please wait...building your DiGraph'
    
    eg.buildEGraph()
    eg.showEGraph()
    
    print 'done'
