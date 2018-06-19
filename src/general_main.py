import tweepy
import numpy as np
import time
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
from bsddb.dbshelve import HIGHEST_PROTOCOL
import rwc.rwc_lib as rwc_lib
import rwc.utilities as ut
import os, sys
from buildRetweetGraph.endorsementgraph import EndorsementGraph

auth = tweepy.OAuthHandler("", "")
auth.set_access_token("", "")
api = tweepy.API(auth)

'''-----Greedy-----'''
def greedy_alg():
    
    dir_content = []
    graph_index = -1
    k1 = -1
    k2 = -1
    edges_to_recommend = -1
    
    print '########## Greedy section ########## \nAvailable files: \n'
    
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
    
    print '\n##### Chosen graph: %s #####\n'%graph_name
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
    
    start_time = time.time()
    #Loop over strategies:
    for i in range(0,len(strategies)):
        
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
    print "Time elapsed: %f"%(time.time() - start_time)


'''-----Global-----'''
def global_alg():
    
    dir_content = []
    graph_index = -1
    k1 = -1
    k2 = -1
    edges_to_recommend = -1
    
    print '########## Global section ########## \nAvailable files: \n'
    
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
    
    print '\n##### Chosen graph: %s ######\n'%graph_name
    print '########---Study of ratio in_degree/(out_degree + 1) in its average and its variance. \nStudy of the trend of (in_degree, out_degree + 1, ratio) too.---########'
    
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

    R = []
    comment = ["Opt Total Decrease RWC -- in_degree type (HIGH-TO-HIGH) : ","Opt Total Decrease RWC -- ratio type : ","Opt Total Decrease RWC -- betweenness centrality : "]
    strategies = ['in_deg','ratio','betwn']
    
    initGraphData = ut.computeData(None, g, 0.85, 0, percent_community=1)
    
    print "---------------------------------------------------------------------------------------------------------------------------"
    
    r = rwc_lib.rwc(0.85, initGraphData)
    print "Initial RWC score =%13.10f"%r[0] #%width.precisionf
    print "---------------------------------------------------------------------------------------------------------------------------"
    
    start_time = time.time()
    #Loop over strategies:
    for i in range(0,len(strategies)):
             
        print strategies[i]+'\n'
    
        sorted_x_y = ut.sortNodes(None, g, initGraphData[8], initGraphData[9], i)#sorted by type sorting 'i'
             
        sorted_dp = rwc_lib.deltaPredictorOrdered(None, g, 0.85, k1, k2, sorted_x_y, initGraphData, r)
    
        R.append(rwc_lib.fagin(sorted_dp,edges_to_recommend))
        
        print R[i][1]
        
        (new_graph,opt,ratio,max_opt) = ut.addEdgeToGraph(path,None,R[i][0],R[i][1],graph_name,strategies[i])
        finalGraphData = ut.computeData(None, new_graph, 0.85, i, percent_community=1, comms_part=(initGraphData[8],initGraphData[9]))  
        
        r1 = rwc_lib.rwc(0.85, finalGraphData)
        print "RWC score after addiction of accepted edges =%13.10f"%r1[0] #%width.precisionf
        print comment[i],"%13.10f"%opt
        print "Maximum Optimum Decrease RWC : =%13.10f"%max_opt
        print "Real Total Decrease RWC =%13.10f"%(r[0]-r1[0]), " acceptance_ratio :",ratio
        print "-----------------------------------------------"
      
    print "-------------------------------------------------End of simulation---------------------------------------------------------"  
    print "Time elapsed: %f"%(time.time() - start_time)

'''-----Local-----'''
def local_alg():
    
    dir_content = []
    graph_index = -1
    percent_comm = -1
    k1 = -1
    k2 = -1
    edges_to_recommend = -1
    
    print '########## Local section ########## \nAvailable files: \n'
    
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
        percent_comm = float(raw_input("\nChoose the percentage of nodes of each community to consider: \n"))
        k1 = int(raw_input("\nChoose the number of best nodes of partition 0 (depends on strategy): \n"))
        k2 = int(raw_input("\nChoose the number of best nodes of partition 1 (depends on strategy): \n"))
        edges_to_recommend = int(raw_input("\nChoose the number of edges to recommend: \n"))
        if (percent_comm > 1 or percent_comm <= 0) or (k1 <= 0 or k2 <= 0) or (edges_to_recommend <= 0):
            print 'Bad input'
            sys.exit(1)
    except EOFError as error:
        print '\nBye!'
        sys.exit(0)
    
    graph_name = (dir_content[graph_index].split('.'))[0]
        
    path = '../outcomes/'+graph_name+'.pickle'
    
    print '\n##### Chosen graph: %s #####\n'%graph_name
    print '########---Study of ratio in_degree/(out_degree + 1) in its average and its variance. \nStudy of the trend of (in_degree, out_degree + 1, ratio) too.---########'
    
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

    R = []
    comment = ["Opt Total Decrease RWC -- in_degree type (HIGH-TO-HIGH) : ","Opt Total Decrease RWC -- ratio type : ","Opt Total Decrease RWC -- betweenness centrality : "]
    strategies = ['in_deg','ratio','betwn']

    start_time = time.time()
    for i in range(0,len(strategies)):
        
        graphData = ut.computeData(None, g, 0.85, i, percent_community=percent_comm)
    
        print "---------------------------------------------------------------------------------------------------------------------------"
    
        r = rwc_lib.rwc(0.85, graphData)
        print "RWC score =%13.10f"%r[0] #%width.precisionf
        print "---------------------------------------------------------------------------------------------------------------------------"
        
        sorted_x_y = (graphData[0],graphData[1])
        sorted_dp = rwc_lib.deltaPredictorOrdered(None, g, 0.85, k1, k2, sorted_x_y, graphData, r)
    
        R.append(rwc_lib.fagin(sorted_dp,edges_to_recommend))
        
        print R[i][1]
        
        (new_graph,opt,ratio,max_opt) = ut.addEdgeToGraph(path,None,R[i][0],R[i][1],graph_name,strategies[i])
        mygraphData = ut.computeData(None, new_graph, 0.85, i, percent_community=percent_comm, comms_part=(graphData[8],graphData[9]))  
        
        r1 = rwc_lib.rwc(0.85, mygraphData)
        print "RWC score after addiction of accepted edges =%13.10f"%r1[0] #%width.precisionf
        print comment[i],"%13.10f"%opt
        print "Maximum Optimum Decrease RWC : =%13.10f"%max_opt
        print "Real Total Decrease RWC =%13.10f"%(r[0]-r1[0]), " acceptance_ratio :",ratio
        print "-----------------------------------------------"
      
    print "-------------------------------------------------End of simulation---------------------------------------------------------"
    print "Time elapsed: %f"%(time.time() - start_time)

'''-----Plot-----'''
def plot():    
    
    dir_output_graph_content = []
    dir_outcomes_content = []
    graph_index = -1
    
    print '########## Plot graph section ########## \nAvailable files: \n'
    
    for root, dirs, files in os.walk('../outcomes'):
        for i in range(0,len(files)):
            print str(i)+'-'+files[i]
            dir_outcomes_content.append(files[i])
    
    while (graph_index >= len(dir_outcomes_content) or graph_index < 0):
        try:
            graph_index = int(raw_input("\nChoose from one of these graphs and type its corresponding index: \n"))
        except EOFError as error:
            print '\nBye!'
            sys.exit(0)
    
    graph_outcomes_name = (dir_outcomes_content[graph_index].split('.'))[0]
    graph_index = -1
    
    for root, dirs, files in os.walk('../output_graph'):
        counter = 0
        for i in range(0,len(files)):
            if graph_outcomes_name in files[i]:
                dir_output_graph_content.append(files[i])
                print str(counter)+'-'+files[i]
                counter += 1
    
    while (graph_index >= len(dir_output_graph_content) or graph_index < 0):
        try:
            graph_index = int(raw_input("\nChoose the output_graph in function of strategy: \n"))
        except EOFError as error:
            print '\nBye!'
            sys.exit(0)
    
    graph_output_graph_name = (dir_output_graph_content[graph_index].split('.'))[0]
    
    
    g_original = nx.read_gpickle('../outcomes/'+graph_outcomes_name+'.pickle')#graph before adding recommended edges
    g = nx.read_gpickle('../output_graph/'+graph_output_graph_name+'.pickle')#graph after adding recommended edges
    
    edges = g.edges()
    
    node_list = []
    nodes_info = {}#{node:(in_deg,out_deg,ratio),...}
    bipartite_graph = nx.DiGraph()#for coloring
    
    for u,v in edges:
        
        if 'color' in g[u][v] and g[u][v]['color'] == 'red':
            
            in_deg_u = g_original.in_degree(u)
            out_deg_u = g_original.out_degree(u)
            ratio_u = float(in_deg_u)/(float(out_deg_u + 1))
            in_deg_v = g_original.in_degree(v)
            out_deg_v = g_original.out_degree(v)
            ratio_v = float(in_deg_v)/(float(out_deg_v + 1))
            
            nodes_info.update({u:(in_deg_u,out_deg_u,ratio_u)})
            nodes_info.update({v:(in_deg_v,out_deg_v,ratio_v)})
            
            node_list.append(u)
            node_list.append(v)
            
            bipartite_graph.add_edge(u, v)#for coloring
        else:
            g[u][v]['color'] = 'black'
            
    g_sub = g.subgraph(node_list)
      
    colors = [g[u][v]['color'] for u,v in g_sub.edges()]
    
    c = bipartite.color(bipartite_graph)
    list_black = []
    list_red = []
    
    for node in g_sub.nodes():
        
        if c[node] == 0:
            list_black.append(node)
        else:
            list_red.append(node)
    
    pos = nx.spring_layout(g_sub)
    
    nx.draw_networkx_nodes(g_sub, pos, nodelist=list_black, node_color = 'red')
    nx.draw_networkx_nodes(g_sub, pos, nodelist=list_red, node_color = 'yellow')
    nx.draw_networkx_edges(g_sub, pos, edge_color=colors)
    nx.draw_networkx_labels(g_sub, pos, labels = nodes_info, font_size=9)
    plt.show()

'''-----Load-----'''
def load_graph():
    
    dir_input_content = []
    graph_index = -1

    print '########## Load graph section ########## \nAvailable files: \n'

    for root, dirs, files in os.walk('../inputs'):
        for i in range(0,len(files)):
            print str(i)+'-'+files[i]
            dir_input_content.append(files[i])

    while (graph_index >= len(dir_input_content) or graph_index < 0):
        try:
            graph_index = int(raw_input("\nChoose from one of these graphs (.txt files) and type its corresponding index: \n"))
        except EOFError as error:
            print '\nBye!'
            sys.exit(0)
    
    graph_name = (dir_input_content[graph_index].split('.'))[0]
    print graph_name


    eg = EndorsementGraph('../inputs',graph_name)
    g = eg.buildEGraph('../outcomes')

    print 'File '+graph_name+' correctly loaded in directory ../outcomes'

'''----Main----'''
if __name__ == '__main__':
    
    
    functions = ['0-Greedy simulation','1-Global simulation','2-Local simulation','3-Plot a graph','4-Load a graph']
    function_pointers = [greedy_alg,global_alg,local_alg,plot,load_graph]
    
    for s in functions:
        print s
    
    index = int(raw_input("\nChoose one of these operations (type the correspondent index): \n"))
    
    if index < 0 or index >= len(functions):
        print 'Bad input'
        sys.exit(1)
        
    function_pointers[index]()
        
        

    