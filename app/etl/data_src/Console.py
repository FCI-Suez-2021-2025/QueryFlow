from app.etl.data_src.IDataTypes import IDataTypes

from enum import Enum


class ConsoleTypes(Enum):
    CONSOLE = 'console'
    GUI = 'gui'


class Console(IDataTypes):
    def __init__(self, type) -> None:
        self.type = type

    def extract(self):
        raise NotImplementedError('Extract method not implemented for console')

    def load(self, data, file_path):
        if self.type == ConsoleTypes.CONSOLE:
            print(data)
        elif self.type == ConsoleTypes.GUI:
            return data