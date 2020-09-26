import networkx as nx



def insert_node_between(graph, pred, child, n):
    graph.remove_edge(pred,child)
    graph.add_edge(pred,"dummy" + str(n))
    graph.add_edge("dummy" + str(n), child)
    return "dummy" + str(n)

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
    ctr=0
    for node in node_list:
        succit = graph.successors(node)
        while(True):
            try:
                successor = next(succit)
                if(graph.nodes[node]["hierarchy_depth"]+1!=graph.nodes[successor]["hierarchy_depth"]):
                    dummy = insert_node_between(graph,node,successor,ctr)
                    graph.nodes[dummy]["hierarchy_depth"]=graph.nodes[node]["hierarchy_depth"]+1
                    ctr= ctr+1
                    node_list.append(dummy)
                else:
                    node_list.append(successor)   
            except:
                break
                    






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
    pass_2(graph, root_list)