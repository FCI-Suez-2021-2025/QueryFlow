import pandas as pd
from app.cv.OperationMain import filterColumns
from app.etl.data_src.DataSrcFactory import DataSrcFactory
from app.etl.helpers import __filter


result = None


def extract(source_type:str,data_source:str) -> pd.DataFrame:
    data = DataSrcFactory.createDataObj(source_type, data_source)
    data = data.extract(data_source)
    return data




def transform(data:pd.DataFrame, criteria:dict) -> pd.DataFrame:

    if type(data) == list:
        if criteria['COLUMNS'] != '__all__' :
            columns = criteria['COLUMNS']
            data = filterColumns(columns,data)
        else:
            data = pd.DataFrame(data)

    else:
        print('step over')
        # filtering
        if criteria['FILTER']:
            data = __filter(data, criteria['FILTER'])

        # columns
        if criteria['COLUMNS'] != '__all__':
            data = data.filter(items=criteria['COLUMNS'])

        # distinct
        if criteria['DISTINCT']:
            data = data.drop_duplicates()

        # ordering
        if criteria['ORDER']:
            column = criteria['ORDER'][0]
            data = data.sort_values(column, ascending=criteria['ORDER'][1] == 'ASC')

        # limit
        if criteria['LIMIT']:
            data = data[:criteria['LIMIT']]
    return data


def load(data:pd.DataFrame, data_destination:str,source_type:str):
    global result
    data_source = DataSrcFactory.createDataObj(source_type,data_destination)
    result = data_source.load(data,data_destination)
    if result is None:
        result = "Execution Done!"
    return data