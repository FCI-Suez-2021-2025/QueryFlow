class IDataSource:
    def __init__(self, type) -> None:
        self.type = type

    def extract(self, path: str):
        pass

    def load(self, path: str):
        pass