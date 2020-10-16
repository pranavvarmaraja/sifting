#!/usr/bin/python3.7

__version__ = '0.1.0-10-14-2020'
__author__ = 'Nicolas Philip <nphilip@pomelocloud.com>'
__summary__ = 'Generating SVG images of directed acyclic NetworkX graphs'


# References:
#   SVG specifications  : https://developer.mozilla.org/en-US/docs/Web/SVG
#   Networkx            : 

# External dependencies:
import networkx as nx
import re
from operator import itemgetter

# ==================================
# Global settings
# ==================================
TAB = '\t'
GRAPH_MARGIN = 4
LABEL_MARGIN = (4,4) #4
# Set scale on both axes (X,Y):
# GRAPH_SCALE  = (160,60)
GRAPH_SCALE  = (200,60)
NODE_SEP = 100

SVG_WIDTH = 1650.00
SVG_HEIGHT = 400.00

# SVG_BACKGROUND_COLOR = "#97a5c0"
SVG_BACKGROUND_COLOR = "white"


SUPPORTED_NODE_SHAPES = ["ellipse", "box"]
NODE_SHAPE = SUPPORTED_NODE_SHAPES[0]



# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# CLASSES
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

class SvgLabel:
    def __init__(self, label='', pos=(0.0,0.0)):
        label = str(label)
        self.label = label
        self.pos   = pos
        # RFE: calculate dimensions based on font type and size
        label_height = 10
        uc_count = len(re.findall(r'[A-Z]', label))      # uppercase characters
        di_count = len(re.findall(r'[0-9]', label))      # digit characters
        na_count = len(re.findall(r'[\W+]', label))      # non alphannumerical
        ws_count = label.count(' ')                      # whitespaces ' '
        lc_count = len(label)-uc_count-na_count-ws_count-di_count# the rest
        # uc_count = 0
        # lc_count = 0
        # na_count = 0
        # ws_count = 0
        # di_count = 0
        label_width = sum([
            uc_count*11.6,
            lc_count*7.8,
            na_count*3.2,
            ws_count*12,
            di_count*12.2,
            ])
        self.dim = (label_width, label_height)

        # self.dim   = (10+len(labe))*8.2, label_height)


class SvgShape:
    def __init__(self, pos=(0.0,0.0), dim=(0.0,0.0)):
        self.pos   = pos
        self.dim   = dim
        # 4 connectors positions:
        self.con   = {"n":(0.0,0.0), "s":(0.0,0.0), "w":(0.0,0.0), "e":(0.0,0.0)}

class SvgNode:
    def __init__(self, nodeid=0,label='',pos=(0.0,0.0), tooltip=''):
        self.id    = nodeid
        self.label = label
        self.pos   = pos
        self.tooltip = tooltip

        # Input validation:
        # if isinstance(self.id,int) != true:

class SvgEdge:
    def __init__(self, sNodeId=0, eNodeId=0, edgeid='', tooltip='', sPos=(0.0), ePos=(0,0)):
        self.id = edgeid
        self.s  = sNodeId
        self.e  = eNodeId
        self.tt = tooltip
        self.sp = sPos
        self.ep = ePos


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# FUNCTIONS:
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# SVG specs
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def get_main_doc():

    s_xml = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
    s_std = '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
    s_author = '<!-- SVG generated by Graph Sifter -->'

    return '\n'.join([s_xml, s_std, s_author])

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Main <svg />
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def get_main_svg(width=100, height=100):

    s_xmlns="http://www.w3.org/2000/svg"              # xmlns
    s_xmlns_xlink="http://www.w3.org/1999/xlink"      # xmlns:xlink
    s_viewBox = "0.00 0.00 {} {}".format(width, height)
    s_svg = '<svg width="{}" height="{}" viewBox="{}" xmlns="{}" xmlns:xlink="{}">'.format(width, height,s_viewBox, s_xmlns, s_xmlns_xlink)
    e_svg = '</svg>'

    return s_svg, e_svg

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Main graph: <g />
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# transform: moves the object by x and y
# https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform

def get_main_graph(height=100):

    # <g id="graph0" class="graph" transform="scale(1 1) rotate(0) translate(4 328)">

    s_id        = "my_graph_0"
    s_class     = "graph"
    s_trans_factor = GRAPH_MARGIN
    s_transform = "scale(1 1) rotate(0) translate({} {})".format(s_trans_factor, round(height)-s_trans_factor)

    s_graph = '<g id="{}" class="{}" transform="{}">'.format(s_id, s_class, s_transform)
    e_graph = '</g>'

    return s_graph, e_graph

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# SVG background
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def get_svg_background(width=100, height=100):

    # <polygon fill="white" stroke="transparent" points="-4,4 -4,-328 443.85,-328 443.85,4 -4,4" />

    # bgFill = "#97a5c0"
    bgFill = SVG_BACKGROUND_COLOR
    bgStrocke = "transparent"
    bgOff = GRAPH_MARGIN
    bgPoints = "{},{} {},{} {},{} {},{} {},{}".format(
        float(-bgOff), float(bgOff),
        float(-bgOff), float(bgOff-height),
        float(width-bgOff), float(bgOff-height),
        float(width-bgOff), float(bgOff),
        float(-bgOff), float(bgOff),
    )

    return '<polygon fill="{}" stroke="{}" points="{}" />'.format(bgFill, bgStrocke, bgPoints)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Generate SVG string for Nodes: <g />
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    # node1 = SvgNode(
    #             "node1",
    #             "node1",
    #             (100.0, 200.0),
    #             "SVG::NODES::Node",
    #         )

# Rectangle drawn around the label, with a specified margin:

def get_shape_rectangle(svgLabel = SvgLabel(), direction='LR'):
    """Returns an instance of the `SvgShape` class with the starting point (x,y)
    and dimensions (width,height) of a rectangle.
    """

    # Mapping to external parameters:
    label_width  = svgLabel.dim[0]
    label_height = svgLabel.dim[1]

    # Width and height == Label dimensions+ Margin
    shape_width  = (LABEL_MARGIN[0]*2) + label_width
    shape_height = (LABEL_MARGIN[1]*4) + label_height

    # Position of the rectangle where x,y == top, left corner
    if direction == 'LR':
        # LR then textJustify = 'start'
        shape_xPos   = svgLabel.pos[0] - LABEL_MARGIN[0]
        shape_yPos   = svgLabel.pos[1] - ((label_height + shape_height) / 2)
    else:
        # TB then textJustify = 'middle'
        shape_xPos   = svgLabel.pos[0] - (shape_width  / 2)
        shape_yPos   = svgLabel.pos[1] - (shape_height / 2) - (label_height / 2)

    svgShape = SvgShape(
        (shape_xPos, shape_yPos),
        (shape_width, shape_height)
        )

    svgShape.con = {
        "e": (svgShape.pos[0] + svgShape.dim[0], svgShape.pos[1] + (svgShape.dim[1] / 2)),
        "w": (svgShape.pos[0]                  , svgShape.pos[1] + (svgShape.dim[1] / 2)),
        # Need to test n and s:
        "n": (svgShape.pos[0] + svgShape.dim[0] / 2, svgShape.pos[1]),
        "s": (svgShape.pos[0] + svgShape.dim[0] / 2, svgShape.pos[1] + svgShape.dim[1]),
    }

    return svgShape

def get_shape_ellipse(svgLabel = SvgLabel(), direction='LR'):
    """Returns an instance of the `SvgShape` class with the starting point (x,y)
    and dimensions (width,height) of an ellipse.
    """

    # Mapping to external parameters:
    label_width  = svgLabel.dim[0]
    label_height = svgLabel.dim[1]

    # Width and height == Label dimensions+ Margin
    shape_width  = (LABEL_MARGIN[0]*6) + (label_width  / 2)
    shape_height = (LABEL_MARGIN[1]*6) + (label_height / 2)

    # Position of the rectangle where x,y == top, left corner
    if direction == 'LR':
        # LR then textJustify = 'start'
        shape_xPos   = svgLabel.pos[0] + (label_width / 2)
        shape_yPos   = svgLabel.pos[1] - (label_height / 2)
        # shape_xPos   = svgLabel.pos[0]
        # shape_yPos   = svgLabel.pos[1]
    else:
        # TB then textJustify = 'middle'
        shape_xPos   = svgLabel.pos[0]
        shape_yPos   = svgLabel.pos[1]

    svgShape = SvgShape(
        (shape_xPos, shape_yPos),
        (shape_width, shape_height)
        )

    svgShape.con = {
        "e": (svgShape.pos[0] + shape_width, svgShape.pos[1]),
        "w": (svgShape.pos[0] - shape_width, svgShape.pos[1]),
        # Need to test n and s:
        "n": (svgShape.pos[0] + svgShape.dim[0] / 2, svgShape.pos[1]),
        "s": (svgShape.pos[0] + svgShape.dim[0] / 2, svgShape.pos[1] + svgShape.dim[1]),
    }

    return svgShape

def get_svg_node(node):

    # <g id="node2" class="node">
    #     <title>Serverless:DynamoDB</title>
    #     <ellipse fill="none" stroke="black" cx="104.17" cy="-18" rx="104.34" ry="18" />
    #     <text text-anchor="middle" x="104.17" y="-13.8" font-family="Times,serif"
    #         font-size="14.00">Serverless:DynamoDB (5)</text>
    # </g>

    # Mapping with external parameters:
    nodeId         = node.id
    nodeTooltip    = node.tooltip
    nodeLabel      = node.label

    labelPos = node.pos
    # # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # # Adjusting label position and dimension to scale (and direction?)
    # # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # labelPos = adjusted_position(node.pos, GRAPH_SCALE)

    # - - - - - - - - - - - - - - - - - - - - - - - - -
    # CSS for node
    # - - - - - - - - - - - - - - - - - - - - - - - - -
    cssClassNode  = "node"
    textJustify   = "start" # start, middle, end - https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/text-anchor
    fontFamily    = "Helvetica,serif"
    fontSize      = '{}'.format(float(16))

    # - - - - - - - - - - - - - - - - - - - - - - - - -
    # Rendering the SVG components for the node:
    # - - - - - - - - - - - - - - - - - - - - - - - - -
    s_node  = '<g id="{}" class="{}">'.format(nodeId, cssClassNode)
    s_title = '<title>{}</title>'.format(nodeTooltip)
    s_text  = '<text text-anchor="{}" x="{:.1f}" y="{:.1f}" font-family="{}" font-size="{:.2f}">{}</text>'.format(textJustify, float(labelPos[0]), float(labelPos[1]), fontFamily, float(fontSize), nodeLabel)
    e_node  = '</g>'

    # - - - - - - - - - - - - - - - - - - - - - - - - -
    # Shape properties:
    # - - - - - - - - - - - - - - - - - - - - - - - - -
    shapeStroke  = "black"     # default: black
    shapeFill    = "white"     # default: none
    shapeShape   = NODE_SHAPE   # Supported: box, ellipse - https://graphviz.org/doc/info/shapes.html

    # The shape position/dimensions are based on the label position/dimensions:
    if shapeShape == 'box':
        svgShape = get_shape_rectangle(SvgLabel(nodeLabel, labelPos))
        s_shape = '<rect x="{:.1f}" y="{:.1f}" width="{:.1f}" height="{:.1f}" fill="{}" stroke="{}"/>'.format(svgShape.pos[0], svgShape.pos[1], svgShape.dim[0], svgShape.dim[1], shapeFill, shapeStroke)
    elif shapeShape == 'ellipse':
        # <ellipse fill="none" stroke="black" cx="101.21" cy="-306" rx="46.41" ry="18"/>
        svgShape = get_shape_ellipse(SvgLabel(nodeLabel, labelPos))
        s_shape = '<ellipse cx="{:.1f}" cy="{:.1f}" rx="{:.1f}" ry="{:.1f}" fill="{}" stroke="{}" />'.format(svgShape.pos[0], svgShape.pos[1], svgShape.dim[0], svgShape.dim[1], shapeFill, shapeStroke)



    # - - - - - - - - - - - - - - - - - - - - - - - - -
    # Render and return the completely formed SVG string
    # to represent the node in SVG format
    # - - - - - - - - - - - - - - - - - - - - - - - - -
    return '\n'.join([
            (TAB*2)+s_node,
            (TAB*3)+s_title,
            (TAB*3)+s_shape,
            (TAB*3)+s_text,
            (TAB*2)+e_node
            ])


def get_svg_nodes(graph):

    s_nodes = ''

    for nodeId, nodeAttr in graph.nodes(data=True):

        pos = nodeAttr['pos'].split(',') if 'pos' in nodeAttr.keys() else ['0','0']
        nodeType = nodeAttr['type'] if 'type' in nodeAttr.keys() else nodeId
        nodeLabel = nodeAttr['label'] if 'label' in nodeAttr.keys() else nodeId

        s_node = get_svg_node(
            SvgNode(
                    nodeId,
                    nodeLabel,
                    (float(pos[0]), float(pos[1])),
                    nodeType,
                )
        )
        s_nodes += s_node + '\n'

    return s_nodes

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Generate SVG string for Edges: <g />
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def get_svg_edge(edge=SvgEdge()):

    edgeId = edge.id
    edgeTooltip = edge.tt

    # CSS for node
    cssClassEdge  = 'edge'
    edgeFill      = 'none'
    edgeStroke    = 'black'

    s_edge  = '<g id="{}" class="{}">'.format(edgeId, cssClassEdge)
    s_title = '<title>{}</title>'.format(edgeTooltip)
    e_edge  = '</g>'

    s_xPos, s_yPos = edge.sp[0], edge.sp[1]
    e_xPos, e_yPos = edge.ep[0], edge.ep[1]

    d_path = "M{:.1f},{:.1f} L{:.1f},{:.1f}".format(s_xPos, s_yPos, e_xPos, e_yPos)
    # print ('Creating edge path: {} [d="{}"]'.format(edge.tt, d_path))

    s_shape = '<path fill="{}" stroke="{}" d="{}" />'.format(edgeFill, edgeStroke, d_path)
    # print("Edge shape: {}".format(s_shape))

    return '\n'.join([
            (TAB*2)+s_edge,
            (TAB*3)+s_title,
            (TAB*3)+s_shape,
            (TAB*2)+e_edge
            ])


def get_connector_position(nodeId, graph, e_key, type='start', direction='LR'):
    """ Returns the position of the connnector on the node.
        - Must specify the connnector type: 'start' or 'end' of the edge
        - Must specify the direction: LR, RL, TB or BT (only LR supported for now)
    """

    if nodeId not in list(graph.nodes(data=False)):
        print("Unable to find node '{}' connected to edge {}".format(nodeId, e_key))
        return False

    if 'pos' not in graph.nodes[nodeId].keys():
        print("No position attribute found for node '{}' connected to edge {}".format(nodeId, e_key))
        return False

    if 'label' not in graph.nodes[nodeId].keys():
        print("Using node_id as label for node '{}' connected to edge {}".format(nodeId, e_key))
        nodeLabel = nodeId
    else:
        nodeLabel = graph.nodes[nodeId]['label']

    if 'shape' not in graph.nodes[nodeId].keys():
        # print("No shape attribute found for node '{}' connected to edge {} - Using default: 'box'".format(nodeId, e_key))
        shapeShape = NODE_SHAPE
    else:
        shapeShape = graph.nodes[nodeId]['shape']


    pos = graph.nodes[nodeId]['pos'].split(',')
    labelPos = (float(pos[0]), float(pos[1]))
    # # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # # Adjusting label position and dimension to scale (and direction?)
    # # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # labelPos = adjusted_position(labelPos, GRAPH_SCALE)

    if shapeShape == 'box':
        svgShape = get_shape_rectangle(SvgLabel(nodeLabel, labelPos))
    elif shapeShape == 'ellipse':
        svgShape = get_shape_ellipse(SvgLabel(nodeLabel, labelPos))

    connector = ''
    if direction == 'LR':
            connector = 'e' if type == 'start' else 'w'

    x = svgShape.con[connector][0]
    y = svgShape.con[connector][1]

    return (x,y)


def get_svg_edges(graph):

    s_edges = ''
    edge_count = 1

    # for u, v, keys, edgedata in my_graph.edges(data=True, keys=True):
    for u, v, edgedata in graph.edges(data=True):
        # Auto-generating keys and tooltip for Digraph() graphs
        # Will need to check if defined as attributes with MultiDigraph graphs
        e_key = 'e_key' + str(edge_count)
        edgeTooltip = str(u) + ' -> ' + str(v)
        # print("Create edge: {}".format(edgeTooltip))

        sPos = get_connector_position(u, graph, e_key, type='start')
        if sPos == False: continue
        ePos = get_connector_position(v, graph, e_key, type='end')
        if ePos == False: continue

        # Getting the string to represent this edge in SVG format:
        s_edge = get_svg_edge(
            SvgEdge(
                    str(u),
                    str(v),
                    e_key,
                    edgeTooltip,
                    sPos,
                    ePos,
                )
        )
        # Capturing the string to represent all edges in SVG format:
        s_edges += s_edge + '\n'
        edge_count += 1

    # Returning the string to represent all edges in SVG format:
    return s_edges



# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# Shifting node position to meet the expected minimum node separation:
# horizontally if direction == [LR | RL]
# vertically if direction == [TB | BT]  -- Not implemented
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

class SvgGraph:

    def __init__(self, graph = None):
        self.graph = nx.DiGraph()
        self.root_nodes = []
        self.leaf_nodes = []
        self.dir = 'LR'                # LR/RL, or TB/BT
        self.sep = 0
        self.scale = GRAPH_SCALE

        if self.graph != None:
            self.graph = graph

    def _scale_positions(self):
        """ Calculating absolute position of all nodes, factoring scale (RFE: factor direction)
        
        Note: The node is skipped, if it does not have the attribute 'pos' present.
        """

        for g_node in self.graph.nodes(data=False):
            if 'pos' not in self.graph.nodes[g_node].keys():
                continue
            pos = self.graph.nodes[g_node]['pos'].split(',')
            nodePos = (float(pos[0]), float(pos[1]))
            if isinstance(nodePos, tuple) == False:
                continue
            # Adjusted position:
            adj_xPos =  70+nodePos[0]*self.scale[0]
            adj_yPos =  -70-nodePos[1]*self.scale[1]

            self.graph.nodes[g_node]['pos'] = "{},{}".format(adj_xPos, adj_yPos)

    def _get_root_nodes(self):
        """ Returns list of root nodes (node ids) of a Directed acyclic graph (nodes w/o predecessors)
        """

        node_list = []

        if self.graph == None or len(self.graph) == 0:
            #  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +
            app_msg = "The provided graph is empty and would need to be initialized to look for its root nodes!"
            print(app_msg)
            #  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +
            return False
        
        for g_node in self.graph:

            # PREDECESSORS extracted here:
            node_pred = list(self.graph.predecessors(g_node))
            pred_count = len(node_pred)

            if pred_count == 0:
                #  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +
                # app_msg = "Node with no predecessors found: '{}'".format(g_node)
                # print(app_msg)
                #  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +
                if 'pos' not in self.graph.nodes[g_node].keys():
                    pos = ['0','0']
                else:
                    pos = self.graph.nodes[g_node]['pos'].split(',')
                nodePos = (float(pos[0]), float(pos[1]))
                node_list.append({"id": g_node, "x": nodePos[0], "y": nodePos[1]})
            else:
                #  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +
                # app_msg = "Node's '{}' predecessors ({}): {}".format(g_node, pred_count, node_pred)
                # print(app_msg)
                #  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +
                pass

        # Sorted by direction:
        # LR/RL -> Horizontal -> sort by "x"
        # TB/BT -> Vertical -> sort by "y"

        if self.dir in ['LR','RL']:
            node_list = sorted(node_list, key=itemgetter('x'),reverse=False)
        else:
            node_list = sorted(node_list, key=itemgetter('y'),reverse=False)

        for r_node in node_list:
            self.root_nodes.append(r_node['id'])

        # print ("Root nodes: {}".format(self.root_nodes))

        # ------------------------------------------------------------------------------------
        # METHOD:   Find leaf nodes (subgraphs) of the subgraph graph, w/o successors and
        #             with the same lowest depth.
        # ------------------------------------------------------------------------------------

    def _get_leaf_nodes(self):
        """ Returns list of leaf nodes (node ids) of a Directed acyclic graph (nodes w/o successors)
        """

        if self.graph == None or len(self.graph) == 0:
            #  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +
            app_msg = "The provided graph is empty and would need to be initialized to look for its leaf nodes!"
            print(app_msg)
            return False
            #  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +

        for g_node in self.graph:

            # SUCCESSORS extracted here:
            node_successors = list(self.graph.successors(g_node))
            successors_count = len(node_successors)

            if successors_count == 0 :
                self.leaf_nodes.append(g_node)
                #   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +
                # app_msg = "Node with no predecessors found: '{}'".format(g_node)
                # print(app_msg)
                #   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +
            else:
                #  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +
                # app_msg = "Node's '{}' successors ({}): {}".format(g_node, successors_count, node_successors)
                # print(app_msg)
                #  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +
                pass

    def _shift_position(self, nodes=None, cumul_shift=0, start='root'):

        for g_node in nodes:
            if start == 'root':
                next_nodes = list(self.graph.successors(g_node))
            else:
                next_nodes = list(self.graph.predecessors(g_node))

            if 'pos' not in self.graph.nodes[g_node]:
                # 'pos' attribute missing - evaluate next root node
                continue
            pos = self.graph.nodes[g_node]['pos'].split(',')
            current_pos = (float(pos[0]), float(pos[1]))

            for next_node in next_nodes:
                if 'pos' not in self.graph.nodes[next_node]:
                    # 'pos' attribute missing - evaluate next root node
                    continue
                pos = self.graph.nodes[next_node]['pos'].split(',')
                next_pos = (float(pos[0]), float(pos[1]))

                # used LR/RL directions:
                # h_space = abs(next_pos[0]-current_pos[0])
                h_space = next_pos[0]-current_pos[0]
                # used TB/BT directions:
                # v_space = abs(next_pos[1]-current_pos[1])
                v_space = next_pos[1]-current_pos[1]

                incr_shift = 0

                if self.dir == 'LR':
                    if  h_space < self.sep:
                        if h_space < 0: h_space = 0
                        v_shift = self.sep - h_space
                        self.graph.nodes[next_node]['pos'] = "{},{}".format(next_pos[0] + cumul_shift + v_shift, next_pos[1])
                        print("Shifting position for this node: {}".format(next_node))
                        incr_shift = v_shift
                        self._shift_position(next_nodes, cumul_shift + incr_shift)

        pass

    def update_positions(self, nodesep=0):

        # Initialize the node separation property (in SVG unit)
        self.sep = nodesep

        # Initialize the direction property:
        # if 'rankdir' in self.graph.graph.keys():
        #     self.dir = self.graph['rankdir']
        self.dir = self.graph.graph.get('rankdir')
        self.dir = 'LR' if self.dir == None else self.dir
        
        self._scale_positions()

        # # Pass 1: Root to leaf nodes
        # self._get_root_nodes()
        # self._shift_position(self.root_nodes, start='root')

        # # Pass 2: Leaf to Root nodes
        # self._get_leaf_nodes()
        # self._shift_position(self.leaf_nodes, start='leaf')

        return self.graph


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# Building the complete SVG object
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

def draw_svg(graph, svg_file_name=''):

    # ---------------------------------------------------------------
    # Demo graph
    # ---------------------------------------------------------------
    # Manually adjust size of the SVG canvas/viewBox/background:
    width = SVG_WIDTH
    height = SVG_HEIGHT
    # RFE: SVG canvas/viewBox size to be calculated automatically
    # ---------------------------------------------------------------

    svg_graph = SvgGraph(graph)
    t_graph = svg_graph.update_positions(NODE_SEP)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # 1) Create the SVG content
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # main doc
    s_doc = get_main_doc()
    # Main svg
    s_svg, e_svg = get_main_svg(width, height)
    # Main graph
    s_graph, e_graph = get_main_graph(height)
    # Background
    s_bkgd = get_svg_background(width, height)

    # Nodes:
    s_nodes = get_svg_nodes(t_graph)
    # Edges:
    s_edges = get_svg_edges(t_graph)

    # Building the entire SVG with pretty output (indent with TAB):
    svg_doc = [
        s_doc,
        '\n',
        s_svg,
            # Graph (start)
            (TAB*1)+s_graph,
            # Background:
            (TAB*2)+s_bkgd,
            # Nodes:
            s_nodes,
            # Edges:
            s_edges,
            # Graph (end)
            (TAB*1)+e_graph,
        e_svg
    ]
    svg_document = '\n'.join(svg_doc)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # 2) Save the created SVG as a file if file path provided:
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    if isinstance(svg_file_name, str) and len(svg_file_name) > 0:
        try:
            svg_file = open(file=svg_file_name, mode='w')
            svg_file.write(svg_document)
            svg_file.close()

            #   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +
            app_msg = 'Success! SVG image saved: {}'.format(svg_file_name)
            print(app_msg)
            #   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +

        except IOError as err:
            #   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +
            err_msg = 'Unable to save the SVG image!'
            err_msg += 'Error: {} -> {}'.format(err_msg, err)
            print(err_msg)
            #   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +

    return svg_document


