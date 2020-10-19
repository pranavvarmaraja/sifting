import networkx as nx
from assign_layers import assign_layers
from resolve_cycles import resolve_cycles
from copy import deepcopy

def generate_node_dict(graph):
    dictionary = {}
    for node in graph.nodes:
        try:
            dictionary[graph.nodes[node]["hierarchy_depth"]].append(node)
        except:
            dictionary[graph.nodes[node]["hierarchy_depth"]] = [node]
    for key in dictionary.keys():
        sort_descending_in_degree(graph,dictionary[key])
    return dictionary

def assign_layer_x(graph, dictionary):
    for key in dictionary.keys():
        node_list = dictionary[key]
        for ele in enumerate(node_list):
            graph.nodes[ele[1]]["layer_x"] = ele[0]

def two_edges_cross(graph, edge1, edge2):
  
    if(graph.nodes[edge2[1]]["layer_x"]>graph.nodes[edge1[1]]["layer_x"] and 
    graph.nodes[edge2[0]]["layer_x"] < graph.nodes[edge1[0]]["layer_x"]):
        return True
    elif(graph.nodes[edge2[1]]["layer_x"]<graph.nodes[edge1[1]]["layer_x"] and 
    graph.nodes[edge2[0]]["layer_x"] > graph.nodes[edge1[0]]["layer_x"]) :    
        return True
    else:
        return False 

def c_uv(graph, node1, node2):
    edge_list1 = graph.in_edges([node1])
    edge_list2 = graph.in_edges([node2])
    count = 0
    for edge1 in edge_list1:
        for edge2 in edge_list2:
            if(two_edges_cross(graph,edge1,edge2)):
                count=count+1
    return count

def total_crossings(graph, depth, dictionary):
    edge_list = []
    count = 0
    for node in dictionary[depth]:
        edge_list = edge_list + list(graph.out_edges([node]))
    for edge1 in edge_list:
        edge_list.remove(edge1)
        for edge2 in edge_list:
            if(two_edges_cross(graph,edge1,edge2)):
                count = count+1
    return count

def sort_in_degree(graph,node_list): 
    if len(node_list) >1: 
        mid = len(node_list)//2  
        L = node_list[:mid]  
        R = node_list[mid:] 
  
        sort_in_degree(graph,L) 
        sort_in_degree(graph,R)  
  
        i = j = k = 0
    
        while i < len(L) and j < len(R): 
            if graph.in_degree(L[i]) < graph.in_degree(R[j]): 
                node_list[k] = L[i] 
                i+= 1
            else: 
                node_list[k] = R[j] 
                j+= 1
            k+= 1
          
        
        while i < len(L): 
            node_list[k] = L[i] 
            i+= 1
            k+= 1
          
        while j < len(R): 
            node_list[k] = R[j] 
            j+= 1
            k+= 1

def sort_descending_in_degree(graph,node_list):
    sort_in_degree(graph,node_list)
    node_list.reverse()
    

def sift_layer(graph,depth, dictionary):
    node_list = deepcopy(dictionary[depth])
    for node in dictionary[depth]:
        i = node_list.index(node)
        swap_node_layer_x(node, node_list[0], graph)
        swap_list_values(i,0,node_list)
        i = 0
        curr_config = deepcopy(node_list)
        min_crossings = total_crossings(graph,depth,dictionary)
        for j in range (1,len(node_list)):
            node2 = curr_config[j]
            cuv = c_uv(graph,node,node2)
            swap_node_layer_x(node,node2, graph)
            swap_list_values(i,j,curr_config)
            i = j
            if min_crossings-cuv+c_uv(graph, node, node2) < min_crossings:
                min_crossings = min_crossings-cuv+c_uv(graph, node, node2)
                node_list = curr_config
    dictionary[depth] = node_list
        
        

    


def swap_node_layer_x(node1, node2, graph):
    graph.nodes[node1]["layer_x"], graph.nodes[node2]["layer_x"] = graph.nodes[node2]["layer_x"], graph.nodes[node1]["layer_x"]

    return graph

def swap_list_values(index1,index2,arr):
    arr[index1],arr[index2] = arr[index2],arr[index1]
    
    

# fix coordinates of nodes after dummy removal
def remove_dummies(graph, dictionary):
    dummy_list = []
    for node in graph.nodes:
        if "dummy" in str(node):
            dummy_list.append(node)
            succit = graph.successors(node)
            predit = graph.predecessors(node)
            pred = next(predit)
            succ = next(succit)
            graph.remove_edge(pred,node)
            graph.remove_edge(node,succ)
            graph.add_edge(pred,succ)
    for node in dummy_list:
        graph.remove_node(node)
    for depth in dictionary:
        dictionary[depth][:] = [node for node in dictionary[depth] if not("dummy" in str(node))]
            
            
        
def update_dictionary(graph,dictionary):
    for depth in dictionary:
        sort_layer_x(graph,dictionary[depth])
        for i in range(len(dictionary[depth])):
            graph.nodes[dictionary[depth][i]]["layer_x"] = i
            graph.nodes[dictionary[depth][i]]["hierarchy_depth"] = depth


def sort_layer_x(graph,node_list): 
    if len(node_list) >1: 
        mid = len(node_list)//2  
        L = node_list[:mid]  
        R = node_list[mid:] 
  
        sort_layer_x(graph,L) 
        sort_layer_x(graph,R)  
  
        i = j = k = 0
    
        while i < len(L) and j < len(R): 
            if graph.nodes[L[i]]["layer_x"] < graph.nodes[R[j]]["layer_x"]: 
                node_list[k] = L[i] 
                i+= 1
            else: 
                node_list[k] = R[j] 
                j+= 1
            k+= 1
          
        
        while i < len(L): 
            node_list[k] = L[i] 
            i+= 1
            k+= 1
          
        while j < len(R): 
            node_list[k] = R[j] 
            j+= 1
            k+= 1


def sift_graph(graph):
    FAS = resolve_cycles(graph)
    assign_layers(graph)
    dictionary = generate_node_dict(graph)
    assign_layer_x(graph, dictionary)
    for depth in dictionary.keys():
        sift_layer(graph,depth, dictionary)
    remove_dummies(graph, dictionary)
    update_dictionary(graph,dictionary)
    return dictionary, FAS

def get_hierarchy_positions(graph):
    bfs_dict, FAS = sift_graph(graph)
    graph.add_edges_from(FAS)
    dictionary = {}
    for depth in bfs_dict:
        layer = bfs_dict[depth]
        if depth%2==0:
            for i in range(len(layer)):
                node = layer[i]
                dictionary[node] = (float(graph.nodes[node]["hierarchy_depth"]), float(2*i))
        else:
            for i in range(len(layer)):
                node = layer[i]
                dictionary[node] = (float(graph.nodes[node]["hierarchy_depth"]), float(2*i+1))
    for node in dictionary:
        dictionary[node] = (dictionary[node][0], dictionary[node][1])

    return dictionary, bfs_dict




#draw function and output to png file
def draw_hierarchy(graph, filename, labels=True, scale=1):
    from matplotlib import pyplot as plt
    positions = get_hierarchy_positions(graph)[0]

    nx.draw(graph, pos=positions, with_labels=labels)
    plt.savefig(filename)
    graph.clear()

# example usage on example graph

# graph = nx.DiGraph()
# edges = [(1, 2), (1, 6), (2, 3), (2, 4), (2, 6),  
#          (3, 4), (3, 5), (4, 8), (4, 9), (6, 7), (7,9), (5,2), (1,10)] 
# graph.add_edges_from(edges)

# draw_hierarchy(graph=graph,labels=True, filename="test3.png")
