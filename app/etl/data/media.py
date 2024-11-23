from abc import ABC
from enum import Enum
from typing import Any

from pandas import DataFrame

from app.cv.operation_main import get_details
from app.cv.threading_main import read_and_detect
from app.etl.data.base_data_types import FieldPathBase, IExtractor


class MediaTypes(Enum):
    """Media Types"""

    IMAGES = "images"
    VIDEO = "video"


class IMedia(FieldPathBase, IExtractor, ABC):
    def __init__(self, path: str):
        FieldPathBase.__init__(self, path)


class BirdImagesMedia(IMedia):
    def __init__(self, path: str):
        IMedia.__init__(self, path)

    def extract(self) -> DataFrame:
        return DataFrame(get_details(self.path))


class VideoMaximumBirdsInFrameMedia(IMedia):
    def __init__(self, path: str):
        IMedia.__init__(self, path)

    def extract(self) -> DataFrame:
        data_dictionary: dict[Any, Any] = read_and_detect(self.path)
        #! DataFrame(data_dictionary, index=[0]) will work fine only if the dictionary keys and values are scaler
        return DataFrame(data_dictionary, index=[0])
