import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    
    def __init__(self):
        pass
    
if __name__ == "__main__":
    
    DG = nx.DiGraph()
    DG.add_nodes_from([1,2,3], tweetcount = 1)
    DG.add_weighted_edges_from([(1,2,0.5), (3,1,0.75)])
    DG[3][1]['weight'] += 1
    print DG[3][1]
    DG.node[1]['tweetcount'] += 1
    print DG.node[1]
    #print DG.nodes
    #print DG.nodes(data = True)
    
    #nx.draw(DG)
    #plt.show()