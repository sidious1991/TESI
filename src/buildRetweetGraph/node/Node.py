class Node:
    
    def __init__(self):
        self.tweet_count = 0
        self.username = ''
        self.topic = ''
        
    def setTweetCount(self, tcount):
        self.tweet_count = tcount
        return self
    
    def setUsername(self, usern):
        self.username = usern
        return self
    
    def setTopic(self, topic):
        self.topic = topic
        
    def getTweetCount(self):
        return self.tweet_count
    
    def getUsername(self):
        return self.username
    
    def getTopic(self):
        return self.topic
    
    def incrTweetCount(self):
        self.tweet_count += 1
        return self
    
if __name__ == "__main__":
    
    n = Node()
    n.incrTweetCount()
    print n.getTweetCount()
    