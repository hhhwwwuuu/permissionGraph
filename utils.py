import numpy as np
import pandas as pd

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




