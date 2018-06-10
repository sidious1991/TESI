from buildRetweetGraph.endorsementgraph import EndorsementGraph
#import matplotlib.pyplot as plt
import sys, os

if __name__ == '__main__':

    dir_input_content = []
    graph_index = -1

    print 'Available files: \n'

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
