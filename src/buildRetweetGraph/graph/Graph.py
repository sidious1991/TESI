import networkx as nx
import matplotlib.pyplot as plt
import pickle
from buildRetweetGraph.twitters_retweets.TwittersRetweets import TwittersRetweets

class Graph:
    
    def __init__(self, twrtw):
        self.digraph = nx.DiGraph(topic = twrtw.getQuery())
        self.twrtw = twrtw
        self.graphfilepath = twrtw.getQuery()+'#digraph'+'.pickle' #default path
        
    def setGraphFilePath(self, path):
        self.graphfilepath = path
        return self
        
    def buildGraph(self):
        dictioTwitters = self.twrtw.computeTwitters()
        dictioRetwitters = self.twrtw.computeRetweets(0)
        
        for key in dictioTwitters.keys():
            self.digraph.add_node(key, tweetcount = dictioTwitters[key])# a node of graph has attribute tweetcount
            
        
        for key in dictioRetwitters.keys():
            self.digraph.add_edge(dictioRetwitters[key]['userfrom'], dictioRetwitters[key]['userto'], retweetcount=dictioRetwitters[key]['retweetcount'])    
         
        #serialization
        with open(self.graphfilepath,'wb') as handle:
            pickle.dump(self.digraph, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
        return self.digraph
    
    def showGraph(self):
        nx.draw(self.digraph)
        plt.show()
    
if __name__ == "__main__":
  
    '''
    DG = nx.DiGraph()
    DG.add_nodes_from([1,2,3], tweetcount = 1)
    DG.add_weighted_edges_from([(1,2,0.5), (3,1,0.75)])
    DG[3][1]['weight'] += 1
    print DG[3][1]
    DG.node[1]['tweetcount'] += 1
    print DG.node[1]
    print DG.nodes
    print DG.nodes(data = True)
    
    nx.draw(DG)
    plt.show()
    '''