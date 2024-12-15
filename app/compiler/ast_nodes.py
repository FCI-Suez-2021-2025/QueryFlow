from dataclasses import dataclass
from enum import Enum


class SortingWay(Enum):
    ASC = "asc"
    DESC = "desc"

    def __str__(self):
        return f"{self.__class__.__name__}.{self.name}"

    def __repr__(self):
        return str(self)


@dataclass
class ColumnNameNode:
    name: str


@dataclass
class ColumnIndexNode:
    index: int


@dataclass
class AggregationNode:
    function: str
    column: ColumnNameNode | ColumnIndexNode


@dataclass
class OrderByParameter:
    parameter: ColumnNameNode | ColumnIndexNode | AggregationNode
    way: SortingWay


@dataclass
class OrderByNode:
    parameters: list[OrderByParameter]
