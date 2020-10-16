from sift import get_hierarchy_positions
from svg import draw_svg

import networkx as nx
from networkx.drawing.nx_agraph import read_dot


def genenerate_pygraph_svg_and_dot(graph_name, graph=nx.DiGraph()):

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Get a Networkx graph from a dot file
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if len(list(graph.nodes(data=False))) == 0:
        new_graph = read_dot("./graphs/" + graph_name + ".dot")
    else:
        new_graph = graph

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Convert the Networkx graph to a Pygraphviz Agraph:
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    new_Agraph = nx.nx_agraph.to_agraph(new_graph)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Generate the SVG
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    svg_file_name = "./graphs/" + graph_name + ".svg"
    svg_data = new_Agraph.draw(path=svg_file_name, format='svg', prog='dot')

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Generate the layout and capture it in the Agraph
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    new_Agraph.layout(prog='dot')

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Save the graph (Pygraphviz Agraph) with position set to node attributes
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    agraph_file_name =  "./graphs/" + graph_name + "AGRAPH.dot"
    new_Agraph.write(agraph_file_name)


def test_sifting():

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Get a Networkx graph from a dot file
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    new_graph = read_dot("./graphs/subgraphs.dot")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Generates the positions for the provided Networkx graph
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # 1) Using Pygraph layout algo calling Graphviz dot
    # pos = nx.nx_agraph.graphviz_layout(new_graph, prog='dot')
    # print(pos)

    # 2) Usinng the positions from thew Sift algo:
    pos = get_hierarchy_positions(new_graph)
    print(pos[0])

    # pos = {"Serverless:Functions": (3.0, 1.0), "Serverless:DynamoDB": (4.0, 0.0), "Parameters": (4.0, 2.0), "Logs": (0.0, 0.0), "Outputs": (0.0, 2.0), "Pseudo Parameters": (1.0, 1.0), "API Gateway:Rest Api": (1.0, 3.0), "API Gateway:APIs": (2.0, 0.0)}

    # Scale the position of the nodes:
    scale=200
    pos = nx.rescale_layout_dict(pos=pos[0], scale=scale)
    print("After rescale of {}".format(scale))
    print(pos)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -



def test_svg():


    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Get a Networkx graph from a dot file
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # new_graph = nx.MultiDiGraph()

    test_example = 2

    # Example #1:
    # -----------
    if test_example == 1:

        my_graph = read_dot("./graphs/subgraphs.dot")
        # my_graph = read_dot("./graphs/subgraph_hierarchy.dot")

        # # 1) Positions provided by Sifter
        # pos = get_hierarchy_positions(my_graph)
        # positions = pos[0]
        # print(positions)
        # # Rendered positions:
        # # {'Serverless:Functions': (3.0, 1.0), 'Serverless:DynamoDB': (4.0, 0.0), 'Parameters': (4.0, 2.0), 'Logs': (0.0, 0.0), 'Outputs': (0.0, 2.0), 'Pseudo Parameters': (1.0, 1.0), 'API Gateway:Rest Api': (1.0, 3.0), 'API Gateway:APIs': (2.0, 0.0)}

        # 2) Expected layout (example 1: cf template):
        # positions = {
        #     'Pseudo Parameters': (1.0, 3.0),
        #     'Logs': (2.0, 3.0),
        #     'Parameters': (4.0, 3.0),
        #     'Outputs': (0.0, 2.0),
        #     'API Gateway:Rest Api': (1.0, 1.0),
        #     'API Gateway:APIs': (2.0, 1.0),
        #     'Serverless:Functions': (3.0, 1.0),
        #     'Serverless:DynamoDB': (4.0, 1.0),
        # }


    # Example #2:
    # -----------
    if test_example == 2:

        # Build graph from DOT representation:
        # my_graph = read_dot("./graphs/graph_test.dot")

        # Build graph manually:
        my_graph = nx.DiGraph()
        edges = [("Node1", "Node2"), ("Node2", "Node3"), ("Node3", "Node4"), ("Node4", "Node5"), ("Node4", "Node6"),
        ("Node1", "Node7"), ("Node8", "Node4"), ("Node8", "Node6")]
        my_graph.add_edges_from(edges)

        # 1) Positions provided by Sifter
        pos = get_hierarchy_positions(my_graph)
        positions = pos[0]
        print(positions)
        # Rendered positions:
        {'Node8': (0.0, 0.0), 'Node1': (0.0, 2.0), 'Node7': (1.0, 1.0), 'Node2': (1.0, 3.0), 'Node3': (2.0, 0.0), 'Node4': (3.0, 1.0), 'Node5': (4.0, 0.0), 'Node6': (4.0, 2.0)}

        # # 2) Expected layout:
        # positions = {
        #     # 'Node1': (0.0, 2.0),
        #     'Node1': (0.0, 1.0),
        #     # 'Node2': (1.0, 3.0),
        #     'Node2': (1.0, 0.0),
        #     'Node3': (2.0, 0.0),
        #     'Node4': (3.0, 1.0),
        #     'Node5': (4.0, 0.0),
        #     'Node6': (4.0, 2.0),
        #     # 'Node7': (1.0, 1.0),
        #     'Node7': (1.0, 2.0),
        #     # 'Node8': (0.0, 0.0),
        #     'Node8': (2.0, 2.0),
        # }

    for node_id in list(my_graph.nodes(data=False)):
        if node_id in positions.keys():
            my_graph.nodes[node_id]["pos"]='{},{}'.format(positions[node_id][0],positions[node_id][1])
        else:
            print("Missing position for this node: {}".format(node_id))

    # Save created SVG to this file
    svg_file_name = "./graphs/test_graph.svg"

    # Draw and save the graph into an SVG image:
    svg_document = draw_svg(my_graph, svg_file_name)

    # print()
    # print('-'*100)
    # print(svg_document)
    # print('-'*100)
    # print()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def test_manual_graph():

    # Base graph:
    my_graph = nx.DiGraph()
    edges = [(1, 2), (2, 3), (3, 4), (4, 5), (4, 6), (1, 7), (8, 4), (8, 6)]
    my_graph.add_edges_from(edges)

    # 1) Generate SVG without setting the position
    genenerate_pygraph_svg_and_dot("corner_case1", my_graph)

    # 2) Generate with the positions provided by Sifter
    pos = get_hierarchy_positions(my_graph)
    positions = pos[0]
    print(positions)

    for node_id in list(my_graph.nodes(data=False)):
        if node_id in positions.keys():
            my_graph.nodes[node_id]["pos"]='{},{}'.format(positions[node_id][0],positions[node_id][1])
        else:
            print("Missing position for this node: {}".format(node_id))

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Convert the Networkx graph to a Pygraphviz Agraph to be able to draw an SVG
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    new_Agraph = nx.nx_agraph.to_agraph(my_graph)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Generate the SVG
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    svg_file_name = "./graphs/" + "corner_case2" + ".svg"
    # Uses the provided positions to generate the SVG if the parameter is not set: prog='dot'
    svg_data = new_Agraph.draw(path=svg_file_name, format='svg', prog='neato', args='-n2')



# ==================================================================
# The following code is not run if this module is imported.
# https://docs.python.org/3.7/tutorial/modules.html

if __name__ == "__main__":

    # test_sifting()

    test_svg()

    # genenerate_pygraph_svg_and_dot("graph_test")

    # test_manual_graph()
