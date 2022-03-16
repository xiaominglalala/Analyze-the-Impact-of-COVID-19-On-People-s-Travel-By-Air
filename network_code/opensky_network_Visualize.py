import opensky_preprocess as op

import networkx as nx
import plotly as py
import plotly.graph_objects as go
from collections import OrderedDict


# transfer the matrix into graph, and display it through matplotlib
def network():
    states_pos = op.getAirports2()
    matrix, states = op.network_Matrix()
    graph = nx.DiGraph()
    for state in states:
        graph.add_node(state,pos=(list(states_pos.get(state))))
    edge = []
    weight = []
    # iterate all edges 
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            # for those edge with weight 0, don't add it
            if (matrix[i][j] == 0):
                continue
            graph.add_edge(states[i], states[j], weight=matrix[i][j])
            edge.append((i,j))
            weight.append(matrix[i][j])


    # add pos to each node by given method
    pos = nx.spring_layout(graph)
    nx.set_node_attributes(graph, pos, 'pos')
    nx.set_edge_attributes(graph, OrderedDict(zip(edge, weight)), 'weight')
    return graph, weight

def create_edge():
    G, weight = network()
    edge_x = []
    edge_y = []
    xtext = []
    ytext = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        xtext.append((x0+x1)/2)
        ytext.append((y0+y1)/2)
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'), 
        hoverinfo='none', 
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
    weights_trace = go.Scatter(
        x=xtext,y= ytext, 
        mode='markers',
        marker_size=0.5,
        text=weight,
        # textposition='top center',
        hovertemplate='weight: %{text}<extra></extra>')

    return node_trace, edge_trace, weights_trace

def color_nodes():
    G, weight = network()
    node_trace, edge_trace, weights_trace = create_edge()
    # node_trace, edge_trace = create_edge()
    node_adjacencies = []
    node_text = []
    for _, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('State: ' + str(adjacencies[0]) + ', Out Degree: '+str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    return node_trace, edge_trace, weights_trace

def create_networkGraph():
    edge_trace, node_trace, weights_trace = color_nodes()
    # edge_trace, node_trace = color_nodes()
    # fig = go.Figure(data=[edge_trace, node_trace],
    fig = go.Figure(data=[edge_trace, node_trace, weights_trace],
             layout=go.Layout(
                title='<br>Network graph',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
                
    # pyplt = py.offline.plot
    # pyplt(fig, filename='figures/opensky_network.html')
    fig.show()

def main():
    create_networkGraph()

if __name__ == '__main__':
    main()