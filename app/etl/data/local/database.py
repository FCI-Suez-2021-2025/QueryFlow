from abc import ABC, abstractmethod
from enum import Enum
from typing import final, override

import sqlalchemy
import pandas as pd

from app.etl.data.base_data_types import (
    FieldPathBase,
    IExtractor,
    ILoader,
)


class DatabaseTypes(Enum):
    MSSQL = "mssql"
    SQLITE = "sqlite"


class IDatabase(FieldPathBase, IExtractor, ILoader, ABC):
    def __init__(self, path: str):
        FieldPathBase.__init__(self, path)
        self.table_name: str = None  # type: ignore
        self.engine: sqlalchemy.Engine = None  # type: ignore
        self.initialize_connection()

    @abstractmethod
    def initialize_connection(self) -> None:
        pass

    @final
    def extract(self) -> pd.DataFrame:
        return pd.read_sql(f"select * from {self.table_name};", self.engine)

    @final
    def load(self, data: pd.DataFrame):
        data.to_sql(self.table_name, self.engine, if_exists="append", index=False)


class MSSQLDatabase(IDatabase):
    def __init__(self, path: str):
        IDatabase.__init__(self, path)

    @override
    def initialize_connection(self) -> None:
        connection_string = self.path.split("|")
        server_name = connection_string[0]
        data_base_name = connection_string[1]
        self.table_name = connection_string[2]
        self.engine = sqlalchemy.create_engine(
            f"mssql+pyodbc://@{server_name}/{data_base_name}?trusted_connection=yes&driver=ODBC+Driver+18+for+SQL+Server&Encrypt=no"
        )


class SQLITEDatabase(IDatabase):
    def __init__(self, path: str):
        IDatabase.__init__(self, path)

    @override
    def initialize_connection(self) -> None:
        path_parts = self.path.split("|")
        data_base_name = path_parts[0]
        self.table_name = path_parts[1]
        self.engine = sqlalchemy.create_engine(f"sqlite:///{data_base_name}")
