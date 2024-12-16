from typing import Any, Callable, Tuple
import pandas as pd
from app.compiler.ast_nodes import *
from app.etl.data.data_factories import (
    LoaderDataFactory,
    ExtractorDataFactory,
)
from app.etl.data.base_data_types import IExtractor, ILoader
from app.etl.helpers import (
    apply_filtering,
    apply_groupby,
    apply_groupby_with_order,
    check_if_column_names_is_in_group_by,
    convert_select_column_indices_to_name,
    generate_aggregation_row,
    get_unique,
    group_by_columns_names,
    apply_order_by_without_groupby,
)


transformed_data = None


def extract(data_source_type: str, data_source_path: str) -> pd.DataFrame:
    data_extractor: IExtractor = ExtractorDataFactory.create(
        data_source_type, data_source_path
    )
    data: pd.DataFrame = data_extractor.extract()
    return data


def transform_select(data: pd.DataFrame, criteria: dict) -> pd.DataFrame:
    are_select_columns_aggregation = False
    if criteria["COLUMNS"] != "__all__":
        are_select_columns_aggregation = all(
            type(item) == tuple for item in criteria["COLUMNS"]
        )
    # filtering
    if criteria["FILTER"]:
        data = apply_filtering(data, criteria["FILTER"])

    if (
        not criteria["GROUP"]
        and criteria["ORDER"]
        and not are_select_columns_aggregation
    ):
        order_by_node: OrderByNode = criteria["ORDER"]
        data = apply_order_by_without_groupby(data, order_by_node)

    if criteria["GROUP"]:
        groupby_columns = get_unique(group_by_columns_names(data, criteria["GROUP"]))
        select_columns = convert_select_column_indices_to_name(
            data, criteria["COLUMNS"]
        )
        if not check_if_column_names_is_in_group_by(select_columns, groupby_columns):
            raise Exception("there are is a column isn't in groupby columns")
        if criteria["ORDER"]:
            order_by_node: OrderByNode = criteria["ORDER"]
            data = apply_groupby_with_order(
                data, select_columns, groupby_columns, order_by_node
            )
        else:
            data = apply_groupby(data, select_columns, groupby_columns)

    else:
        if criteria["COLUMNS"] != "__all__":
            columns: list[str | Tuple] = criteria["COLUMNS"]
            is_column_number: Callable[[str], bool] = lambda x: x.startswith(
                "["
            ) and x.endswith("]")
            # if all the select columns are aggregation functions

            if are_select_columns_aggregation:
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

            else:
                if any(type(column) == tuple for column in columns):
                    raise Exception(
                        "there are aggregation columns in select you should use group by"
                    )
                # assuming that select columns don't contain any aggregate
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
