import tweepy, pickle
from buildRetweetGraph.twitters_retweets.TwittersRetweets import TwittersRetweets
from buildRetweetGraph.graph.Graph import Graph

auth = tweepy.OAuthHandler("", "")
auth.set_access_token("", "")
api = tweepy.API(auth)


if __name__ == '__main__':  
       
    tws = TwittersRetweets('2017-11-1','2017-11-10', '#regionali#sicilia', api)
    
    g = Graph(tws)
    g.buildgraph()
    g.showGraph()
    
    '''
    tw = tws.computeTwitters()
    print tw
    rtws = tws.computeRetweets(0)
    print rtws
    '''
    '''
    for status in list:
        #json_str = json.dumps(status._json) #json.dumps(json object) returns a string
        print("retweet: ")
        print(status._json[u'user'][u'screen_name'])
        print(status._json[u'screen_name'])
    '''