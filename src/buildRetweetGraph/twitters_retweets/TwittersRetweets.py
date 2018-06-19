from __future__ import division
import pickle
import got
import tweepy
import time
import datetime

class TwittersRetweets:
    
    def __init__(self, since, until, query, twittapi):
        self.__since = since
        self.__until = until
        self.__query = query
        self.__twittapi = twittapi
    
    def setSince(self, since):
        self.__since = since
        return self
    
    def setUntil(self, until):
        self.__until = until
        return self
    
    def setQuery(self, query):
        self.__query = query
        return self
    
    def setTwittApi(self, twittapi):
        self.__twittapi = twittapi
        return self
    
    def getQuery(self):
        return self.__query
    
    '''
    @return: the tuple (dictioTwitters,tweetids,dictioRetweets).
    '''
    def __computeTwitters(self):
        
        tweetCriteria = got.manager.TweetCriteria().setSince(self.__since).setUntil(self.__until).setQuerySearch(self.__query)
        twitters = got.manager.TweetManager.getTweets(tweetCriteria)
        
        dictioTwitters = {}
        dictioRetweets = {}
        tweetids = []
        
        for twitter in twitters:
            tweetids.append({twitter.id : twitter.username})
            
            if dictioTwitters.has_key(twitter.username):
                dictioTwitters[twitter.username]['tweetcount'] += 1   
            else:
                dictioTwitters.update({twitter.username : {'tweetcount':1}})
        
        return (dictioTwitters,tweetids,dictioRetweets)

    '''
    @param: path is the path to the text file in which to write all the retweets of the hashtag indicated in the query.
    @return: dictioRetweets, that is a dictionary like {(retweetuser,tweetuser):{retweetprob:..},...},
             of retweets about the query.
    '''
    def computeRetweets(self,path):
        
        (dictioTwitters,tweets,dictioRetweets) = self.__computeTwitters()  

        i = 0
        
        while i<len(tweets):
            
            tweetkey = (tweets[i].keys())[0] # the current dictionary of tweet id contains olny one key (tweet id)
            tweetuser = tweets[i][tweetkey] # user who tweetted
            #tweetcount = dictioTwitters[tweetuser]['tweetcount'] # his tweetcount about this topic
        
            try:
                list_statuses = self.__twittapi.retweets(tweetkey) # list of status objects of retweets
                    
                for status in list_statuses:
                    retweetuser = (status._json['user']['screen_name']) # user who retweetted
                        
                    if not dictioTwitters.has_key(retweetuser): # insert retweet user in dictioTwitters though 
                        dictioTwitters.update({retweetuser: {'tweetcount':0}}) # he has not tweetted on the specific topic
                            
                    if dictioRetweets.has_key((retweetuser,tweetuser)):
                        dictioRetweets[(retweetuser,tweetuser)]['retweetcount'] += 1
                        
                    else:
                        dictioRetweets.update({(retweetuser,tweetuser):{'retweetcount':1}})
                        
                i += 1
        
            except(tweepy.error.RateLimitError):   
                print '###twitter rate limit error### sleeping 15 minutes...'
                #sleep and calls itself
                print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                time.sleep(900)
                print 'awake'
                continue # i unchanged

        with open(path,'w') as f:
            for key in dictioRetweets.keys():
                f.write(key[0]+','+key[1]+','+str(dictioRetweets[key]['retweetcount'])+'\n')

        return dictioRetweets

if __name__ == '__main__':
    pass
