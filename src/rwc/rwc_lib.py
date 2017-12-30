from __future__ import division
import numpy as np
import networkx as nx
import utilities as ut

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
    @param type: if 0 nodes of each community ordered by degree_tot,
                 elif 1 nodes of each community ordered by in_degree,
                 else nodes of each community ordered by ratio in_degree/degree_tot
    @return a tuple of two lists and two dictionaries:
            the first is a list of tuples. Each tuple is of type (edge:delta_of_rwc).
            The list returned is ordered in increasing order of delta_of_rwc.
            the second is a list of tuples. Each tuple is of type (edge:acceptance_probability).
            The list returned is ordered in decreasing order of acceptance_probability.
            The two dictionaries are the unsorted versions of the two lists.
'''
def deltaProbabOrdered(path, graph, a, k1, k2, data, type, dictioPol):
    
    if path is None and graph is None or (k1 < 0 or k2 < 0):
        return
    
    g = nx.read_gpickle(path) if path is not None else graph
    
    if type == 0:
        sorted_x = data[8]
        sorted_y = data[9]
    else:
        (sorted_x,sorted_y) = ut.sortNodes(None, g, type)
    
    min_k1 = min(k1,len(sorted_x))
    min_k2 = min(k2,len(sorted_y))

    dictio_delta = {}
    dictio_prob = {}
    
    adj_mat = np.array(nx.attr_matrix(g)[0])
    
    if dictioPol is not None:
    
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
    else:

        for i in range(0,min_k1):
            for j in range(0,min_k2):
                if adj_mat[sorted_x[i][0]][sorted_y[j][0]] == 0:
                    e = (sorted_x[i][0],sorted_y[j][0])
                    dictio_delta.update({e : deltaRwc(None, g, a, data, e)})
                    dictio_prob.update({e : ut.acceptanceProbabilityGP(None, g, e, data)})
                if adj_mat[sorted_y[j][0]][sorted_x[i][0]] == 0:
                    e = (sorted_y[j][0],sorted_x[i][0])
                    dictio_delta.update({e : deltaRwc(None, g, a, data, e)})
                    dictio_prob.update({e : ut.acceptanceProbabilityGP(None, g, e, data)})

    dict_delta_sorted = sorted(dictio_delta.iteritems(), key=lambda (k,v):(v,k))
    dict_prob_sorted = sorted(dictio_prob.iteritems(), key=lambda (k,v):(v,k), reverse=True)

    return (dict_delta_sorted,dictio_delta,dict_prob_sorted,dictio_prob)


'''
    @param data: tuple returned by deltaProbabOrdered
    @param k: number of edge to propose
    @return the top k edges, whose scoring function is EXPECTED DELTA_RWC (id est acceptance_probability*delta_rwc)
            and aceptance_probability 
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
    bool = 0
    
    while threshold < R[maxkey]:
        
        if bool%2 == 0:
            i += 1
            R.update({list_I[i][0]:list_I[i][1]*dictio_P[list_I[i][0]]})#random access
            
        else:
            j += 1
            R.update({list_P[j][0]:list_P[j][1]*dictio_I[list_P[j][0]]})#random access
    
        threshold = list_I[i][1]*list_P[j][1]
        maxkey = max(R.keys(), key=(lambda k: R[k]))
        bool += 1
        
    sortedR = sorted(R.iteritems(), key=lambda (k,v):(v,k))
    '''
    i=0;
    while i < len(sortedR):
        sortedR[i]=(sortedR[i][0],(sortedR[i][1],dictio_P[sortedR[i][0]]))
        i+=1
    '''
    probR = {}
    for i in sortedR[0:k]:
        probR.update({i[0]:(i[1],dictio_P[i[0]])})#(edge):(delta*prob,prob)
    
    return (sortedR,probR)


if __name__ == '__main__':
    
    graphData = ut.computeData('../../outcomes/parted_graph.pickle', None, 40, 0.85)
      
    g = nx.read_gpickle('../../outcomes/parted_graph.pickle')
    
    print "---------------------------------------------------------------------------------------------------------------------------"
    print "Acceptance probability that does not depend on polarization score:"
    
    r = rwc(0.85, graphData)
    print "RWC score =%13.10f"%r #%width.precisionf
    print "---------------------------------------------------------------------------------------------------------------------------"
    R = []
    comment = ["Expected Decrease RWC -- degree type (HIGH-TO-HIGH) : ","Expected Decrease RWC -- in_degree type : ","Expected Decrease RWC -- ratio type : ","Expected Decrease RWC -- betweenness centrality : "]
    
    for i in range(0,4):
        
        sorted_dp = deltaProbabOrdered(None, g, 0.85, 20, 20, graphData, i, None)
    
        R.append(fagin(sorted_dp,30))
    
        print comment[i]
        print R[i][1]
        
        (new_graph,exp,ratio,max_exp) = ut.addEdgeToGraph('../../outcomes/parted_graph.pickle',R[i][1])
        mygraphData = ut.computeData(None, new_graph, 40, 0.85)   
        r1 = rwc(0.85, mygraphData)
        print "RWC score after addiction of accepted edges =%13.10f"%r1 #%width.precisionf
        print comment[i],"%13.10f"%exp
        print "Maximum Expected Decrease RWC : =%13.10f"%max_exp
        print "Delta TOT =%13.10f"%(r-r1), " aceptance_ratio :",ratio
        print "-----------------------------------------------"
    
    print "---------------------------------------------------------------------------------------------------------------------------"
    print "Acceptance probability that depends on polarization score:"
    
    dictioPol = ut.polarizationScore('../../outcomes/parted_graph.pickle', None, graphData)
    r = rwc(0.85, graphData)
    print "RWC score =%13.10f"%r #%width.precisionf
    print "---------------------------------------------------------------------------------------------------------------------------"
    R = []
    comment = ["Expected Decrease RWC -- degree type (HIGH-TO-HIGH) : ","Expected Decrease RWC -- in_degree type : ","Expected Decrease RWC -- ratio type : ","Expected Decrease RWC -- betweenness centrality : "]
    
    for i in range(0,4):
        
        sorted_dp = deltaProbabOrdered(None, g, 0.85, 20, 20, graphData, i, dictioPol)
    
        R.append(fagin(sorted_dp,30))
    
        print comment[i]
        print R[i][1]
        
        (new_graph,exp,ratio,max_exp) = ut.addEdgeToGraph('../../outcomes/parted_graph.pickle',R[i][1])
        mygraphData = ut.computeData(None, new_graph, 40, 0.85)   
        r1 = rwc(0.85, mygraphData)
        print "RWC score after addiction of accepted edges =%13.10f"%r1 #%width.precisionf
        print comment[i],"%13.10f"%exp
        print "Maximum Expected Decrease RWC : =%13.10f"%max_exp
        print "Delta TOT =%13.10f"%(r-r1), " aceptance_ratio :",ratio
        print "-----------------------------------------------"