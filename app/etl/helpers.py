import pandas as pd
import re



def __filter(data:pd.DataFrame, filters:dict) -> pd.DataFrame:
    left = filters['left']
    right = filters['right'] 

    if filters["type"] == 'or' or filters["type"] == 'and':
        left = __filter(data, left)
        right = __filter(data, right)

        if filters["type"] == 'or':
            data = pd.concat([left, right])
        elif filters["type"] == 'and':
            data = pd.merge(left, right)
        data = data[~data.index.duplicated(keep='first')]

    elif filters["type"] == 'like':
        data = data[[True if re.match(right, str(x)) else False for x in data[left]]]
    elif filters["type"] == '>':
        data = data[data[left] > right]
    elif filters["type"] == '>=':
        data = data[data[left] >= right]
    elif filters["type"] == '<':
        data = data[data[left] < right]
    elif filters["type"] == '<=':
        data = data[data[left] <= right]
    elif filters["type"] == '==':
        data = data[data[left] == right]
    elif filters["type"] == '!=':
        data = data[data[left] != right]

    return data



    