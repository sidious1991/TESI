import networkx as nx
import nxmetis
import matplotlib.pyplot as plt
import pickle

class EndorsementGraph:
    
    def __init__(self, twrtw):
        self.__twrtw = twrtw
        self.__graphfilepath = '../outcomes/'+twrtw.getQuery()+'#digraph.pickle' #default path
        
    def setEGraphFilePath(self, path):
        self.__graphfilepath = path
        return self
    
    def setTwrRtw(self, twrtw):
        self.__twrtw = twrtw
        return self
    
    '''
    @return: a digraph representing the endorsement graph about the query in the observation period
             specified in self.__twrtw. The digraph is serialized by pickle.
    '''
    def buildEGraph(self):
        
        digraph = nx.DiGraph(topic = self.__twrtw.getQuery());
        
        dictioTwitters = self.__twrtw.computeTwitters()
        dictioRetwitters = self.__twrtw.computeRetweets()
        
        for key in dictioTwitters.keys():
            digraph.add_node(key, tweetcount = dictioTwitters[key]['tweetcount'])# a node of graph has attribute tweetcount
            
        for key in dictioRetwitters.keys():
            #Garimella et al. consideration (minimum number of retweets by key[0] for key[1] content)
            if digraph.node[key[1]]['tweetcount']*dictioRetwitters[key]['retweetprob'] >= 2:
                digraph.add_edge(key[0], key[1], retweetprob=dictioRetwitters[key]['retweetprob'])    
         
        #Delete all the nodes with degree (outdegree+indegree) == 0
        for node in digraph.nodes().keys():
            if digraph.degree(node) == 0:
                digraph.remove_node(node)
                 
        #serialization
        nx.write_gpickle(digraph, self.__graphfilepath, protocol=pickle.HIGHEST_PROTOCOL)
        
        return digraph
    
    '''
    @return ...
    '''
    def communities(self, digraph):
        #metis or louvain?
        pass
    '''
    @param digraph: directed graph (endorsement graph for a particular query)
    @param edge: a tuple (source,target).It is a directed edge that does not 
                 belong to digraph we want to calculate the acceptance probability.
    @return: acceptance probability of edge (u,v)
    '''
    def LinkPrediction(self, digraph, edge):
        pass
          
if __name__ == "__main__":
    pass