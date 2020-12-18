import numpy as np
import pandas as pd
import buildGraph as bg
import networkx as nx


def normalization(matrix):
    matrix = np.array(matrix)
    _range = np.max(matrix) - np.min(matrix)
    return (matrix - np.min(matrix)) / _range

def filterRarePermission():
    data = pd.read_csv('data/permission_frequency_on_category.csv', encoding='utf-8')
    rarePermissions = {}
    permissions = data.columns.values.tolist()[1:11]
    for index, row in data.iterrows():
        for i in range(len(row[1:11])):
            # filiter out rare permissions that less than 5% ocurrence in dataset
            if row[i+1]/ row['Count'] < 0.05:
                if row['category'] in rarePermissions:
                    rarePermissions[row['category']].append(permissions[i])
                else:
                    rarePermissions[row['category']] = [permissions[i]]
    return rarePermissions


def freqPermission(category, permission):
    data = pd.read_csv('data/permission_frequency_on_category.csv', encoding='utf-8')
    return data.loc[data.category == category, permission][0] / data.loc[data.category == category, 'Count'][0]


def weightProportion(src, dst, graph):
    weightMax = np.max(bg.weightMatrix(graph, mtype='weight'))
    return graph.edges[src,dst]['weight'] / weightMax



def searchCommon(graph):
    '''

    :param graph:
    :return: common permissions
    '''


    # generate the assoicated matrix
    adj_matrix = bg.weightMatrix(graph, mtype='adjacency') + np.eye(len(bg.perList))
    weight_matrix = bg.weightMatrix(graph, mtype='weight')
    dg_matrix = bg.degreeMatrix(graph)

    # check the optimal start node

    # pick the nodes with large degree & high request frequency
    # 获取度最大 且 请求次数最多的permissions集
    row, _ = np.where(dg_matrix == np.max(dg_matrix))
    maxDegree = np.array([graph.nodes[bg.perList[i]]['count'] for i in row])
    roots = [bg.perList[i] for i in range(len(bg.perList)) if graph.nodes[bg.perList[i]]['count'] == np.max(maxDegree)]
    #print(roots)

    '''
    从roots中的一个节点开始BFS
    寻找common permissions的组合
    '''
    result = []
    per = ['Calendar', 'Contacts', 'Camera', 'Location', 'Microphone', 'Phone', 'SMS', 'Call Log', 'Storage', 'Sensors']
    for root in roots:
        result.append(BFS(root,per, graph))
    return result

def DFS(root, permissions, graph):
    # # sort the neighbor by degree of node and weight of edges
    # def sortNeighbor(root, nodes):
    #     results = {}
    #     for node in nodes:
    #         if node in permissions:
    #             results[node] = {'degree': graph.degree[root],
    #                              'weight': graph.edges[root, node]['weight'],
    #                              'count': graph.nodes[node]['count']}
    #
    #     results = sorted(results.items(), key=lambda x: (x[1]['count'], x[1]['weight'], x[1]['degree']), reverse=True)
    #     return results


    common = []
    common.append(root)

    permissions.remove(root)

    nodes = [u for u,_ in nx.bfs_predecessors(graph, source=root, depth_limit=1)]
    #print(nodes)
    neighbors = sortNeighbor(root, nodes,permissions, graph)
    #print(neighbors)
    '''
    判断排序后的第一个是否满足要求，
    若满足，选取该点作为common，
    否则，结束
    '''
    if freqPermission(graph.graph['name'], neighbors[0][0]) < 0.05 or weightProportion(root, neighbors[0][0], graph) < 0.2:
        return common
    elif neighbors[0][0] in permissions:
        common.extend(DFS(neighbors[0][0], permissions, graph))
        return common
    else:
        return common

def BFS(root, permissions, graph):
    common = []

    if len(permissions) == 0 or root not in permissions or root in common:
        return common

    common.append(root)
    permissions.remove(root)

    nodes = [u for u,_ in nx.bfs_predecessors(graph, source=root, depth_limit=1)]
    neighbors = sortNeighbor(root, nodes,permissions, graph)

    '''
    广度优先筛选符合条件的permissions
    若满足条件，选取为common
    否则， 跳过
    '''
    #print(neighbors)
    for key, values in neighbors:
        if freqPermission(graph.graph['name'], key) < 0.05 or weightProportion(root, key, graph) < 0.2:
            break
        elif key in permissions:
            common.append(key)
            permissions.remove(key)

    for node in common[1:]:
        common.extend(BFS(node, permissions, graph))

    return common







# sort the neighbor by degree of node and weight of edges
def sortNeighbor(root, nodes, permissions, graph):
    results = {}
    for node in nodes:
        if node in permissions:
            results[node] = {'degree': graph.degree[root],
                            'weight': graph.edges[root, node]['weight'],
                            'count': graph.nodes[node]['count']}

    results = sorted(results.items(), key=lambda x: (x[1]['count'], x[1]['weight'], x[1]['degree']), reverse=True)
    return results








