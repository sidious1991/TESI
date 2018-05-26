import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import bipartite

if __name__ == '__main__':
    
    g_original = nx.read_gpickle('../outcomes/retweet_graph_indiana.pickle')#graph before adding recommended edges
    g = nx.read_gpickle('../output_graph/retweet_graph_indiana_in_deg.pickle')#graph after adding recommended edges
    
    edges = g.edges()
    
    node_list = []
    nodes_info = {}#{node:(in_deg,out_deg,ratio),...}
    bipartite_graph = nx.DiGraph()#for coloring
    
    for u,v in edges:
        if g[u][v]['color'] == 'red':
            
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
    
    