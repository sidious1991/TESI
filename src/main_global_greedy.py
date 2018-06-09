import tweepy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from bsddb.dbshelve import HIGHEST_PROTOCOL
import rwc.rwc_lib as rwc_lib
import rwc.utilities as ut
import os, sys

auth = tweepy.OAuthHandler("", "")
auth.set_access_token("", "")
api = tweepy.API(auth)


if __name__ == '__main__':  
    
    #from one month earlier to a week later the election date in Sicily
    '''
    tws = TwittersRetweets('2017-10-05','2017-11-12', '#regionali', api)
    
    eg = EndorsementGraph(tws)
    
    print 'please wait...building your DiGraph'
    
    digraph = eg.buildEGraph()
    
    nx.draw_random(digraph)
    plt.show()
    
    print 'done'
    '''
    '''
    G = nx.random_partition_graph([80,80],.30,.001, directed=True)
    
    for edge in G.edges():
        G[edge[0]][edge[1]]['color'] = 'black'
    
    nx.write_gpickle(G, '../outcomes/parted_graph.pickle', protocol=HIGHEST_PROTOCOL)
    
    nx.draw(G)
    plt.show()
    '''
    dir_content = []
    graph_index = -1
    k1 = -1
    k2 = -1
    edges_to_recommend = -1
    
    print 'Greedy version. \nAvailable files: \n'
    
    for root, dirs, files in os.walk('../outcomes'):
        for i in range(0,len(files)):
            print str(i)+'-'+files[i]
            dir_content.append(files[i])
    
    while (graph_index >= len(dir_content) or graph_index < 0):
        try:
            graph_index = int(raw_input("\nChoose from one of these graphs and type its corresponding index: \n"))
        except EOFError as error:
            print '\nBye!'
            sys.exit(0)
    
    try:
        k1 = int(raw_input("\nChoose the number of best nodes of partition 0 (depends on strategy): \n"))
        k2 = int(raw_input("\nChoose the number of best nodes of partition 1 (depends on strategy): \n"))
        edges_to_recommend = int(raw_input("\nChoose the number of edges to recommend: \n"))
        if (k1 <= 0 or k2 <= 0) or (edges_to_recommend <= 0):
            print 'Bad input'
            sys.exit(1)
    except EOFError as error:
        print '\nBye!'
        sys.exit(0)
    
    graph_name = (dir_content[graph_index].split('.'))[0]
        
    path = '../outcomes/'+graph_name+'.pickle'
    
    print 'Chosen graph: %s \n'%graph_name
    print '########---Study of ratio in_degree/(out_degree + 1) in its average and its variance. Study of the trend of (in_degree, out_degree + 1, ratio) too.---########'
    
    print '-----------------------------------------------------------'
    
    avg_in_out = 0.0
    var_in_out = 0.0
    scanned_nodes = 0
    
    g = nx.read_gpickle(path)
    nodes = g.nodes()
        
    minimum = min(len(nodes),100)
        
    for node in nodes:
        
        in_deg = g.in_degree(node)
        out_deg = g.out_degree(node)
        ratio = (float(in_deg)/float(out_deg+1))
            
        '''Welford's method:'''
        old_avg = avg_in_out
        avg_in_out = (avg_in_out*scanned_nodes + ratio)/(scanned_nodes + 1)
        var_in_out = var_in_out + (ratio - avg_in_out)*(ratio - old_avg)
        
        scanned_nodes += 1
            
        if scanned_nodes < minimum:
            print "%d,%d,%.3f"%(in_deg,(out_deg+1),ratio)
        
    var_in_out /= (len(nodes)-1) # correct variance
        
    print path+" avg_in_out = %13.10f"%avg_in_out
    print path+" var_in_out = %13.10f"%var_in_out
    
    print '\n'  
  
    print '##########################---SIMULATIONS---###############################'
    
    strategies = ['in_deg_greedy','ratio_greedy','betwn_greedy']
    
    initGraphData = ut.computeData(None, g, 0.85, 0, percent_community=1)
    
    print "---------------------------------------------------------------------------------------------------------------------------"
    
    r = rwc_lib.rwc(0.85, initGraphData)
    print "Initial RWC score =%13.10f"%r[0] #%width.precisionf
    print "---------------------------------------------------------------------------------------------------------------------------"
    
    #Loop over strategies:
    for i in range(0,1):
        
        round_graph = nx.read_gpickle(path)
        round_data = initGraphData;
        #sorted_x_y = ut.sortNodes(None, g, initGraphData[8], initGraphData[9], i)#sorted by type sorting 'i'
        r1= r;
        print strategies[i]+' \n'
        print "rwc initial",r1[0], len(round_graph.edges())

        for k in range(0,edges_to_recommend): 
             
            R = []
  
            sorted_x_y = ut.sortNodes(None, round_graph, round_data[8], round_data[9], i)#sorted by type sorting 'i'
            sorted_dp = rwc_lib.deltaPredictorOrdered(None, round_graph, 0.85, k1, k2, sorted_x_y, round_data, r1)

            R.append(rwc_lib.fagin(sorted_dp,1))
            
            print R[0][1]
            
            (round_graph,opt,ratio,max_opt) = ut.addEdgeToGraph(None,round_graph,R[0][0],R[0][1],graph_name,strategies[i])
            
            #We assume that communities and partition do not change
            round_data = ut.computeData(None, round_graph, 0.85, i, percent_community=1, comms_part=(round_data[8],round_data[9]))  
            
            r1 = rwc_lib.rwc(0.85, round_data)
            
            print "rwc",r1[0]
            
        print "RWC score after addiction of accepted edges =%13.10f"%r1[0] #%width.precisionf
        print "Real Total Decrease RWC =%13.10f"%(r[0]-r1[0])
        print "-----------------------------------------------"
      
    print "-------------------------------------------------End of simulation---------------------------------------------------------"  
    
    
    
    
    
    