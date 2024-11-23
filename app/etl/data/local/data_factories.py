from app.etl.data.local.database import *
from app.etl.data.local.flat_data import *
from app.etl.data.local.media import *
from app.etl.data.local.base_data_types import *
from app.etl.data.remote.GoogleEarthAPIDataCollector import *


class ExtractableDataFactory:
    @classmethod
    def create(cls, type: str, path: str) -> IExtractor:
        extractable_enum = cls.__getType(type)
        match extractable_enum:
            case DatabaseTypes.MSSQL:
                return MSSQLDatabase(path)
            case DatabaseTypes.SQLITE:
                return SQLITEDatabase(path)
            case FlatDataTypes.JSON:
                return JSONFlatData(path)
            case FlatDataTypes.HTML:
                return HTMLFlatData(path)
            case FlatDataTypes.CSV:
                return CSVFlatData(path)
            case FlatDataTypes.XML:
                return XMLFlatData(path)
            case FlatDataTypes.EXCEL:
                return EXCELFlatData(path)
            case MediaTypes.IMAGES:
                return BirdImagesMedia(path)
            case MediaTypes.VIDEO:
                return VideoMaximumBirdsInFrameMedia(path)
            case "google_earth_engine" :
                google_earth_api = GoogleEarthAPIDataCollector(path)
                return google_earth_api.collect("2024-1-22", "2024-06-14", 30.0065457, 27.5157469, 1000)
            case _:
                raise ValueError(type + " is not supported datasource type")

    @classmethod
    def __getType(cls, type: str) -> Enum:
        type = type.lower()
        if type == "mssql":
            return DatabaseTypes.MSSQL
        elif type == "sqlite":
            return DatabaseTypes.SQLITE
        elif type == "json":
            return FlatDataTypes.JSON
        elif type == "html":
            return FlatDataTypes.HTML
        elif type == "csv":
            return FlatDataTypes.CSV
        elif type == "xml":
            return FlatDataTypes.XML
        elif type == "excel":
            return FlatDataTypes.EXCEL
        elif type == "video":
            return MediaTypes.VIDEO
        elif type == "images" or type == "folder" or type == "image":
            return MediaTypes.IMAGES
        elif type in {"google_earth_engine", "gee"}:  # Map aliases
            return "google_earth_engine"
        else:
            raise ValueError(type + " is not supported datasource type")


class LoadableDataFactory:
    @classmethod
    def create(cls, type: str, path: str) -> ILoader:
        objType = cls.__getType(type)
        match objType:
            case DatabaseTypes.MSSQL:
                return MSSQLDatabase(path)
            case DatabaseTypes.SQLITE:
                return SQLITEDatabase(path)
            case FlatDataTypes.JSON:
                return JSONFlatData(path)
            case FlatDataTypes.HTML:
                return HTMLFlatData(path)
            case FlatDataTypes.CSV:
                return CSVFlatData(path)
            case FlatDataTypes.XML:
                return XMLFlatData(path)
            case FlatDataTypes.EXCEL:
                return EXCELFlatData(path)
            case _:
                raise ValueError(type + " is not supported data source type")

    @classmethod
    def __getType(cls, type: str) -> Enum:
        type = type.lower()
        if type == "mssql":
            return DatabaseTypes.MSSQL
        elif type == "sqlite":
            return DatabaseTypes.SQLITE
        elif type == "json":
            return FlatDataTypes.JSON
        elif type == "html":
            return FlatDataTypes.HTML
        elif type == "csv":
            return FlatDataTypes.CSV
        elif type == "xml":
            return FlatDataTypes.XML
        elif type == "excel":
            return FlatDataTypes.EXCEL
        else:
            raise ValueError(type + " is not supported data destination type")
