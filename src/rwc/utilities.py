from __future__ import division
import networkx as nx
import community
from networkx.classes.function import degree

def personalizedPageRank(path, graph):
    
    if path is None and graph is None:
        return ()
    
    g = nx.read_gpickle(path) if path is not None else graph
    
    comms = {}
    
    partition = community.best_partition(g.to_undirected())
    
    for node in partition.keys():
        key = partition[node]
        if comms.has_key(key):
            comms[key].append(node)
        else:
            comms.update({key:[node]})
            
    num_x = len(comms[0])
    num_y = len(comms[1])
    p_x = 1/num_x
    p_y = 1/num_y
    
    n_start_x = {}
    n_start_y = {}
    
    for key in comms.keys():
        for node in comms[key]:
            if key == 0:
                n_start_x.update({node: p_x})
                n_start_y.update({node: 0})             
            else:
                n_start_x.update({node: 0})
                n_start_y.update({node: p_y})
    
    e_x = n_start_x
    e_y = n_start_y
    
    r_x = nx.pagerank(g, alpha=0.85, personalization=e_x, nstart=n_start_x)
    r_y = nx.pagerank(g, alpha=0.85, personalization=e_y, nstart=n_start_y)
    
    return (r_x,r_y,comms)
    
def c_vectors(path, graph):
    
    if path is None and graph is None:
        return ()
    
    g = nx.read_gpickle(path) if path is not None else graph
    
    (r_x,r_y,comms) = personalizedPageRank(path, g)
    
    degrees_x = g.degree(comms[0])
    degrees_y = g.degree(comms[1])
    degrees = g.degree(g.nodes().keys())
    
    print degrees_x
    print degrees_y
    print degrees
    
if __name__ == '__main__':
    
    c_vectors('../../outcomes/parted_graph.pickle', None)
    
    
    
    
    
    
    
    
    