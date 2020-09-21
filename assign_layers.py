import networkx as nx



def insert_node_between(graph, pred, child, n):
    graph.remove_edge(pred,child)
    graph.add_edge(pred,"dummy" + str(n))
    graph.add_edge("dummy" + str(n), child)

def pass_1(graph, root_list, depth):
    if(len(root_list)>0):
        child_list = set()
        for node in root_list:
            graph.nodes[node]['hierarchy_depth'] = depth
            child_list.update(graph.successors(node))
        pass_1(graph, child_list, depth+1)
    else:
        pass


def pass_2(graph, node_list):
    for node in node_list:
        for successor in 




def assign_layers(graph):
    root_list = []
    leaf_list = []
    nodes = graph.nodes()
    for node in nodes:
        if(graph.in_degree(node)==0):
            root_list.append(node)
        elif(graph.out_degree(node)==0):
            leaf_list.append(node)

    pass_1(graph, root_list, 0)
    pass_2(graph, leaf_list)
    


graph = nx.DiGraph()

graph.add_nodes_from(["A","B","C","D","E"], hierarchy_depth=0)
graph.add_edges_from([("A","B"),("B","C"),("B","D"),("E","C"),("C","D")])
assign_layers(graph)
# for node in graph.nodes():
#     print(node + ":" + str(graph.nodes[node]["hierarchy_depth"]))
# print(graph.edges())