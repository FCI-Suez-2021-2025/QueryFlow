from abc import ABC
from enum import Enum
from typing import override

import pandas as pd
from app.etl.data.base_data_types import (
    FieldPathBase,
    IExtractor,
    ILoader,
)


class FlatDataTypes(Enum):
    CSV = "csv"
    EXCEL = "excel"
    JSON = "json"
    XML = "xml"
    HTML = "html"


class IFlatData(FieldPathBase, IExtractor, ILoader, ABC):
    def __init__(self, path: str) -> None:
        FieldPathBase.__init__(self, path)


class CSVFlatData(IFlatData):
    def __init__(self, path: str) -> None:
        IFlatData.__init__(self, path)

    @override
    def extract(self) -> pd.DataFrame:
        return pd.read_csv(self.path)

    @override
    def load(self, data: pd.DataFrame) -> None:
        return data.to_csv(self.path)


class EXCELFlatData(IFlatData):
    def __init__(self, path: str) -> None:
        IFlatData.__init__(self, path)

    @override
    def extract(self) -> pd.DataFrame:
        return pd.read_excel(self.path)

    @override
    def load(self, data: pd.DataFrame) -> None:
        return data.to_excel(self.path)


class JSONFlatData(IFlatData):
    def __init__(self, path: str) -> None:
        IFlatData.__init__(self, path)

    @override
    def extract(self) -> pd.DataFrame:
        return pd.read_json(self.path)

    @override
    def load(self, data: pd.DataFrame) -> None:
        return data.to_json(self.path)


class XMLFlatData(IFlatData):
    def __init__(self, path: str) -> None:
        IFlatData.__init__(self, path)

    @override
    def extract(self) -> pd.DataFrame:
        return pd.read_xml(self.path)

    @override
    def load(self, data: pd.DataFrame) -> None:
        # replace spaces in column names with underscore when loading data into a xml file
        # because  XML tags cannot contain spaces.
        return data.rename(columns=lambda x: x.replace(" ", "_")).to_xml(self.path)


class HTMLFlatData(IFlatData):
    def __init__(self, path: str) -> None:
        IFlatData.__init__(self, path)

    @override
    def extract(self) -> pd.DataFrame:
        file_path, table_number = self.path.split("|", 1)
        return pd.read_html(file_path)[table_number - 1]

    @override
    def load(self, data: pd.DataFrame) -> None:
        return data.to_html(self.path)
