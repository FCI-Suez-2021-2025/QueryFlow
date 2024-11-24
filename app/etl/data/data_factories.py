from app.etl.data.local.database import *
from app.etl.data.local.flat_data import *
from app.etl.data.local.media import *
from app.etl.data.base_data_types import *
from app.etl.data.remote.remote_data import *


class ExtractorDataFactory:
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
            case RemoteDataTypes.GEE:
                return GEEDataExtractor(path)
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
            return RemoteDataTypes.GEE
        else:
            raise ValueError(type + " is not supported datasource type")


class LoaderDataFactory:
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
