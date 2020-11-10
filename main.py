import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

g = nx.DiGraph()

edges = np.array([["hoge", 2],
                  [5, "hoge"],
                  ["hoge", "fuga"],
                  ["fuga", "bar"], ])

g.add_edge(0, 1)
g.add_edges_from(edges)
nx.draw_networkx(g, node_size=1500)
plt.show()