from pandas import DataFrame
from abc import ABC, abstractmethod


class FieldPathBase:
    def __init__(self, path: str):
        self.path = path


class IExtractor(ABC):
    @abstractmethod
    def extract(self) -> DataFrame:
        pass


class ILoader(ABC):
    @abstractmethod
    def load(self, data: DataFrame) -> None:
        pass
