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
    @param k: is the number of the 'high-degree vertices' to consider in each community
    @param a: is the dumping parameter (probability to continue)
    @return the communities of the graph, the personalization vectors for the communities,
            the c_x and c_y vectors, the partition and mats_x, mats_y tuples from M method,
            the sorted_x and sorted_y nodes of communities (by degree)
'''
def computeData(path, graph, k, a):
    
    if path is None and graph is None or k < 0:
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
    
    e_x = {}
    e_y = {}
    
    for key in comms.keys():
        for node in comms[key]:
            if key == 0:
                e_x.update({node: p_x})
                e_y.update({node: 0})             
            else:
                e_x.update({node: 0})
                e_y.update({node: p_y})
    
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
    
    mats_x = M(None, g, a, e_x)
    mats_y = M(None, g, a, e_y)
    
    return (e_x,e_y,c_x,c_y,mats_x,mats_y,comms,partition,sorted_x,sorted_y)
    
    
'''
    @param path: is the path to diGraph (if not None)
    @param graph: is a diGraph (if not None) 
    @param a: is the dumping parameter (probability to continue)
    @param personal: is the restart vector
    @return the M_x or M_y matrix inverted (source Garimella et alii), depending on the restart vector (personal)
            and P_x or P_y matrix
'''
def M(path, graph, a, personal):
    
    if path is None and graph is None:
        return
    
    g = nx.read_gpickle(path) if path is not None else graph
    
    P = nx.google_matrix(g, alpha=1, personalization=personal, dangling=personal) # Transition matrix (per row)

    I = np.identity(len(g.nodes()))

    m = np.subtract(I,np.dot(a,P))

    m_inv = linalg.inv(m)
    
    p_array = np.array(P)

    return (m_inv,p_array)
    
    
'''
    @param pscores: is a tuple identifying the polarity scores of a directed edge (from,to).
    @return the acceptance probability of the directed edge (from,to).
            The probability is based on the dipole and work concepts.
    future: total_acceptance_probability = alpha*P(work,dipole)+beta*P_other(other_factors)
            alpha + beta = 1
'''
def acceptanceProbability(pscores):
    
    fromp = pscores[0]
    top = pscores[1]
    
    work = -np.exp(-(top))+np.exp(-(fromp)) if (fromp <= top) else np.exp(fromp)-np.exp(top)
    
    prob = np.exp(-work)
    
    return prob


'''
    @param path: is the path to diGraph (if not None)
    @param graph: is a diGraph (if not None) 
    @param data: tuple returned by computeData
    @return polarization score for each node in digraph.
            Algorithm used (adapted) from source:
            
            Measuring Political Polarization: Twitter shows the two sides of Venezuela
            A. J. Morales, J. Borondo, J. C. Losada and R. M. Benito
            Grupo de Sistemas Complejos. Universidad Politecnica de Madrid.
            ETSI Agronomos, 28040, Madrid, Spain
'''
def polarizationScore(path, graph, data):
    
    if path is None and graph is None:
        return
    
    g = nx.read_gpickle(path) if path is not None else graph
    
    (e_x,e_y,c_x,c_y,mats_x,mats_y,comms,part,sorted_x,sorted_y) = data
    
    max_iter = 16
    
    dictio_polarization = {0:{}}
    adj = nx.attr_matrix(g)
    adj_array = np.array(adj[0])
    nodes = adj[1]
    
    #initialization
    for node in part.keys():
        
        mypart = part[node]
        maxpol = 1 if mypart == 0 else -1
        
        mypol = maxpol if g.degree(node) == 0 else maxpol*(g.in_degree(node)/g.degree(node))
        
        dictio_polarization[0].update({node:mypol})

    #iterations
    for i in range(1,max_iter+1):
        dictio_polarization.update({i:{}})
        for j in nodes:
            row = adj_array[j]
            sum_pol = 0
            for k in nodes:
                sum_pol += row[k]*dictio_polarization[i-1][k]
            
            dictio_polarization[i].update({j:(sum_pol/g.out_degree(j))})

    return dictio_polarization[max_iter]


if __name__ == '__main__':
    
    pass
    
    
    
    


