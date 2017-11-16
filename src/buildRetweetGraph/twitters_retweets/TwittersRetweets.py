import got

class TwittersRetweets:
    
    def __init__(self, since, until, query, twittapi):
        self.since = since
        self.until = until
        self.query = query
        self.dictioTwitters = {} #nodes of future graph: {twitter.username: tweet_count}
        self.dictioRetweets = {} #edges of future graph
        self.tweetids = [] # a list of object like [{tweet_id: username}]
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
    
    def getTweetIds(self):
        return self.tweetids
    
    def getDictioTwitters(self):
        return self.dictioTwitters
    
    def getDictioRetweets(self):
        return self.dictioRetweets
        
    def computeTwitters(self):
        tweetCriteria = got.manager.TweetCriteria().setSince(self.since).setUntil(self.until).setQuerySearch(self.query)
        twitters = got.manager.TweetManager.getTweets(tweetCriteria)
        
        for twitter in twitters:
            self.tweetids.append({twitter.id : twitter.username})
            
            if self.dictioTwitters.has_key(twitter.username):
                self.dictioTwitters[twitter.username] += 1   
            else:
                self.dictioTwitters.update({twitter.username : 1})
    
        return self.dictioTwitters
    
    def computeRetweets(self):
        
        temp_list = []
        
        for twid in self.tweetids:
            for key in twid:
                temp_list = self.twittapi.retweets(key) #retweets al tweet key dell'utente twid.key
                user = twid[key]
                
            
            
    
if __name__ == '__main__':
    pass