import pandas as pd
import sqlalchemy
from app.cv.bird import *




###########################
#====== OLD EXTRACT ======#
###########################
def __extract_from_csv(file_path) -> pd.DataFrame:
    # file_type,file_path=data_source.split(":",1)
    data = pd.read_csv(file_path)
    return data

    
def __extract_from_sqlite(db_file_path, table_name) -> pd.DataFrame:
    sqlite_engine = sqlalchemy.create_engine(f'sqlite:///{db_file_path}')
    data = pd.read_sql(f'select * from {table_name}', sqlite_engine)
    return data


def __extract_from_mssql(connection_string:str) -> pd.DataFrame:
    connection_string = connection_string.split("/")
    server_name = connection_string[0]
    db_name = connection_string[1]
    table_name = connection_string[2]

    mssql_engine = sqlalchemy.create_engine(f'mssql+pyodbc://{server_name}/{db_name}?trusted_connection=yes&driver=SQL+Server+Native+Client+11.0')
    table = mssql_engine.execute(f"SELECT * FROM {table_name};")
    
    data = pd.DataFrame(table, columns=table.keys())
    return data


def __extract_from_html(file_path) -> pd.DataFrame:
    data = pd.read_html(file_path)
    return data[0]

def __extract_from_json(file_path) -> pd.DataFrame:
    data = pd.read_json(file_path, orient='records')
    return data

def __extract_from_xml(file_path) -> pd.DataFrame:
    data = pd.read_xml(file_path)
    return data

def __extract_from_excel(file_path) -> pd.DataFrame:
    data = pd.read_excel(file_path)
    return data
def __extract_from_video(file_path):
    d = DetectBirds(file_path)
    birds = d.detect()
    return str(birds)