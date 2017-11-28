import networkx as nx
import community
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
        
    def buildEGraph(self):
        
        digraph = nx.DiGraph(topic = self.__twrtw.getQuery());
        
        dictioTwitters = self.__twrtw.computeTwitters()
        dictioRetwitters = self.__twrtw.computeRetweets()
        
        for key in dictioTwitters.keys():
            digraph.add_node(key, tweetcount = dictioTwitters[key]['tweetcount'])# a node of graph has attribute tweetcount
            
        
        for key in dictioRetwitters.keys():
            digraph.add_edge(key[0], key[1], retweetprob=dictioRetwitters[key]['retweetprob'])    
         
        #serialization
        nx.write_gpickle(digraph, self.__graphfilepath, protocol=pickle.HIGHEST_PROTOCOL)
        
        return digraph
    
    '''
    @return A tuple with: 
            -the partition of digraph (using Louvain Algorithm), with communities numbered from 0 to number of communities
            -number of communities
    '''
    def communities(self, digraph):
        
        partition = community.best_partition(digraph.to_undirected())
        return (partition,float(len(set(partition.values())))) 
    
    '''
    @param digraph: directed graph (endorsement graph for a particular query
    @param edge: a tuple (source,target).It is an edge that does not belong to 
                 digraph we want to calculate the prediction index.
    @return: a list of probabilities. For each path from source to target this 
            function computes the product of retweetprobs for each edge in the path.
            *** here insert my heuristics **
    '''
    def MyLinkPrediction(self, digraph, edge):
              
        for path in nx.all_simple_paths(digraph, edge[0], edge[1]):
            pass
          
if __name__ == "__main__":
    pass