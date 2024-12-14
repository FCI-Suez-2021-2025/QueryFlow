import itertools
from typing import Any, Callable, Tuple
import pandas as pd
from app.etl.data.data_factories import (
    LoaderDataFactory,
    ExtractorDataFactory,
)
from app.etl.data.base_data_types import IExtractor, ILoader
from app.etl.helpers import (
    apply_filtering,
    apply_groupby,
    check_if_column_names_is_in_group_by,
    convert_select_column_indices_to_name,
    generate_aggregation_row,
    get_unique,
    group_by_columns_names,
)


transformed_data = None


def extract(data_source_type: str, data_source_path: str) -> pd.DataFrame:
    data_extractor: IExtractor = ExtractorDataFactory.create(
        data_source_type, data_source_path
    )
    data: pd.DataFrame = data_extractor.extract()
    return data


def transform_select(data: pd.DataFrame, criteria: dict) -> pd.DataFrame:

    # filtering
    if criteria["FILTER"]:
        data = apply_filtering(data, criteria["FILTER"])
    if not criteria["GROUP"]:
        # ordering
        if criteria["ORDER"]:
            tuple_order = criteria["ORDER"]
            column: str = tuple_order[0]
            sorting_way: str = tuple_order[1]

            # to handle if the column is passed by number not buy name
            if column.startswith("[") and column.endswith("]"):
                column_number = int(column[1:-1])
                column = data.columns[column_number]
            data = data.sort_values(column, ascending=sorting_way == "asc")
    if criteria["GROUP"]:
        groupby_columns = get_unique(group_by_columns_names(data, criteria["GROUP"]))
        select_columns = convert_select_column_indices_to_name(
            data, criteria["COLUMNS"]
        )
        if not check_if_column_names_is_in_group_by(select_columns, groupby_columns):
            raise Exception("there are is a column isn't in groupby columns")
        data = apply_groupby(data, select_columns, groupby_columns)
        print(data)
    else:
        if criteria["COLUMNS"] != "__all__":
            columns: list[str | Tuple] = criteria["COLUMNS"]
            is_column_number: Callable[[str], bool] = lambda x: x.startswith(
                "["
            ) and x.endswith("]")
            # if all the select columns are aggregation functions
            if all(type(item) == tuple for item in columns):
                # list of tuples each tuple is (aggregation,colum name)
                aggregate_columns: list[Tuple[str | Any]] = [
                    (
                        (tuple[0], data.columns[int(tuple[1][1:-1])])
                        if is_column_number(tuple[1])
                        else tuple
                    )
                    for tuple in columns
                ]

                data = generate_aggregation_row(data, aggregate_columns)

            else:  # assuming that select columns don't contain any aggregate
                column_names = [
                    (
                        data.columns[int(column[1:-1])]
                        if is_column_number(column)
                        else column
                    )
                    for column in columns
                ]

                # Select columns
                data = data[column_names]
    # distinct
    if criteria["DISTINCT"]:
        data = data.drop_duplicates()

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
