import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import bipartite
import sys, os

if __name__ == '__main__':
    
    dir_output_graph_content = []
    dir_outcomes_content = []
    graph_index = -1
    
    print 'Available files: \n'
    
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
    
    