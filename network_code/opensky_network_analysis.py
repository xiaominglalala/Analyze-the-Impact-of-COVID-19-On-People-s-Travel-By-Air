
import opensky_preprocess as op

import numpy as np
import networkx as nx
import community
import matplotlib.pyplot as plt

# transfer the matrix into graph, and display it
def network():
    matrix, states = op.network_Matrix()
    inDegree = [0 for i in range(len(states))]
    outDegree = [0 for i in range(len(states))]
    graph = nx.DiGraph()
    # iterate all edges 
    for i in range(len(matrix)):
        # print(matrix[i])
        for j in range(len(matrix[i])):
            # for those edge with weight 0, don't add it
            if (matrix[i][j] == 0):
                continue
            graph.add_edge(states[i], states[j], weight=matrix[i][j])
            outDegree[i] = outDegree[i] + 1
            inDegree[j] = inDegree[j] + 1

    return graph, states, inDegree, outDegree

def detailInfo():
    print()
    G, states, inDegree, outDegree = network()

    # output the in degree and out degree for each nodes
    for node, inD, outD in zip(states, inDegree, outDegree):
        print('State: ' + str(node) + ', In Degree = ' + str(inD) + ', Out Degree = ' + str(outD) + '  ')

    # Change G to an undirected graph and find the number of CCs
    undirected_G = G.to_undirected()
    nbr_components = nx.number_connected_components(undirected_G)
    print("\nNumber of connected components:", nbr_components)

    # compute the centralities for each nodes
    centralities = nx.betweenness_centrality(G)
    print()
    print("Betweeness of each node")
    for node in list(G.nodes()):
        print('State: ' + str(node) + ', Betweemess = ' + str(centralities[node]))

    #####################
    # Clustering
    #####################
    # Conduct modularity clustering
    # Create an unweighted version of G because modularity works only on graphs with non-negative edge weights
    unweighted_G = nx.Graph()
    for u, v in undirected_G.edges():
        unweighted_G.add_edge(u, v)
    partition = community.best_partition(unweighted_G)

    # Print clusters (You will get a list of each node with the cluster you are in)
    print()
    print("Clusters")
    print(partition)

    values = [partition.get(node) for node in unweighted_G.nodes()]
    nx.draw_spring(unweighted_G, cmap = plt.get_cmap('jet'), node_color = values, node_size=10, with_labels=False)
    plt.show()

    # Determine the final modularity value of the network
    modValue = community.modularity(partition, unweighted_G)
    print("modularity: {}".format(modValue))

    # print out the cluster coefficient for each nodes
    print('Cluster Coefficient: ')
    d = nx.clustering(G)
    for key, value in d.items():
        print('State: ' + str(key) + ', Cluster Coefficient: ' + str(value))
    
    # print out the triangles for each nodes
    print('Triangles：')
    ave = 0
    d = nx.triangles(undirected_G)
    for key, value in d.items():
        print('State: ' + str(key) + ', Triangles: ' + str(value))
        ave = ave + value
    print('Average Triangles: ', ave / len(d))

    # print out the averages for the centrality metrics
    d = nx.closeness_centrality(G)
    for key, value in d.items():
        ave = ave + value
    print('Averages for the Centrality Metrics: ', ave / len(d))

def average_shortest_path_length(G):
    ave_length = 0
    size = 0
    path = dict(nx.algorithms.shortest_paths.generic.shortest_path_length(G))
    path = list(path.values())
    for i in range(len(path)):
        size = size + len(path[i])
        ave_length = ave_length + np.sum(list(path[0].values()))
    ave_length = ave_length / size
    return ave_length

def cluster_analysis():
    G, states, inDegree, outDegree = network()
    undirected_G = G.to_undirected()
    unweighted_G = nx.Graph()
    for u, v in undirected_G.edges():
        unweighted_G.add_edge(u, v)
    partition = community.best_partition(unweighted_G)

    # Print clusters (You will get a list of each node with the cluster you are in)
    print()
    print("Clusters")
    print(partition)

    # Get the values for the clusters and select the node color based on the cluster value
    values = [partition.get(node) for node in unweighted_G.nodes()]
    nx.draw_spring(unweighted_G, cmap = plt.get_cmap('jet'), node_color = values, node_size=10, with_labels=False)
    plt.show()

    # Determine the final modularity value of the network
    modValue = community.modularity(partition, unweighted_G)
    print("modularity: {}".format(modValue))

def info():
    # simply print out some basic and clean info about the network
    G, states, inDegree, outDegree = network()
    print('Number of nodes: ', len(G.nodes()))
    print('Number of edges: ', len(G.edges()))
    print('Density: ', nx.density(G))
    print('Average Degree(In + Out): ', np.average(inDegree) + np.average(outDegree))
    print('Average Shortest Path Length: ', nx.average_shortest_path_length(G))
    print('Average Clustering Coefficient: ', nx.algorithms.cluster.average_clustering(G))
    
def main():
    # the matrix is too large to display
    # network()
    # basic information
    print('BASIC INFO =>')
    info()
    # cluster analysis
    print('CLUSTER ANALYSIS =>')
    cluster_analysis()
    # detailed information
    print('DETAILED INFO =>')
    detailInfo()

if __name__ == '__main__':
    main()