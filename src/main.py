import tweepy
import pickle
from buildRetweetGraph.twitters_retweets.TwittersRetweets import TwittersRetweets

auth = tweepy.OAuthHandler("", "")
auth.set_access_token("", "")
api = tweepy.API(auth)


if __name__ == '__main__':  
 
    #tws = TwittersRetweets('2017-10-1','2017-11-10', '#regionali #sicilia', api)
    
    #tws.computeTwitters('user_tweetcount.txt', 'tweets_id.txt')
    #usertw = open('tweets_id.txt','r')
    #obj = pickle.load(usertw)
    
    #print obj
    #print 'done'
    #usertw.close()
    #obj = [{'asd':'lol'}]
    #key = obj[0].keys()
    #value = obj[0][key[0]]
    '''for status in list:
        #json_str = json.dumps(status._json) #json.dumps(json object) returns a string
        print("retweet: ")
        print(status._json[u'user'][u'screen_name'])
        print(status._json[u'screen_name'])'''