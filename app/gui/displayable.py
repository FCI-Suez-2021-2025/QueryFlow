from abc import ABC, abstractmethod
import pandas as pd
from enum import Enum


class DisplayableTypes(Enum):
    CONSOLE = "console"
    GUI = "gui"


class IDisplayable(ABC):
    @abstractmethod
    def display(self, data: pd.DataFrame):
        pass


class ConsoleDisplayable:
    def display(self, data: pd.DataFrame) -> None:
        print(data)


class Displayable:
    def display(self, data: pd.DataFrame) -> None:
        pass
