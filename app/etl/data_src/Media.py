from enum import Enum

from app.cv.OperationMain import getDetails
from app.cv.ThreadingMain import readAndDetect
from app.etl.data_src.IDataTypes import IDataTypes


class MediaTypes(Enum):
    """Media Types"""
    IMAGES = "images"
    VIDEO = "video"

class Media(IDataTypes):
    """Media"""
    def __init__(self,type):
        self.type = type
    def extract(self,path):
        if self.type == MediaTypes.VIDEO:
            # getPose() => read frames,perform the model on those frames to dict
            res = readAndDetect(path)
            return res
        elif self.type == MediaTypes.IMAGES:
            # getDetails(folderPath) => loop each file transform name to dict
            data = getDetails(path)
            return data
    def load(self,data,path):
        #has no load
        pass
