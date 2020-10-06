import networkx as nx



#usage resolve_cycles(graph G)
def resolve_cycles(graph):

    #initialize empty list of feedback arc set
    FAS = []
    #compute order of nodes which minimizes backwards edges
    arrangement = linear_arrangement(graph)
    #remove all backwards nodes and add to feedback arc set (equivalent to make graph acyclic)
    #because if backwards edges do not exist, no way for a cycle to exist where a node leads back
    # to any predecessor
    for i in range(len(arrangement)):
        for j in range(0,i):
            node1 = arrangement[i]
            node2 = arrangement[j]
            if(graph.has_edge(node1,node2)):

                FAS.append((node1,node2))
                
                graph.remove_edge(node1,node2)
    return FAS


    
#usage arrangement = linear_arrangement(graph)
def linear_arrangement(graph):


    # ensure that original graph remains unchanged
    g = graph.copy()

    # node list contains the list of all nodes in the graph
    node_list = list(graph.nodes)
    # sink list is a list of all nodes which have outdegree 0
    sink_list = []
    #source list is a list of all nodes which have indegree 0
    source_list = []

    #add appropriate nodes to sink list and source list initially
    for node in node_list:
        if(graph.out_degree(node)==0):
            sink_list.append(node)
        elif(graph.in_degree(node)==0):
            source_list.append(node)
    

    #sequence 1 and 2 are combined to return the linear arrangement of the graph
    sequence1 = []
    sequence2 = []

    #implementation of greedyFAS (university of victoria, 2016), see wiki references for more details
    while(graph.order()>0):

        
        while(len(sink_list)>0):
            sink = sink_list[0]
            sequence2.insert(0,sink)
            graph.remove_node(sink)
            node_list = list(graph.nodes)
            sink_list = []
            source_list = []
            for node in node_list:
                if(graph.out_degree(node)==0):
                    sink_list.append(node)
                elif(graph.in_degree(node)==0):
                    source_list.append(node)
      
        while(len(source_list)>0):
            source = source_list[0]
            sequence1.append(source)
            graph.remove_node(source)
            node_list = list(graph.nodes)
            sink_list = []
            source_list = []
            for node in node_list:
                if(graph.out_degree(node)==0):
                    sink_list.append(node)
                elif(graph.in_degree(node)==0):
                    source_list.append(node)
        
        if(graph.order()==0):
            break
        node_list = list(graph.nodes)
        max_node = node_list[0]
        max_sink_index = sink_index(graph,node_list[0])

        sink_list = []
        source_list = []
        for node in node_list:
            if(sink_index(graph,node)>max_sink_index):
                max_node = node
                max_sink_index = sink_index(graph,node)


        sequence1.append(max_node)
        graph.remove_node(max_node)


        node_list = list(graph.nodes)
        sink_list = []
        source_list = []
        for node in node_list:
                if(graph.out_degree(node)==0):
                    sink_list.append(node)
                elif(graph.in_degree(node)==0):
                    source_list.append(node)
        

        
    #sets the graph back to its original copy
    graph.update(g)
    #returns the optimal linear arrangement of the given directional graph
    return list(sequence1 + sequence2)
        


#usage x = sink_index(graph, node)
#returns sink index of graph according to GreedyFAS algorithm
def sink_index(graph, node):

    return graph.out_degree(node) - graph.in_degree(node)