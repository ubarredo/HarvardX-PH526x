from collections import Counter

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from scipy.stats import bernoulli


def er_graph(nodes, prob):
    net = nx.Graph()
    net.add_nodes_from(range(nodes))
    for node1 in net.nodes():
        for node2 in net.nodes():
            if node1 < node2 and bernoulli.rvs(p=prob):
                net.add_edge(node1, node2)
    return net


def basic_net_stats(net, name):
    print("-------- %s --------" % name)
    print("Number of nodes: %d" % net.number_of_nodes())
    print("Number of edges: %d" % net.number_of_edges())
    print("Average degree: %.2f" % np.mean(list(net.degree().values())))
    subgraphs = nx.connected_component_subgraphs(net)
    print("Composition:", [sub.number_of_nodes() for sub in subgraphs])
    net_lcc = max(nx.connected_component_subgraphs(net), key=len)
    print("Connection%:", round(100 * len(net_lcc) / len(net), 2))
    print()


def plot_degree_distribution(net, name, col='blue'):
    plt.hist(list(net.degree().values()), histtype='step', label=name,
             color=col)
    plt.title("Degree distribution")
    plt.xlabel("Degree $k$")
    plt.ylabel("$P(k)$")
    plt.legend()


def stat_homophily(char):
    counts = np.array(list(Counter(char.values()).values()))
    return sum(counts / sum(counts) * (counts - 1) / (sum(counts) - 1))


def real_homophily(net, char, ids):
    num_same_ties, num_ties = 0, 0
    for n1 in net.nodes():
        for n2 in net.nodes():
            if n1 < n2:
                if ids[n1] in char and ids[n2] in char:
                    if net.has_edge(n1, n2):
                        num_ties += 1
                        if char[ids[n1]] == char[ids[n2]]:
                            num_same_ties += 1
    return num_same_ties / num_ties


matrix1 = np.loadtxt('docs/village1_relationships.csv', delimiter=',')
matrix2 = np.loadtxt('docs/village2_relationships.csv', delimiter=',')
net1 = nx.to_networkx_graph(matrix1)
net2 = nx.to_networkx_graph(matrix2)

pid1 = np.array(pd.read_csv('docs/village1_pid.csv', header=None)).flatten()
pid2 = np.array(pd.read_csv('docs/village2_pid.csv', header=None)).flatten()

df = pd.read_stata('docs/individual_characteristics.dta')
df1 = df[df['village'] == 1]
df2 = df[df['village'] == 2]

gender1 = dict(zip(df1['pid'], df1['resp_gend']))
gender2 = dict(zip(df2['pid'], df2['resp_gend']))
caste1 = dict(zip(df1['pid'], df1['caste']))
caste2 = dict(zip(df2['pid'], df2['caste']))
religion1 = dict(zip(df1['pid'], df1['religion']))
religion2 = dict(zip(df2['pid'], df2['religion']))

homophily = pd.DataFrame(columns=(['stat_gender', 'real_gender',
                                   'stat_caste', 'real_caste',
                                   'stat_religion', 'real_religion']))
homophily.loc['village1'] = (stat_homophily(gender1),
                             real_homophily(net1, gender1, pid1),
                             stat_homophily(caste1),
                             real_homophily(net1, caste1, pid1),
                             stat_homophily(religion1),
                             real_homophily(net1, religion1, pid1))
homophily.loc['village2'] = (stat_homophily(gender2),
                             real_homophily(net2, gender2, pid2),
                             stat_homophily(caste2),
                             real_homophily(net2, caste2, pid2),
                             stat_homophily(religion2),
                             real_homophily(net2, religion2, pid2))

my_graph = er_graph(15, .1)
net1_lcc = max(nx.connected_component_subgraphs(net1), key=len)
net2_lcc = max(nx.connected_component_subgraphs(net2), key=len)

plt.figure(figsize=(9, 4))
plt.subplot(121)
plot_degree_distribution(my_graph, "My graph", 'green')
plt.subplot(122)
nx.draw(my_graph, with_labels=True, node_color='green')
plt.savefig('plots/social_network_analysis_1')

plt.figure(figsize=(12, 4))
plt.subplot(131)
nx.draw(net1_lcc, node_color='red', node_size=1, alpha=.5)
plt.subplot(132)
plot_degree_distribution(net1, "Village 1", 'red')
plot_degree_distribution(net2, "Village 2", 'blue')
plt.subplot(133)
nx.draw(net2_lcc, node_color='blue', node_size=1, alpha=.5)
plt.savefig('plots/social_network_analysis_2')

basic_net_stats(my_graph, "My graph")
basic_net_stats(net1, "Village 1")
basic_net_stats(net2, "Village 2")
print("### Homophily measure ###")
print(homophily)

plt.show()
