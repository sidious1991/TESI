import got

class Tweets:
    
    def __init__(self, since, until, query):
        self.since = since
        self.until = until
        self.query = query
        self.dictio = {}
    
    def setSince(self, since):
        self.since = since
        return self
    
    def setUntil(self, until):
        self.until = until
        return self
    
    def setQuery(self, query):
        self.query = query
        return self
    
    def setDict(self, dictio):
        self.dictio = dictio
        return self
    
    def computeTwitters(self):
        tweetCriteria = got.manager.TweetCriteria().setSince(self.since).setUntil(self.until).setQuerySearch(self.query)
        twitters = got.manager.TweetManager.getTweets(tweetCriteria)
        
        for twitter in twitters:
            if self.dictio.has_key(twitter.username):
                self.dictio[twitter.username] += 1   
            else:
                self.dictio.update({twitter.username : 1})
    
        return self.dictio
    
if __name__ == '__main__':
    
    tws = Tweets('2017-10-1','2017-11-10','#Regionali #Sicilia')
    twsDictio = tws.computeTwitters()
    
    print twsDictio
    