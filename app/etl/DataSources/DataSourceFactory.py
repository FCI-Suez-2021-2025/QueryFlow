
from app.etl.DataSources.Database.Database import Database
from app.etl.DataSources.Database.DataTypes import DatabaseType
from app.etl.DataSources.Flatfile.FlatfileTypes import EFlatfile
from app.etl.DataSources.Flatfile.Flatfile import Flatfile
from app.etl.DataSources.Media.MediaTypes import EMedia
from app.etl.DataSources.IDataSource import IDataSource
from app.etl.DataSources.Media.Media import Media
from app.etl.DataSources.Console.Console import Console
from app.etl.DataSources.Console.EConsole import EConsoleTypes


class DataSourceFactory():

    def factory(cls, data_source):
        T = data_source.split(':')[0]
        if (T == 'mssql'):
            return  Database(DatabaseType.MSSQL, data_source)
        elif (T == 'sqllite'):
            return  Database(DatabaseType.SQLLITE, data_source)
        elif (T == 'json'):
            return  Flatfile(EFlatfile.JSON, )
        elif (T == 'html'):
            return  Flatfile(EFlatfile.HTML)
        elif (T == 'csv'):
            return Flatfile(EFlatfile.CSV)
        elif (T == 'xml'):
            return Flatfile(EFlatfile.XML)
        elif (T == 'excel'):
            return Flatfile(EFlatfile.EXCEL)
        elif (T == 'video'):
            return Media(EMedia.VIDEO)
        elif (T == 'folder'):
            return Media (EMedia.Folder)
        elif (T == 'img'):
            return  Media(EMedia.IMAGE)
        elif (T == 'stdout'):
            return Console(EConsoleTypes.STDOUT)
        elif(T == 'custom'):
            return Console(EConsoleTypes.CUSTOM)

        else:
            raise ValueError(T + " is not supported datasource type")