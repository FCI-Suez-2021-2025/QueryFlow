from enum import Enum

import sqlalchemy
import pandas as pd
from app.etl.data_src.IDataTypes import IDataTypes

class DatabaseTypes(Enum):
    MSSQL = 'mssql'
    SQLITE = 'sqlite'


class Database(IDataTypes):
    def __init__(self, type,path):
        self.type = type
        self.path = path
        if type == DatabaseTypes.MSSQL:
            connection_string = path.split("/")
            server_name = connection_string[0]
            db_name = connection_string[1]
            self.table_name = connection_string[2]
            self.engine = sqlalchemy.create_engine(
                f'mssql+pyodbc://{server_name}/{db_name}?trusted_connection=yes&driver=SQL+Server+Native+Client+11.0')
            table = self.engine.execute(f"SELECT * FROM {self.table_name};")
        elif type == DatabaseTypes.SQLITE:
            self.table_name = path.split('/')[1]
            self.engine = sqlalchemy.create_engine(f'sqlite:///{self.path}/')

    def extract(self,path):
            data = pd.read_sql(f'select * from {self.table_name}', self.engine)
            return data

    def load(self,data,path):
            data.to_sql(self.table_name, self.engine, if_exists='append', index=False)

