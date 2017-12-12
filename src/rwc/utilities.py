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
            the c_x and c_y vectors, the partition and mats_x, mats_y tuples from M method
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
    
    return (e_x,e_y,c_x,c_y,mats_x,mats_y,comms,partition)
    
    
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
   This is Random Walk Controversy score.
   @param a: is the dumping parameter (probability to continue)
   @param data: tuple returned by computeData
   @return the rwc of the diGraph
'''    
def rwc(a, data):
    
    (e_x,e_y,c_x,c_y,mats_x,mats_y,comms,part) = data    
    
    sub_c = np.subtract(c_x,c_y)
    
    sub_m = np.subtract(np.dot(mats_x[0],e_x.values()),np.dot(mats_y[0],e_y.values()))
   
    rwc_m = np.dot(np.dot(sub_c,(1-a)),sub_m)
    
    return rwc_m
   
'''
    @param path: is the path to diGraph (if not None)
    @param graph: is a diGraph (if not None) 
    @param a: is the dumping parameter (probability to continue)
    @param data: tuple returned by computeData
    @param sourcev: outgoing node
    @param destv: incoming node
    @return the delta rwc by 'Sherman-Morrison'
'''
def deltaRwc(path, graph, a, data, sourcev, destv):

    if path is None and graph is None:
        return
    
    g = nx.read_gpickle(path) if path is not None else graph

    (e_x,e_y,c_x,c_y,mats_x,mats_y,comms,part) = data 
    
    sourcecomm = part[sourcev] #community of start vertex
    p = mats_x[1] if sourcecomm == 0 else mats_y[1]
    q = g.out_degree(sourcev) #out_degree of source
    source_row = p[sourcev,:] #row of sourcev in its transition matrix
    dangling = (q == 0) #bool source is a dangling vertex
    
    sub_c = np.subtract(c_x,c_y)
    
    u = np.zeros(len(g.nodes()))
    u[sourcev] = 1
    
    v = np.zeros(len(g.nodes()))
    v[destv] = 1
    
    z_x = np.zeros(len(g.nodes()))
    z_y = np.zeros(len(g.nodes()))
    
    if dangling:
        z_x = np.subtract(e_x,v)
        z_y = np.subtract(e_y,v)
        
    else:
        #print source_row
        z_x = np.dot(1/(q+1),source_row)
        z_x[destv] = -1/(q+1)
        z_y = np.dot(1/(q+1),source_row)
        z_y[destv] = -1/(q+1)
        
    
    mx_z = np.dot(a,np.dot(mats_x[0],z_x))
    u_mx = np.dot(u,mats_x[0])
    my_z = np.dot(a,np.dot(mats_y[0],z_y))
    u_my = np.dot(u,mats_y[0])
    den_x = 1 + np.dot(u,mx_z)
    den_y = 1 + np.dot(u,my_z)
    num_x = np.dot(mx_z,u_mx)
    num_y = np.dot(my_z,u_my)
    
    x_factor = np.dot((num_x/den_x),e_x.values())#vector 
    y_factor = np.dot((num_y/den_y),e_y.values())#vector
    
    ''' Sherman-Morrison Formula '''
    
    delta = (1-a)*np.dot(sub_c,np.subtract(y_factor,x_factor))
    
    return delta

def fagin():
    pass

if __name__ == '__main__':
    
    graphData = computeData('../../outcomes/parted_graph.pickle', None, 40, 0.85)
    r = rwc(0.85, graphData)
    print r
    
    delta = deltaRwc('../../outcomes/parted_graph.pickle', None, 0.85, graphData, 0, 150)
    print delta
    
    