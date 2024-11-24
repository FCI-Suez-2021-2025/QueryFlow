from enum import Enum
from pandas import DataFrame
from app.etl.data.local.base_data_types import IExtractor, FieldPathBase
from app.etl.data.remote.gee.google_earth_api_data_collector import (
    GoogleEarthAPIDataCollector,
)


class RemoteDataTypes(Enum):
    """Remote Types"""

    GEE = "gee"


class GEEDataExtractor(FieldPathBase, IExtractor):
    def __init__(self, path: str):
        FieldPathBase.__init__(self, path)
        self.path_parts = path.split("|")
        self.gee_api_collector = GoogleEarthAPIDataCollector(self.path_parts[0])

    def extract(self) -> DataFrame:
        return self.gee_api_collector.collect(
            self.path_parts[1],
            self.path_parts[2],
            float(self.path_parts[3]),
            float(self.path_parts[4]),
            float(self.path_parts[5]),
        )
