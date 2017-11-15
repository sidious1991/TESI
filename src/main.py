import tweepy
import json
import got

from test.test_decimal import file

auth = tweepy.OAuthHandler("", "")
auth.set_access_token("", "")
api = tweepy.API(auth)
'''
file_input = open("../tweets/democratic-candidate-timelines.txt", "r")

id_list = []

for line in file_input:
    id_list.append(int(line))
 
file_input.close()

status_list = api.statuses_lookup(id_list[0:5])

file_output = open("../tweets/parsed_tweets.txt", "a")

for status in status_list:
    json_str = json.dumps(status._json) #json.dumps(json object) returns a string
    file_output.write(json_str + "\n")

file_output.close()

print(status_list)
'''
'''
tweets = tweepy.Cursor(api.search, q = "#finoallafine", since="2017-11-8", until="2017-11-10",).items()

for tweet in tweets:
    json_str = json.dumps(tweet._json) #json.dumps(json object) returns a string
    print(json_str)
'''  

if __name__ == '__main__':  
    tweetCriteria = got.manager.TweetCriteria().setSince("2017-10-1").setUntil("2017-11-10").setQuerySearch("#Regionali #Sicilia")
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    for t in tweets:
        print t.username
    
    '''list = []  
      
    #for tweet in tweets:
    list = api.retweets(tweet.id)
        
    print tweet.username # on twitter: @username
    
    for status in list:
        #json_str = json.dumps(status._json) #json.dumps(json object) returns a string
        print("retweet: ")
        print(status._json[u'user'][u'screen_name'])'''