import pandas as pd
import re


def __get_source_type(data_source:str) -> str:
    if data_source == 'CONSOLE':
        return 'CONSOL'
    elif re.search(r'.*\.csv(\.zip)?', data_source):   
        return 'CSV'
    elif re.search(r'.*\.db/\w+', data_source):
        return 'SQLITE'
    elif re.search(r'Data Source.*', data_source):
        return 'MSSQL'
    elif re.search(r'.*\.html', data_source):   
        return 'HTML'
    elif re.search(r'.*\.json', data_source):   
        return 'JSON'
    elif re.search(r'.*\.xml', data_source):   
        return 'XML'
    elif re.search( r'(.+\.xlsx)| (.+\.xls) | (.+\.xlsm)| (.+\.xlsb)| (.+\.odf)| (.+\.ods)| (.+\.odt)', data_source):   
        return 'EXCEL'

# def __get_source_type_forward(data_source:str) -> str:
#     ds_type,ds_path =data_source.split(":",1)
#     print(ds_type,ds_path)
#     return 'CSV'




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



    