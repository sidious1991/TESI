import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    
    def __init__(self):
        pass
    
if __name__ == "__main__":
    
    DG = nx.DiGraph()
    DG.add_node(3, tweetcount = 3)
    DG.add_nodes_from([1,2])
    DG.add_weighted_edges_from([(1,2,0.5), (3,1,0.75)])
    print DG.nodes
    print DG.nodes(data = True)
    
    nx.draw(DG)
    plt.show()