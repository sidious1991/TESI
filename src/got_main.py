import tweepy
import buildRetweetGraph.twitters_retweets as b

auth = tweepy.OAuthHandler("MmmyW1HEqjNGVGtpECx5fvHLH", "WwAgwBr0Jue77YqGs0voir29tc4HEClFrgo0oGm42i0EToA8cq")
auth.set_access_token("928998853361176578-zfPgfVajCvmIp8JoHxwSC7MfDf0lfgL", "G5r0R3iyO8ZOFYEK1UyIWJhWA4vWJoKkq5d2fcSz2EoOp")
api = tweepy.API(auth)

if __name__ == '__main__':  
    
    hashtag = raw_input("\nChoose the hashtag (#hashtag)\n")
   
    since = raw_input("\nChoose the date to start looking for tweets / retweets (YYYY-MM-DD)\n")

    to = raw_input("\nChoose the final date of the search (YYYY-MM-DD)\n")	

    tws = b.TwittersRetweets(since,to, hashtag, api)
    
    path = '../inputs/'+hashtag+'_retweet_graph'+'.txt'

    tws.computeRetweets(path)
    
    print 'File saved in '+path
    
  
