import tweepy
from rwc import utilities
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from bsddb.dbshelve import HIGHEST_PROTOCOL
import rwc.rwc_lib as rwc_lib
import rwc.utilities as ut

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
    print '########---Study, for all graphs, of average of ratio in_degree/(out_degree + 1) and its variance---########'
       
    graph = ['../outcomes/parted_graph.pickle','../outcomes/retweet_graph_beefban.pickle','../outcomes/retweet_graph_russia_march.pickle','../outcomes/retweet_graph_ukraine.pickle','../outcomes/retweet_graph_nemtsov.pickle']
    
    for path in graph:
        print '-----------------------------------------------------------'
    
        avg_in_out = 0.0
        var_in_out = 0.0
        scanned_nodes = 0
    
        G = nx.read_gpickle(path)
    
        for node in G.nodes():
        
            avg_in_out = (avg_in_out*scanned_nodes + (G.in_degree(node)/(G.out_degree(node)+1)))/(scanned_nodes + 1)
            var_in_out = (var_in_out*scanned_nodes + (G.in_degree(node)/(G.out_degree(node)+1) - avg_in_out)**2)/(scanned_nodes + 1)
        
            scanned_nodes += 1
        
        print path+" avg_in_out = %13.10f"%avg_in_out
        print path+" var_in_out = %13.10f"%var_in_out
    
    print '\n'    
    print '##########################---SIMULATIONS---###############################'
    
    g = nx.read_gpickle('../outcomes/parted_graph.pickle')

    R = []
    comment = ["Opt Total Decrease RWC -- in_degree type (HIGH-TO-HIGH) : ","Opt Total Decrease RWC -- ratio type : ","Opt Total Decrease RWC -- betweenness centrality : ", "Opt Total Decrease RWC -- avg in_degree type : "]
    graph_name = 'retweet_graph_ukraine'
    strategies = ['in_deg','ratio','betwn','avg_in_deg']
    '''
        graph_data_rwc = computeData(0,percent = 1)
        rwc(0.85, graph_data_rwc)
    '''
    
    for i in range(0,3):
        
        graphData = ut.computeData(None, g, 0.85, i, percent_community=0.5)
    
        print "---------------------------------------------------------------------------------------------------------------------------"
    
        r = rwc_lib.rwc(0.85, graphData)
        print "RWC score =%13.10f"%r[0] #%width.precisionf
        print "---------------------------------------------------------------------------------------------------------------------------"
        
        sorted_dp = rwc_lib.deltaPredictorOrdered(None, g, 0.85, 40, 40, graphData, r)
    
        R.append(rwc_lib.fagin(sorted_dp,20))
        
        print R[i][1]
        
        (new_graph,opt,ratio,max_opt) = ut.addEdgeToGraph('../outcomes/parted_graph.pickle',R[i][0],R[i][1],graph_name,strategies[i])
        mygraphData = ut.computeData(None, new_graph, 0.85, i, percent_community=0.5)  
        
        r1 = rwc_lib.rwc(0.85, mygraphData)
        print "RWC score after addiction of accepted edges =%13.10f"%r1[0] #%width.precisionf
        print comment[i],"%13.10f"%opt
        print "Maximum Optimum Decrease RWC : =%13.10f"%max_opt
        print "Real Total Decrease RWC =%13.10f"%(r[0]-r1[0]), " acceptance_ratio :",ratio
        print "-----------------------------------------------"
      
    print "-------------------------------------------------End of simulation---------------------------------------------------------"  
    
    
    
    
    
    
    
    