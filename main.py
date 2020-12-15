'''
Author: Zhiqiang
Date: 2020.12.11
Description: This project is to generate the relation graph among
             requested permissions of Android apps in one genre.
'''

import networkx as nx
from tqdm import tqdm
import matplotlib.pyplot as plt
import buildGraph as bg





if __name__ == '__main__':
    print("Loading permission list from csv...")
    categories, permissions, data = bg.dataReader()

    print("Starting graph generation...")
    pbar = tqdm(total=len(categories))
    for category in categories:
        print("Creating graph for permission {}".format(category))
        graph = bg.buildGraph(category, permissions, data.groupby('category').get_group(category))
        nx.draw(graph, with_labels=True, node_size=1000, pos= nx.shell_layout(graph))
        plt.show()
        pbar.update(1)
        #print(graph.nodes.data())
        adj_matrix = bg.adjacencyGraph(graph)
        break
    pbar.close()


