from app.etl.data_src.Console import *
from app.etl.data_src.Database import *
from app.etl.data_src.FlatData import *
from app.etl.data_src.Media import *


class DataSrcFactory():
    @classmethod
    def createDataObj(cls,type,path):
        objType = cls.getType(type)
        objs = {
            DatabaseTypes.MSSQL: lambda: Database(DatabaseTypes.MSSQL,path),
            DatabaseTypes.SQLITE: lambda: Database(DatabaseTypes.SQLITE,path),
            FlatDataTypes.JSON: lambda: FlatData(FlatDataTypes.JSON),
            FlatDataTypes.HTML: lambda: FlatData(FlatDataTypes.HTML),
            FlatDataTypes.CSV: lambda: FlatData(FlatDataTypes.CSV),
            FlatDataTypes.XML: lambda: FlatData(FlatDataTypes.XML),
            FlatDataTypes.EXCEL: lambda: FlatData(FlatDataTypes.EXCEL),
            ConsoleTypes.CONSOLE: lambda: Console(ConsoleTypes.CONSOLE),
            ConsoleTypes.GUI: lambda: Console(ConsoleTypes.GUI),
            MediaTypes.IMAGES: lambda: Media(MediaTypes.IMAGES),
            MediaTypes.VIDEO: lambda: Media(MediaTypes.VIDEO),
        }
        return objs[objType]()

    @classmethod
    def getType(cls,type):
        type = type.lower()
        if type == 'mssql':
            return DatabaseTypes.MSSQL
        elif type == 'sqlite':
            return DatabaseTypes.SQLITE
        elif type == 'json':
            return FlatDataTypes.JSON
        elif type == 'html':
            return FlatDataTypes.HTML
        elif type == 'csv':
            return FlatDataTypes.CSV
        elif type == 'xml':
            return FlatDataTypes.XML
        elif type == 'excel':
            return FlatDataTypes.EXCEL
        elif type== 'video':
            return MediaTypes.VIDEO
        elif type == 'images' or type == 'folder' or type == 'image':
            return MediaTypes.IMAGES
        elif type == 'console':
            return ConsoleTypes.CONSOLE
        elif type == 'gui':
            return ConsoleTypes.GUI
        else:
            raise ValueError(type + " is not supported datasource type")
