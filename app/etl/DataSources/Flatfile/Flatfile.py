from app.etl.DataSources.IDataSource import IDataSource
from app.etl.DataSources.Flatfile.FlatfileTypes import EFlatfile
import pandas as pd

# Eflatfile.HTML
class Flatfile(IDataSource):
    def __init__(self, type: EFlatfile) -> None:
        super().__init__(type)
        self.extractCallbacks = {
            EFlatfile.HTML: (lambda path: pd.read_html(path)),
            EFlatfile.JSON: (lambda path: pd.read_json(path)),
            EFlatfile.XML: (lambda path: pd.read_xml(path)),
            EFlatfile.CSV: (lambda path: pd.read_csv(path)),
            EFlatfile.EXCEL: (lambda path: pd.read_excel(path))
        }
        self.loadCallbacks = {
            EFlatfile.HTML: (lambda data, path: data.to_html(path)),
            EFlatfile.JSON: (lambda data, path: data.to_json(path)),
            EFlatfile.XML: (lambda data, path: data.to_xml(path)),
            EFlatfile.CSV: (lambda data, path: data.to_csv(path,index=False)),
            EFlatfile.EXCEL: (lambda data, path: data.to_excel(path))
        }

    def load(self, data, file_path):
        self.loadCallbacks[self.type](data, file_path)

    def extract(self, file_path):
        return self.extractCallbacks[self.type](file_path)
