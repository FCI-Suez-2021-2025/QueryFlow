import pandas as pd
from app.etl.data_factories import (
    LoaderDataFactory,
    ExtractorDataFactory,
)
from app.etl.data.local.base_data_types import IExtractor, ILoader
from app.etl.helpers import apply_filtering


transformed_data = None


def extract(data_source_type: str, data_source_path: str) -> pd.DataFrame:
    data_extractor: IExtractor = ExtractorDataFactory.create(
        data_source_type, data_source_path
    )
    data: pd.DataFrame = data_extractor.extract()
    return data


def transform(data: pd.DataFrame, criteria: dict) -> pd.DataFrame:
    print("step over")
    # filtering
    if criteria["FILTER"]:
        data = apply_filtering(data, criteria["FILTER"])

    # columns
    if criteria["COLUMNS"] != "__all__":
        # data = data.filter(items=criteria["COLUMNS"])

        # Separate column names and numbers
        column_names = [col for col in criteria["COLUMNS"] if isinstance(col, str)]
        column_numbers = [col for col in criteria["COLUMNS"] if isinstance(col, int)]

        # Select columns
        data = pd.concat([data[column_names], data.iloc[:, column_numbers]], axis=1)
    # distinct
    if criteria["DISTINCT"]:
        data = data.drop_duplicates()

    # ordering
    if criteria["ORDER"]:
        column = criteria["ORDER"][0]
        data = data.sort_values(column, ascending=criteria["ORDER"][1] == "ASC")

    # limit
    if criteria["LIMIT_OR_TAIL"] != None:
        operator, number = criteria["LIMIT_OR_TAIL"]
        if number == 0:
            # empty data frame
            data = pd.DataFrame(columns=data.columns)
        elif operator == "limit":
            data = data[:number]
        else:
            data = data[-number:]

    global transformed_data
    transformed_data = data
    return data


def load(data: pd.DataFrame, source_type: str, data_destination: str):
    data_loader: ILoader = LoaderDataFactory.create(source_type, data_destination)
    data_loader.load(data)
