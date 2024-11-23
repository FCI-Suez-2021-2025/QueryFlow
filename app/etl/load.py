import pandas as pd
import sqlalchemy

def __load_to_csv(data, csv_file_path):
    data.to_csv(csv_file_path , header=None, mode='a')


def __load_to_sqlite(data, db_file_path, table_name):
    sqlite_engine = sqlalchemy.create_engine(f'sqlite:///{db_file_path}')
    data.to_sql(table_name, sqlite_engine, if_exists='append', index=False)


def __load_to_mssql(data, connection_string):
    connection_string = connection_string.split("/")
    server_name = connection_string[0]
    db_name = connection_string[1]
    table_name = connection_string[2]

    mssql_engine = sqlalchemy.create_engine(f'mssql+pyodbc://{server_name}/{db_name}?trusted_connection=yes&driver=SQL+Server+Native+Client+11.0')
    data.to_sql(table_name, mssql_engine, if_exists='append', index=False)

def __load_to_json(data, file_path):
    data.to_json(file_path)

def __load_to_html(data, file_path):
    data.to_html(file_path)

def __load_to_xml(data, file_path):
    data.to_xml(file_path)

def __load_to_excel(data, file_path):
    data.to_excel(file_path) 