from __future__ import division
import networkx as nx
import matplotlib.pyplot as plt
import community
import scipy as sp
import numpy as np
from scipy import linalg

'''
    Source : 'Reducing Controversy by Connecting Opposing Views' - Garimella et alii
'''

'''
    @param path: is the path to diGraph (if not None)
    @param graph: is a diGraph (if not None)
    @param a: is the dumping parameter (probability to continue)
    @return the communities of the graph, the personalization vectors for the communities,
            the c_x and c_y vectors, the partition and m_x and m_y inverted
'''
def computeData(path, graph, k, a):
    
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
    
    e_x = n_start_x # uniform in x
    e_y = n_start_y # uniform in y
    
    c_x = []
    c_y = []
    
    degrees = g.degree(g.nodes().keys())
    degrees_x = g.degree(comms[0]) #comm X -- to be ordered
    degrees_y = g.degree(comms[1]) #comm Y -- to be ordered
    sorted_x = sorted(degrees_x ,key=lambda tup: tup[1], reverse=True)
    sorted_y = sorted(degrees_y ,key=lambda tup: tup[1], reverse=True)
    
    #inizialization
    for i in range(0,len(degrees)):
        c_x.append(0)
        c_y.append(0)
    
    minimum = min(k,len(sorted_x),len(sorted_y))
    
    for i in range(0,minimum):
        c_x[sorted_x[i][0]] = 1
        c_y[sorted_y[i][0]] = 1
    
    m_x = M(None, g, a, e_x)
    m_y = M(None, g, a, e_y)
    
    return (e_x,e_y,c_x,c_y,linalg.inv(m_x),linalg.inv(m_y),comms,partition)
    
'''
   This is Random Walk Controversy score.
   @param path: is the path to diGraph (if not None)
   @param graph: is a diGraph (if not None) 
   @param a: is the dumping parameter (probability to continue)
   @param k: is the number of the 'high-degree vertices' to consider in each community
   @return the rwc of the diGraph
'''    
def rwc(path, graph, a, k):
    
    if path is None and graph is None:
        return
    
    g = nx.read_gpickle(path) if path is not None else graph

    (e_x,e_y,c_x,c_y,m_x_inv,m_y_inv,comms,part) = computeData(path, g, k, a)    
    
    sub_c = np.subtract(c_x,c_y)
    
    sub_m = np.subtract(np.dot(m_x_inv,e_x.values()),np.dot(m_y_inv,e_y.values()))
   
    rwc_m = np.dot(np.dot(sub_c,(1-a)),sub_m)
    
    return rwc_m
   
'''
    @param path: is the path to diGraph (if not None)
    @param graph: is a diGraph (if not None) 
    @param a: is the dumping parameter (probability to continue)
    @param personal: is the restart vector
    @return the M_x or M_y matrix (source Garimella et alii), depending on the restart vector (personal)
'''
def M(path, graph, a, personal):
    
    if path is None and graph is None:
        return
    
    g = nx.read_gpickle(path) if path is not None else graph
    
    P = nx.google_matrix(g, alpha=1, personalization=personal, dangling=personal) # Transition matrix (per row)

    I = np.identity(len(g.nodes()))

    m = np.subtract(I,np.dot(a,P))

    return m


def deltaRwc(path, graph, a, k, data, sourcev, destv):

    if path is None and graph is None:
        return
    
    g = nx.read_gpickle(path) if path is not None else graph

    (e_x,e_y,c_x,c_y,m_x_inv,m_y_inv,comms,part) = data 
    
    sourcecomm = part[sourcev] #community of start vertex
    dangling = (g.out_degree(sourcev) == 0) #bool source is a dangling vertex
    
    sub_c = np.subtract(c_x,c_y)
    
    u = np.zeros(len(g.nodes()))
    u[sourcev] = 1
    
    v = np.zeros(len(g.nodes()))
    v[destv] = 1
    
    

if __name__ == '__main__':
    
    r = rwc('../../outcomes/parted_graph.pickle', None, 0.85, 40)
    print r
    