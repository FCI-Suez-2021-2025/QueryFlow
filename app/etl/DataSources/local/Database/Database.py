import sqlalchemy
import pandas as pd

from app.etl.DataSources.local.IDataSource import IDataSource
from app.etl.DataSources.local.Database.DataTypes import DatabaseType


class Database(IDataSource):
    def __init__(self, type, connection_string) -> None:
        if (type == DatabaseType.MSSQL):
            connection_string = connection_string.split('::')[1].split('/')
            self.engine = sqlalchemy.create_engine(
                f'mssql+pyodbc://{connection_string[0]}/{connection_string[1]}?trusted_connection=yes&driver=SQL+Server+Native+Client+11.0')
            self.table_name = connection_string[2]
        elif (type == DatabaseType.SQLLITE):
            cs = connection_string.split('::')[1].split('/')[0]
            self.engine = sqlalchemy.create_engine(f'sqlite:///{cs}')
            self.table_name = connection_string.split('::')[1].split('/')[1]

    def extract(self, file_path):
        data = pd.read_sql(f'select * from {self.table_name}', self.engine)
        return data

    def load(self, data, file_path):
        data.to_sql(self.table_name, self.engine, if_exists='append', index=False)