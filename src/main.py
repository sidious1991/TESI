import tweepy
from buildRetweetGraph.twitters_retweets.TwittersRetweets import TwittersRetweets

auth = tweepy.OAuthHandler("", "")
auth.set_access_token("", "")
api = tweepy.API(auth)


if __name__ == '__main__':  
 
    tws = TwittersRetweets('2017-10-1','2017-11-10', '#regionali #sicilia', api)
    tws.computeTwitters()
    tws.computeRetweets()  
    #for tweet in tweets:
    #list = api.retweets('')
        
    #print tweet.username # on twitter: @username
    
    '''for status in list:
        #json_str = json.dumps(status._json) #json.dumps(json object) returns a string
        print("retweet: ")
        print(status._json[u'user'][u'screen_name'])
        print(status._json[u'screen_name'])'''