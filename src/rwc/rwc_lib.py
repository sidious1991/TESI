from __future__ import division
import numpy as np
import networkx as nx
import utilities as ut
from rwc.utilities import polarizationScore

'''
    Source : 'Reducing Controversy by Connecting Opposing Views' - Garimella et alii
'''

'''
   This is Random Walk Controversy score.
   @param a: is the dumping parameter (probability to continue)
   @param data: tuple returned by computeData
   @return the rwc of the diGraph
'''    
def rwc(a, data):
    
    (e_x,e_y,c_x,c_y,mats_x,mats_y,comms,part,sorted_x,sorted_y) = data    
    
    sub_c = np.subtract(c_x,c_y)
    
    sub_m = np.subtract(np.dot(mats_x[0],e_x.values()),np.dot(mats_y[0],e_y.values()))
   
    rwc_m = np.dot(np.dot(sub_c,(1-a)),sub_m)
    
    return rwc_m
   
   
'''
    @param path: is the path to diGraph (if not None)
    @param graph: is a diGraph (if not None) 
    @param a: is the dumping parameter (probability to continue)
    @param data: tuple returned by computeData
    @param edge: edge to add
    @return the delta rwc by 'Sherman-Morrison'
'''
def deltaRwc(path, graph, a, data, edge):

    if path is None and graph is None:
        return
    
    g = nx.read_gpickle(path) if path is not None else graph

    (e_x,e_y,c_x,c_y,mats_x,mats_y,comms,part,sorted_x,sorted_y) = data 
    
    sourcev = edge[0]
    destv = edge[1]
    
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


'''
    @param path: is the path to diGraph (if not None)
    @param graph: is a diGraph (if not None)
    @param a: is the dumping parameter (probability to continue)
    @param k1: number of nodes of community X to consider, 
               ordered in decreasing order of degree
    @param k2: number of nodes of community Y to consider, 
               ordered in decreasing order of degree
    @param dictioPol: polarization score of nodes ({node:polarization ...})
    @return a tuple of two lists:
            the first is a list of tuples. Each tuple is of type (edge:decrease_of_rwc).
            The list returned is ordered in increasing order of decrease_of_rwc.
            the second is a list of tuples. Each tuple is of type (edge:acceptance_probability).
            The list returned is ordered in decreasing order of acceptance_probability.
'''
def deltaProbabOrdered(path, graph, a, k1, k2, data, dictioPol):
    
    if path is None and graph is None or (k1 < 0 or k2 < 0):
        return
    
    g = nx.read_gpickle(path) if path is not None else graph
    sorted_x = data[8]
    sorted_y = data[9]

    min_k1 = min(k1,len(sorted_x))
    min_k2 = min(k2,len(sorted_y))

    dictio_delta = {}
    dictio_prob = {}
    
    adj_mat = np.array(nx.attr_matrix(g)[0])
    
    for i in range(0,min_k1):
        for j in range(0,min_k2):
            if adj_mat[sorted_x[i][0]][sorted_y[j][0]] == 0:
                e = (sorted_x[i][0],sorted_y[j][0])
                dictio_delta.update({e : deltaRwc(None, g, a, data, e)})
                dictio_prob.update({e : ut.acceptanceProbability((dictioPol[sorted_x[i][0]],dictioPol[sorted_y[j][0]]))})
            if adj_mat[sorted_y[j][0]][sorted_x[i][0]] == 0:
                e = (sorted_y[j][0],sorted_x[i][0])
                dictio_delta.update({e : deltaRwc(None, g, a, data, e)})
                dictio_prob.update({e : ut.acceptanceProbability((dictioPol[sorted_y[j][0]],dictioPol[sorted_x[i][0]]))})

    dict_delta_sorted = sorted(dictio_delta.iteritems(), key=lambda (k,v):(v,k))
    dict_prob_sorted = sorted(dictio_prob.iteritems(), key=lambda (k,v):(v,k), reverse=True)
    '''
    count = 0
    for i in range(0,len(dict_sorted)):
        count += dict_sorted[i][1]
    
    print count
    '''
    return (dict_delta_sorted,dict_prob_sorted)

'''
    @param k: number of edge to propose
'''
def fagin(sorted_delta, sorted_prob, k):
    
    if k < 0 or len(sorted_delta) != len(sorted_prob):
        return 
    
    min_k = min(k,len(sorted_delta))
    

if __name__ == '__main__':
    
    graphData = ut.computeData('../../outcomes/parted_graph.pickle', None, 40, 0.85)
    dictioPol = ut.polarizationScore('../../outcomes/parted_graph.pickle', None, graphData)
    
    r = rwc(0.85, graphData)
    print r
    
    sorted = deltaProbabOrdered('../../outcomes/parted_graph.pickle', None, 0.85, 10, 10, graphData,dictioPol)
    print sorted[0]#delta
    print sorted[1]#prob
    
    