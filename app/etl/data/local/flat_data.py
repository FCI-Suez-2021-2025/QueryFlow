from abc import ABC
from enum import Enum
import re
from typing import Any, override

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
        def __sanitize_xml_tag_name(column_name: Any) -> str:
            tag_name = str(column_name)

            # handle empty column name
            if not tag_name:
                return "_"

            # Replace spaces with underscores
            tag_name = tag_name.replace(" ", "_")

            # Ensure it doesn't start with a number
            if tag_name[0].isdigit():
                tag_name = "_" + tag_name  # Prepend an underscore

            # Remove invalid characters (punctuation, special characters)
            tag_name = re.sub(r"[^A-Za-z0-9_-]", "", tag_name)

            # if tag_name becomes empty after removing invalid characters
            if not tag_name:
                return "_"
            # Handle colons (used only in namespaces)
            if ":" in tag_name:
                tag_name = tag_name.replace(":", "_")

            return tag_name

        return data.rename(columns=__sanitize_xml_tag_name).to_xml(self.path)


class HTMLFlatData(IFlatData):
    def __init__(self, path: str) -> None:
        IFlatData.__init__(self, path)

    @override
    def extract(self) -> pd.DataFrame:
        file_path, table_number = self.path.split("|", 1)
        return pd.read_html(file_path)[int(table_number) - 1]

    @override
    def load(self, data: pd.DataFrame) -> None:
        return data.to_html(self.path)
