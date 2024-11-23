from enum import Enum

import pandas as pd
from app.etl.data_src.IDataTypes import IDataTypes


class FlatDataTypes(Enum):
    CSV = 'csv'
    EXCEL = 'excel'
    JSON = 'json'
    XML = 'xml'
    HTML ='html'

class FlatData(IDataTypes):
    def __init__(self,type):
        self.type = type
        # super().__init__(self,type)

    def extract(self,path):

        match self.type:
            case FlatDataTypes.CSV:
                data = pd.read_csv(path)
            case FlatDataTypes.EXCEL:
                data = pd.read_excel(path)
            case FlatDataTypes.JSON:
                data = pd.read_json(path)
            case FlatDataTypes.XML:
                data = pd.read_xml(path)
            case FlatDataTypes.HTML:
                data = pd.read_html(path)
            case _:
                data = None
        return data

    def load(self,data,path):
        match self.type:
            case FlatDataTypes.CSV:
                data.to_csv(path)
            case FlatDataTypes.EXCEL:
                data.to_excel(path)
            case FlatDataTypes.JSON:
                data.to_json(path)
            case FlatDataTypes.XML:
                data.to_xml(path)
            case FlatDataTypes.HTML:
                data.to_html(path)


