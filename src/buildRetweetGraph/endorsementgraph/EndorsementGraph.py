import networkx as nx
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
            digraph.add_node(key, tweetcount = dictioTwitters[key])# a node of graph has attribute tweetcount
            
        
        for key in dictioRetwitters.keys():
            digraph.add_edge(dictioRetwitters[key]['userfrom'], dictioRetwitters[key]['userto'], retweetprob=dictioRetwitters[key]['retweetprob'])    
         
        #serialization
        nx.write_gpickle(digraph, self.__graphfilepath, protocol=pickle.HIGHEST_PROTOCOL)
        
        return digraph
          
if __name__ == "__main__":
    pass