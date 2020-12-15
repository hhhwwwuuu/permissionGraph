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

# def dataReader():
#     data = pd.read_csv('data/permission_preprocessed.csv', encoding= 'utf-8')
#
#     def getPermissions(data):
#         return data.columns.values.tolist()[2:]
#
#     def getCategory(data):
#         return list(set(data['category'].values.tolist()))
#
#     return getCategory(data), getPermissions(data), data
#
#
# def buildGraph(category, permissions, data):
#
#     ### connecting the relations of permissions based on apps
#     def connectEdge(graph):
#         for index, row in data.iterrows():
#             if 1 in row[2:].values.tolist():
#                 reqPermissions = [permissions[i] for i in range(len(permissions)) if row[2:].values.tolist()[i]]
#                 #print(reqPermissions)
#                 if len(reqPermissions) != 1:
#                     edges = combinations(reqPermissions, 2)
#                     for edge in edges:
#                         if graph.has_edge(edge[0], edge[1]):
#                             graph[edge[0]][edge[1]]['weight'] += 1
#                         else:
#                             graph.add_edge(edge[0], edge[1], weight=1)
#             else:
#                 continue
#         return graph
#
#     # create an empyt graph, namly category of apps
#     graph = nx.Graph(name=category)
#
#     # init all nodes by permissions
#     graph.add_nodes_from(permissions)
#
#     '''
#     add attributes to each node
#     name : naming the node with associated permission
#     count: count the requested times of each permissions
#     '''
#     for per in permissions:
#         graph.nodes[per]['name'] = per
#         try:
#             graph.nodes[per]['count'] = data[per].value_counts()[1]
#         except:
#             graph.nodes[per]['count'] = 0
#
#     graph = connectEdge(graph)
#
#     return graph





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
        break
    pbar.close()


