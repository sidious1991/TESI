import tweepy
import json
from test.test_decimal import file

#auth = tweepy.OAuthHandler(...)
#auth.set_access_token(...)

api = tweepy.API(auth)

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

#print(status_list)


    
    
    