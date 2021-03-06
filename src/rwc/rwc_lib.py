from __future__ import division
import numpy as np
import networkx as nx
import utilities as ut
import math

'''
    Source : 'Reducing Controversy by Connecting Opposing Views' - Garimella et alii
'''

'''
   This is Random Walk Controversy score.
   @param a: is the probability to continue (1 - a is the restart probability)
   @param data: tuple returned by computeData
   @return the rwc of the diGraph, c_x*r_x, c_y*r_y
'''    
def rwc(a, data):
    
    (sorted_x,sorted_y,e_x,e_y,c_x,c_y,mats_x,mats_y,comms,part,inter_comm_edges_ratio) = data    
    
    sub_c = np.subtract(c_x,c_y)
    sub_c_alpha = np.dot((1-a),sub_c)
    
    m_e_x = np.dot(mats_x[0],list(e_x.values()))
    m_e_y = np.dot(mats_y[0],list(e_y.values()))
    
    sub_m = np.subtract(m_e_x, m_e_y)
   
    rwc_m = np.dot(np.transpose(sub_c_alpha),sub_m)
    
    c_x_r_x = np.dot(c_x, np.dot((1-a), m_e_x))
    c_y_r_y = np.dot(c_y, np.dot((1-a), m_e_y))
        
    return rwc_m,c_x_r_x,c_y_r_y
   
   
'''
    @param path: is the path to diGraph (if not None)
    @param graph: is a diGraph (if not None) 
    @param a: is the probability to continue (1 - a is the restart probability)
    @param data: tuple returned by computeData
    @param edge: edge to add
    @return the delta rwc by 'Sherman-Morrison'
'''
def deltaRwc(path, graph, a, data, edge):

    if path is None and graph is None:
        return
    
    g = nx.read_gpickle(path) if path is not None else graph

    (sorted_x,sorted_y,e_x,e_y,c_x,c_y,mats_x,mats_y,comms,part,inter_comm_edges_ratio) = data 
    
    sourcev = edge[0]
    destv = edge[1]
    
    sourcecomm = part[sourcev] #community of start vertex
    p = mats_x[1] if sourcecomm == 0 else mats_y[1]
    q = g.out_degree(sourcev) #out_degree of source
    source_col = p[:,sourcev] #col of sourcev in transposed transition matrix
    dangling = (q == 0) #bool source is a dangling vertex
    
    sub_c = np.subtract(c_x,c_y)
    
    u = np.zeros(len(g.nodes()))
    u[sourcev] = 1
    
    v = np.zeros(len(g.nodes()))
    v[destv] = 1
    
    z_x = np.zeros(len(g.nodes()))
    z_y = np.zeros(len(g.nodes()))
    
    if dangling:
        z_x = np.subtract(list(e_x.values()),v)
        z_y = np.subtract(list(e_y.values()),v)
        
    else:
        z_x = np.dot(1/(q+1),source_col)
        z_x[destv] = -1/(q+1)
        z_y = np.dot(1/(q+1),source_col)
        z_y[destv] = -1/(q+1)
        
    mx_z = np.dot(a,np.dot(mats_x[0],z_x))
    u_mx = np.dot(np.transpose(u),mats_x[0])
    my_z = np.dot(a,np.dot(mats_y[0],z_y))
    u_my = np.dot(np.transpose(u),mats_y[0])
    den_x = 1 + np.dot(np.transpose(u),mx_z)
    den_y = 1 + np.dot(np.transpose(u),my_z)
    num_x = np.outer(mx_z,u_mx)
    num_y = np.outer(my_z,u_my)
    
    x_factor = np.dot(np.dot(num_x, float(1/den_x)),list(e_x.values()))#vector 
    y_factor = np.dot(np.dot(num_y, float(1/den_y)),list(e_y.values()))#vector
    
    ''' Sherman-Morrison Formula '''
    
    delta_partial = np.dot(np.transpose(sub_c),np.subtract(y_factor,x_factor))
    delta = np.dot((1-a),delta_partial)
    
    return delta


'''
    @param path: is the path to diGraph (if not None)
    @param graph: is a diGraph (if not None)
    @param a: is the probability to continue (1 - a is the restart probability)
    @param k1: number of nodes of community X to consider, 
               ordered depending on type t
    @param k2: number of nodes of community Y to consider, 
               ordered depending on type t
    @param sorted_x_y: tuple (sorted_x,sorted_y) returned by sortNodes
    @param data: tuple returned by computeData
    @param r: the tuple returned by rwc function
    @return a tuple of two lists and two dictionaries:
            the first is a list of tuples. Each tuple is of type (edge:delta_of_rwc).
            The list returned is ordered in increasing order of delta_of_rwc.
            the second is a list of tuples. Each tuple is of type (edge:link_predictor).
            The list returned is ordered in decreasing order of link_predictor.
            The two dictionaries are the unsorted versions of the two lists.
'''
def deltaPredictorOrdered(path, graph, a, k1, k2, sorted_x_y, data, r):
    
    if path is None and graph is None or (k1 < 0 or k2 < 0):
        return
    
    g = nx.read_gpickle(path) if path is not None else graph
    sorted_x = sorted_x_y[0]
    sorted_y = sorted_x_y[1]
    
    ratio = (r[1]/r[2]) #c_x*r_x/c_y*r_y
    print r[1],r[2],ratio
     
    min_k1 = min(k1,len(sorted_x))
    min_k2 = min(k2,len(sorted_y))

    dictio_delta = {}
    dictio_predictor = {}
    
    adj_mat = np.array(nx.attr_matrix(g)[0])
    
    for i in range(0,min_k1):
        for j in range(0,min_k2):
            if adj_mat[sorted_x[i][0]][sorted_y[j][0]] == 0:
                e = (sorted_x[i][0],sorted_y[j][0])
                dictio_delta.update({e : deltaRwc(None, g, a, data, e)})
                dictio_predictor.update({e : ut.KatzScore(g, e, data[10])})
                
            if adj_mat[sorted_y[j][0]][sorted_x[i][0]] == 0:
                e = (sorted_y[j][0],sorted_x[i][0])
                dictio_delta.update({e : deltaRwc(None, g, a, data, e)})
                dictio_predictor.update({e : ut.KatzScore(g, e, data[10])})
                        
    dict_delta_sorted = sorted(dictio_delta.iteritems(), key=lambda (k,v):(v,k))
    dict_predictor_sorted = sorted(dictio_predictor.iteritems(), key=lambda (k,v):(v,k), reverse=True)
            
    return (dict_delta_sorted,dictio_delta,dict_predictor_sorted,dictio_predictor)


'''
    @param data: tuple returned by deltaPredictorOrdered
    @param k: number of edge to propose
    @return the top k edges, whose scoring function is link_predictor*delta_rwc
            and link_predictor 
            Source: http://www.inf.unibz.it/dis/teaching/SDB/reports/report_mitterer.pdf
'''
def fagin(data, k):
    
    if k < 0 or len(data[0]) != len(data[2]):
        return 
    
    min_k = min(k,len(data[0]))
    
    list_I = data[0]
    list_P = data[2]
    
    dictio_I = data[1]
    dictio_P = data[3]
    
    R = {}
    threshold = list_I[0][1]*list_P[0][1] 
    R.update({list_I[0][0]:list_I[0][1]*dictio_P[list_I[0][0]]})#random access
    R.update({list_P[0][0]:list_P[0][1]*dictio_I[list_P[0][0]]})#random access
    maxkey = max(R.keys(), key=(lambda k: R[k]))
    i = 0
    j = 0
    counter = 0
    
    while threshold < R[maxkey]:
        
        if counter%2 == 0:
            i += 1
            if i >= min_k:
                break
            R.update({list_I[i][0]:list_I[i][1]*dictio_P[list_I[i][0]]})#random access
            
        else:
            j += 1
            if j >= min_k:
                break
            R.update({list_P[j][0]:list_P[j][1]*dictio_I[list_P[j][0]]})#random access
    
        threshold = list_I[i][1]*list_P[j][1]
        maxkey = max(R.keys(), key=(lambda k: R[k]))
        counter += 1
        
    sortedR = sorted(R.iteritems(), key=lambda (k,v):(v,k))
    '''
    i=0;
    while i < len(sortedR):
        sortedR[i]=(sortedR[i][0],(sortedR[i][1],dictio_P[sortedR[i][0]]))
        i+=1
    '''
    print sortedR[0:min_k] # sorted list of : [((node_from, node_to),link_predictor*delta_rwc), ((node_from, node_to),link_predictor*delta_rwc),..]
    predictorR = {}
    for i in sortedR[0:min_k]:
        predictorR.update({i[0]:(dictio_I[i[0]],dictio_P[i[0]])})#(edge):(delta_rwc,link_predictor)
    
    return (sortedR[0:min_k],predictorR)


if __name__ == '__main__':
    pass