import got
import pickle

class TwittersRetweets:
    
    def __init__(self, since, until, query, twittapi):
        self.since = since
        self.until = until
        self.query = query
        self.twittapi = twittapi
    
    def setSince(self, since):
        self.since = since
        return self
    
    def setUntil(self, until):
        self.until = until
        return self
    
    def setQuery(self, query):
        self.query = query
        return self
    
    def setTwittApi(self, twittapi):
        self.twittapi = twittapi
        return self
       
    def computeTwitters(self, twittersfilepath, tweetsfilepath):
        
        tweetCriteria = got.manager.TweetCriteria().setSince(self.since).setUntil(self.until).setQuerySearch(self.query)
        twitters = got.manager.TweetManager.getTweets(tweetCriteria)
        
        dictioTwitters = {}
        tweetids = []
        
        for twitter in twitters:
            tweetids.append({twitter.id : twitter.username})
            
            if dictioTwitters.has_key(twitter.username):
                dictioTwitters[twitter.username] += 1   
            else:
                dictioTwitters.update({twitter.username : 1})
        
        #serialization
        twitters = open(twittersfilepath,'w')
        pickle.dump(dictioTwitters, twitters)
        tweets = open(tweetsfilepath,'w')
        pickle.dump(tweetids, tweets)
        
        twitters.close()
        tweets.close()
        
        return dictioTwitters
    
    def computeRetweets(self, index, twittersfilepath, tweetsfilepath):       
        ''' index of starting self.tweetids element '''

        if index < 0:
            return 'index not valid'
        else:
            twittersfile = open(twittersfilepath,'r')
            twitters = pickle.load(twittersfile)
            tweetsfile = open(tweetsfilepath,'r')
            tweets = pickle.load(tweetsfile)
            
            retweets = {}
            
            if index > len(tweets) - 1:
                return 'done'
            
            for i in range(index,len(tweets)):
                for tweetkey in tweets[i].keys():
                    tweetusername = tweets[i][tweetkey]
            
            twittersfile.close()
            tweetsfile.close()
            
            return 'done'
        
if __name__ == '__main__':
    pass