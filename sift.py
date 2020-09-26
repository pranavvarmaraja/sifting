import networkx as nx
from assign_layers import assign_layers
from resolve_cycles import resolve_cycles
import copy
from matplotlib import pyplot as plt

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
    if(graph.nodes[edge1[1]]["hierarchy_depth"]!=graph.nodes[edge2[1]]["hierarchy_depth"]):
        raise Exception("hierarchy_depths are not adjacent for layers being compared")
    else:
        if(graph.nodes[edge2[1]]["layer_x"]>graph.nodes[edge1[1]]["layer_x"] and 
        graph.nodes[edge2[0]]["layer_x"] < graph.nodes[edge1[0]]["layer_x"]):
            return True
        elif(graph.nodes[edge2[1]]["layer_x"]<graph.nodes[edge1[1]]["layer_x"] and 
        graph.nodes[edge2[0]]["layer_x"] > graph.nodes[edge1[0]]["layer_x"]) :    
            return True
        else:
            return False 

def c_uv(graph, node1, node2):
    edge_list1 = graph.out_edges([node1])
    edge_list2 = graph.out_edges([node2])
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
    node_list = copy.deepcopy(dictionary[depth])
    for node in dictionary[depth]:
        i = node_list.index(node)
        swap_node_layer_x(node, node_list[0])
        swap_list_values(i,0,node_list)
        i = 0
        curr_config = copy.deepcopy(node_list)
        min_crossings = total_crossings(graph,depth,dictionary)
        for j in range (1,len(node_list)):
            node2 = curr_config[j]
            cuv = c_uv(graph,node,node2)
            swap_node_layer_x(node,node2)
            swap_list_values(i,j,curr_config)
            i = j
            if min_crossings-cuv+c_uv(graph, node, node2) < min_crossings:
                min_crossings = min_crossings-cuv+c_uv(graph, node, node2)
                node_list = curr_config
    dictionary[depth] = node_list
        
        

    


def swap_node_layer_x(node1, node2):
    graph.nodes[node1]["layer_x"], graph.nodes[node2]["layer_x"] = graph.nodes[node2]["layer_x"], graph.nodes[node1]["layer_x"]

def swap_list_values(index1,index2,arr):
    arr[index1],arr[index2] = arr[index2],arr[index1]
    



def sift_graph(graph):
    resolve_cycles(graph)
    assign_layers(graph)
    dictionary = generate_node_dict(graph)
    assign_layer_x(graph, dictionary)
    for depth in dictionary.keys():
        sift_layer(graph,depth, dictionary)
    

def get_positions(graph):
    sift_graph(graph)
    dictionary = {}
    for node in graph.nodes:
        dictionary[node] = [graph.nodes[node]["hierarchy_depth"], graph.nodes[node]["layer_x"]]
    return dictionary

graph = nx.DiGraph()

graph.add_nodes_from(["A","B","C","D","E"])
graph.add_edges_from([("A","B"),("B","C"),("B","D"),("E","C"),("C","D")])
positions = get_positions(graph)
print(positions)

for node in graph.nodes:
    print(node + "; (layer_x: " + str(graph.nodes[node]["layer_x"]) + ", depth: " + str(graph.nodes[node]["hierarchy_depth"]) + ")")

# nx.draw(graph, with_labels=True, pos=positions)
# plt.savefig("test2.png")