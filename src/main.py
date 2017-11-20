import tweepy, pickle
from buildRetweetGraph.twitters_retweets.TwittersRetweets import TwittersRetweets
from buildRetweetGraph.graph.Graph import Graph

auth = tweepy.OAuthHandler("", "")
auth.set_access_token("", "")
api = tweepy.API(auth)


if __name__ == '__main__':  
    
    tws = TwittersRetweets('2017-11-1','2017-11-10', '#elezionisicilia', api)
    
    g = Graph(tws)
    
    print 'please wait...building your DiGraph'
    
    g.buildGraph()
    g.showGraph()
    
    print 'done'
