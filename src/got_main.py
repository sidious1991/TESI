import tweepy
import buildRetweetGraph.twitters_retweets as b

auth = tweepy.OAuthHandler("", "")
auth.set_access_token("", "")
api = tweepy.API(auth)

if __name__ == '__main__':  
    
    hashtag = raw_input("\nChoose the hashtag (#hashtag)\n")
   
    since = raw_input("\nChoose the date to start looking for tweets / retweets (YYYY-MM-DD)\n")

    to = raw_input("\nChoose the final date of the search (YYYY-MM-DD)\n")	

    tws = b.TwittersRetweets(since,to, hashtag, api)
    
    path = '../inputs/'+hashtag+'_retweet_graph'+'.txt'

    tws.computeRetweets(path)
    
    print 'File saved in '+path
    
  
