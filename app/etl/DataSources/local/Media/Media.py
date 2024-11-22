
from app.etl.DataSources.local.IDataSource import IDataSource
from app.etl.Move_Bird.bird import BirdMoveDetect,birds
from app.etl.DataSources.local.Media.MediaTypes import EMedia

class Media(IDataSource):
    def __init__(self, type) -> None:
        super().__init__(type)

    def extract(self, file_path):
        if(self.type==EMedia.Folder):
            data =BirdMoveDetect().changes(file_path)
            return data
        if(self.type==EMedia.VIDEO):
            data=birds.count_birds(file_path)
            return data

    def load(self, file_path):
        print('not supported')
