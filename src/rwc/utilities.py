from __future__ import division
import networkx as nx
import community
import scipy as sp
import numpy as np

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
    
def rwc(path, graph, k):
    
    if path is None and graph is None:
        return
    
    g = nx.read_gpickle(path) if path is not None else graph

    (r_x,r_y,comms) = personalizedPageRank(path, g)
    
    degrees_x = g.degree(comms[0]) #comm X -- to be ordered
    degrees_y = g.degree(comms[1]) #comm Y -- to be ordered
    degrees = g.degree(g.nodes().keys())
    sorted_x = sorted(degrees_x ,key=lambda tup: tup[1], reverse=True)
    sorted_y = sorted(degrees_y ,key=lambda tup: tup[1], reverse=True)
    
    c_x = []
    c_y = []
    
    #inizialization
    for i in range(0,len(degrees)):
        c_x.append(0)
        c_y.append(0)
    
    minimum = min(k,len(sorted_x),len(sorted_y))
    
    for i in range(0,minimum):
        c_x[sorted_x[i][0]] = 1
        c_y[sorted_y[i][0]] = 1
    
    rwc = 0
    
    for i in range(0,len(degrees)):
        rwc += (c_x[i]-c_y[i])*(r_x[i]-r_y[i])
    
    return rwc

def M(path, graph, a, personal):
    
    if path is None and graph is None:
        return
    
    g = nx.read_gpickle(path) if path is not None else graph
    
    p = nx.google_matrix(g, alpha=a, personalization=personal)#per righe

    id = np.identity(len(g.nodes()))

    m = np.subtract(id,np.dot(a,p)) 

    return m

if __name__ == '__main__':
    
    r = rwc('../../outcomes/parted_graph.pickle', None, 40)
    print r
    
    
    
    
    
    
    
    
    