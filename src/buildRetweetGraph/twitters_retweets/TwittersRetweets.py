from __future__ import division
import got
import pickle
import tweepy
import time
import datetime

class TwittersRetweets:
    
    def __init__(self, since, until, query, twittapi):
        self.since = since
        self.until = until
        self.query = query
        self.twittapi = twittapi
        self.twittersfilepath = '../outcomes/'+query+'#twitters'+'.pickle' # default paths
        self.tweetsfilepath = '../outcomes/'+query+'#tweets'+'.pickle'
        self.retweetsfilepath = '../outcomes/'+query+'#retweets'+'.pickle'
    
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
    
    def setTwittersFilePath(self, path):
        self.twittersfilepath = path
        return self
    
    def setTweetsFilePath(self, path):
        self.tweetsfilepath = path
        return self
    
    def setRetweetsFilePath(self, path):
        self.retweetsfilepath = path
        return self
    
    def getQuery(self):
        return self.query
    
    def computeTwitters(self):
        
        tweetCriteria = got.manager.TweetCriteria().setSince(self.since).setUntil(self.until).setQuerySearch(self.query)
        twitters = got.manager.TweetManager.getTweets(tweetCriteria)
        
        dictioTwitters = {}
        dictioRetweets = {}
        tweetids = []
        
        for twitter in twitters:
            tweetids.append({twitter.id : twitter.username})
            
            if dictioTwitters.has_key(twitter.username):
                dictioTwitters[twitter.username] += 1   
            else:
                dictioTwitters.update({twitter.username : 1})
        
        #serialization
        with open(self.twittersfilepath,'wb') as handle:
            pickle.dump(dictioTwitters, handle, protocol=pickle.HIGHEST_PROTOCOL)
            
        with open(self.tweetsfilepath,'wb') as handle:
            pickle.dump(tweetids, handle, protocol=pickle.HIGHEST_PROTOCOL)
            
        with open(self.retweetsfilepath, 'wb') as handle:
            pickle.dump(dictioRetweets, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
        return dictioTwitters
    
    def computeRetweets(self, index):       
        ''' index of starting self.tweetids element '''
        
        with open(self.twittersfilepath,'rb') as handle:
            dictioTwitters = pickle.load(handle)
        with open(self.tweetsfilepath,'rb') as handle:
            tweets = pickle.load(handle)
        with open(self.retweetsfilepath, 'rb') as handle:
            dictioRetweets = pickle.load(handle)  

        if index < 0 or index > (len(tweets) - 1):
            return {}
        else:                        
            for i in range(index,len(tweets)):
                for tweetkey in tweets[i].keys():
                    
                    tweetuser = tweets[i][tweetkey] # user who tweetted
                    tweetcount = dictioTwitters[tweetuser] # his tweetcount about this topic
                    
                    try:
                        list_statuses = self.twittapi.retweets(tweetkey) # list of status objects of retweets
                    
                        for status in list_statuses:
                            retweetuser = (status._json['user']['screen_name']) # user who retweetted
                        
                            if not dictioTwitters.has_key(retweetuser): # insert retweet user in dictioTwitters though 
                                dictioTwitters.update({retweetuser: 0}) # he has not tweetted on the specific topic
                            
                            if dictioRetweets.has_key(retweetuser+tweetuser):
                                den = dictioRetweets[retweetuser+tweetuser]['retweetprob']*tweetcount + 1
                                dictioRetweets[retweetuser+tweetuser]['retweetprob'] = den/tweetcount
                        
                            else:
                                p = 1/tweetcount
                                dictioRetweets.update({(retweetuser+tweetuser):{'userfrom':retweetuser,'userto':tweetuser,'retweetprob':p}})
                    
                    except(tweepy.error.RateLimitError):   
                        print '###twitter rate limit error### sleeping 15 minutes...'
                        with open(self.twittersfilepath,'wb') as handle:
                            pickle.dump(dictioTwitters, handle, protocol=pickle.HIGHEST_PROTOCOL)
                        with open(self.retweetsfilepath, 'wb') as handle:
                            pickle.dump(dictioRetweets, handle, protocol=pickle.HIGHEST_PROTOCOL)
                        #tweets list is unchanged
                        #sleep and calls itself
                        print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                        time.sleep(900)
                        print 'awake'
                        return self.computeRetweets(i)
                                               
            with open(self.twittersfilepath,'wb') as handle:
                pickle.dump(dictioTwitters, handle, protocol=pickle.HIGHEST_PROTOCOL)
            with open(self.retweetsfilepath, 'wb') as handle:
                pickle.dump(dictioRetweets, handle, protocol=pickle.HIGHEST_PROTOCOL)
            #tweets list is unchanged
     
            return dictioRetweets
        
if __name__ == '__main__':
    pass