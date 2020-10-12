import sift
import networkx as nx
from matplotlib import pyplot as plt



graph = nx.DiGraph()
edges = [(1, 2), (1, 6), (2, 3), (2, 4), (2, 6),  
         (3, 4), (3, 5), (4, 8), (4, 9), (6, 7), (7,9), (5,2), (1,10)] 
graph.add_edges_from(edges)

# graph = nx.gnm_random_graph(50, 100, directed=True)

runtime = sift.draw_hierarchy(graph=graph, filename="test1.png")
print(runtime)

# nx.draw(graph, with_labels=True, pos=nx.drawing.layout.circular_layout(graph,scale=1))
# plt.savefig("test2.png")
# graph.clear()