from app.etl.DataSources.IDataSource import IDataSource
from app.etl.DataSources.Console.EConsole import EConsoleTypes
class Console(IDataSource):
    def __init__(self, type) -> None:
        super().__init__(type)

    def extract(self):
        raise NotImplementedError('Extract method not implemented for console')

    def load(self, data, file_path):
        if self.type == EConsoleTypes.STDOUT:
            print(data)
        elif self.type == EConsoleTypes.CUSTOM:
            return data