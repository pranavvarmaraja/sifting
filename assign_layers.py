import networkx as nx



def insert_node_between(graph, pred, child, n):
    """ Inserts dummy nodes between two nodes such that pred->child becomes pred->dummy & dummy->child
        Parameters:
        graph: NetworkX Digraph to be modified
        pred: parent node (dummy is inserted after this node)
        child: child node (dummy is inserted before this node)
        n: dummy node # to be added
        
        Returns: id of dummy node added

    """
    graph.remove_edge(pred,child)
    graph.add_edge(pred,"dummy" + str(n))
    graph.add_edge("dummy" + str(n), child)
    return "dummy" + str(n)



def pass_1(graph, root_list, depth):
    """ Assigns initial hierarchy_depths to graph after cycles are removed
        Parameters:
        graph: graph to be hierarchized
        root_list: list of nodes to be set to a given depth
        depth (int): depth to be assigned to a given set of nodes
    """
    if(len(root_list)>0):
        child_list = set()
        for node in root_list:
            graph.nodes[node]['hierarchy_depth'] = depth
            child_list.update(graph.successors(node))
        pass_1(graph, child_list, depth+1)
    else:
        pass

def pass_2(graph):
    """ Moves nodes with indegree 0 to their correct depths using the locations of the children
        (root nodes should be at a depth one previous to the depth of their closest child)
        Parameters:
        graph (nx.Digraph): graph to be altered
    """
    node_list = []
    for node in graph.nodes:
        if graph.nodes[node]["hierarchy_depth"] == 0:
            try:
                successor_iterator = graph.successors(node)
                minimum_depth = graph.nodes[next(successor_iterator)]["hierarchy_depth"]
            except:
                pass
            while True:
                try:
                    successor = next(successor_iterator)
                    currdepth = graph.nodes[successor]["hierarchy_depth"]
                    if currdepth<minimum_depth:
                        minimum_depth = currdepth
                except:
                    break
            graph.nodes[node]["hierarchy_depth"] = minimum_depth-1
            node_list.append(node)
    return node_list
            


def pass_3(graph, node_list):
    """Inserts dummy nodes in appropriate locations to ensure that there are no edges spanning multiple depths

        Parameters:
        graph (nx.Digraph): graph to be altered
        node_list: list of root nodes (depth 0)

    """
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
    if type(graph)!=nx.DiGraph:
        raise Exception("graph is not a digraph!")
    root_list = []
    leaf_list = []
    nodes = graph.nodes()
    for node in nodes:
        if(graph.in_degree(node)==0):
            root_list.append(node)
        elif(graph.out_degree(node)==0):
            leaf_list.append(node)
    pass_1(graph, root_list, 0)
    pass_2(graph)
    pass_3(graph, root_list)