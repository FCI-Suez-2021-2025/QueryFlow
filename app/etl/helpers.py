import pandas as pd
import re
from typing import Any, Generic, Tuple, TypeVar

from app.compiler.ast_nodes import *


def column_index_to_column_name(
    data: pd.DataFrame, parameter: ColumnIndexNode
) -> ColumnNameNode:
    return ColumnNameNode(data.columns[parameter.index])


def apply_filtering(data: pd.DataFrame, filters_expressions_tree: dict) -> pd.DataFrame:
    # if it's a unary expression
    if len(filters_expressions_tree) == 2:
        operator: str = filters_expressions_tree["type"]
        operand: dict = filters_expressions_tree["operand"]
        if operator == "not":
            removed_data = apply_filtering(data, operand)
            return pd.concat([data, removed_data]).drop_duplicates(keep=False)
    operator: str = filters_expressions_tree["type"]
    if operator == "or" or operator == "and":
        # if it's a binary expression
        left_operand: dict = filters_expressions_tree["left"]
        right_operand: dict = filters_expressions_tree["right"]
        # data after applying left operand
        left = apply_filtering(data, left_operand)
        right = apply_filtering(data, right_operand)

        if operator == "or":
            data = pd.concat([left, right])
        else:
            data = pd.merge(left, right)
        return data[~data.index.duplicated(keep="first")]

    left_operand: str = filters_expressions_tree["left"]

    right_operand = filters_expressions_tree["right"]
    # region get the value in the right operand and check if it is an int or float or string or its a column passed by name or number
    if type(right_operand) == str:
        if right_operand.startswith('"') and right_operand.endswith('"'):
            right_operand: str = right_operand[1:-1]
        elif right_operand.startswith("[") and right_operand.endswith("]"):
            column_number = int(right_operand[1:-1])
            right_operand: pd.DataFrame = data[data.columns[column_number]]
        else:
            right_operand: pd.DataFrame = data[right_operand]
    # endregion
    # get the column in the left operand and check if its passed by name or number
    if left_operand.startswith("[") and left_operand.endswith("]"):
        column_number = int(left_operand[1:-1])
        left_operand = data[data.columns[column_number]]
    else:
        left_operand = data[left_operand]

    if operator == "like":
        return data[
            [True if re.match(right_operand, str(x)) else False for x in left_operand]
        ]

    if operator == ">":
        return data[left_operand > right_operand]
    if operator == ">=":
        return data[left_operand >= right_operand]
    elif operator == "<":
        return data[left_operand < right_operand]
    elif operator == "<=":
        return data[left_operand <= right_operand]
    elif operator == "==":
        return data[left_operand == right_operand]
    elif operator == "!=" or operator == "<>":
        return data[left_operand != right_operand]

    return data


def get_scaler_aggregate(df: pd.DataFrame, aggregate: str, column: str) -> Any:
    """
    Retrieves the aggregation result of a given column in a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    aggregate : str
        Aggregation function to use. Can be one of the following:
            'sum'
            'count'
            'first'
            'last'
            'mean'
            'median'
            'min'
            'max'
            'std'
            'var'
            'prod'
            'sem'
            'size'
            'quantile'
            'nunique'
    column : str
        Name of the column to aggregate.

    Returns
    -------
    Any
        Aggregation result.
    """
    if aggregate == "sum":
        # Sum of values
        return df[column].sum()
    elif aggregate == "count":
        # Count of non-null values
        return df[column].shape[0]
    elif aggregate == "first":
        # First value in the column
        return df[column].iloc[0]
    elif aggregate == "last":
        # Last value in the column
        return df[column].iloc[-1]
    elif aggregate == "mean":
        # Average (mean) of values
        return df[column].mean()
    elif aggregate == "median":
        # Median of values
        return df[column].median()
    elif aggregate == "min":
        # Minimum value
        return df[column].min()
    elif aggregate == "max":
        # Maximum value
        return df[column].max()
    elif aggregate == "std":
        # Standard deviation
        return df[column].std()
    elif aggregate == "var":
        # Variance of values
        return df[column].var()
    elif aggregate == "prod":
        # Product of values
        return df[column].prod()
    elif aggregate == "sem":
        # Standard error of the mean
        return df[column].sem()
    elif aggregate == "size":
        # Size of the DataFrame
        return df.shape[0]
    elif aggregate == "quantile":
        # Quantile (requires a parameter, e.g., q=0.25)
        return df[column].quantile()
    elif aggregate == "nunique":
        # Number of unique values
        return df[column].nunique()
    else:
        # Return None if the aggregate function is not supported
        return None


def generate_aggregation_row(df: pd.DataFrame, aggregation_list: list[Tuple[str, str]]):
    agg_dict = {}
    new_column_names: list[str] = [None] * len(aggregation_list)
    for index, item in enumerate(aggregation_list):
        agg_func, column = item
        if column == "*":
            column = "rows"
        new_column_name = f"{agg_func}_{column}"
        column_value = get_scaler_aggregate(df, agg_func, column)
        if new_column_name not in agg_dict:
            agg_dict[new_column_name] = column_value
        new_column_names[index] = new_column_name

    # Aggregated DataFrame with the unique columns
    unique_columns_df = pd.DataFrame(agg_dict, index=[0])
    return unique_columns_df[new_column_names]


def group_by_columns_names(
    df: pd.DataFrame, columns_expressions: list[str]
) -> list[str]:
    column_names = [None] * len(columns_expressions)
    for i in range(len(columns_expressions)):
        column_expression = columns_expressions[i]
        if is_index(column_expression):
            column_name = column_index_to_name(df, column_expression)
        else:
            column_name = column_expression
        column_names[i] = column_name
    return column_names


def is_index(value: str) -> bool:
    if value.startswith("[") and value.endswith("]"):
        return True
    return False


def column_index_to_name(df: pd.DataFrame, index_expression: str) -> str:
    column_number = int(index_expression[1:-1])
    return df.columns[column_number]


T = TypeVar("T")


def get_unique(items: list[T]) -> list[T]:
    unique_list = []
    seen = set()

    for item in items:
        if item not in seen:
            unique_list.append(item)
            seen.add(item)
    return unique_list


def convert_select_column_indices_to_name(
    df: pd.DataFrame,
    select_columns: list[tuple[str | str] | str],
) -> list[str | tuple[str, str]]:
    result_columns = [None] * len(select_columns)
    for index in range(len(select_columns)):
        item = select_columns[index]
        if type(item) == tuple:
            agg, column = item
            if is_index(column):
                column_name = column_index_to_name(df, column)
                result_columns[index] = (agg, column_name)
            else:
                column_name = column
                result_columns[index] = (agg, column_name)
        else:
            column = item
            if is_index(column):
                column_name = column_index_to_name(df, column)
                result_columns[index] = column_name
            else:
                column_name = column
                result_columns[index] = column_name
    return result_columns


def check_if_column_names_is_in_group_by(
    columns: list[str | tuple], groupby_columns: list[str]
) -> bool:
    columns_names = filter(lambda x: type(x) == str, columns)
    groupby_columns = set(groupby_columns)
    return all(column_name in groupby_columns for column_name in columns_names)


def apply_groupby(
    df: pd.DataFrame, select_columns: list[str | tuple], groupby_columns: list[str]
) -> pd.DataFrame:
    size_columns = []
    for i in range(len(select_columns)):
        c = select_columns[i]
        if type(c) == tuple:
            if c == ("size", "*"):
                size_columns.append((i, "size_rows"))
            elif c[0] == "size":
                size_columns.append((i, f"size_{c[1]}"))

    if size_columns:
        for item in size_columns:
            index: int = item[0]
            select_columns[index] = ("size", df.columns[0])

    new_column_names = list(
        map(lambda x: "_".join(x) if type(x) == tuple else x, select_columns)
    )

    dict = {}
    aggregation_columns = list(filter(lambda x: type(x) == tuple, select_columns))
    for agg_function, column in aggregation_columns:
        current_functions: list = dict.get(column, list())
        current_functions.append(agg_function)
        dict[column] = current_functions

    for column, agg_functions in dict.items():
        dict[column] = list(set(agg_functions))
    grouped_df = df.groupby(groupby_columns).agg(dict).reset_index()
    # region flatten columns
    list_of_columns = flatten_columns(grouped_df)
    grouped_df.columns = list_of_columns
    # endregion
    grouped_df = grouped_df[new_column_names]

    if size_columns:
        original_columns_names = new_column_names.copy()
        for i, column in size_columns:
            original_columns_names[i] = column
        grouped_df.columns = original_columns_names

    return grouped_df


def apply_groupby_with_order(
    df: pd.DataFrame,
    select_columns: list[str | tuple],
    groupby_columns: list[str],
    order_by_node: OrderByNode,
) -> pd.DataFrame:
    order_parameters = order_by_node.parameters
    test_set = set(groupby_columns)
    for order_parameter in order_parameters:
        if type(order_parameter.parameter) is ColumnIndexNode:
            order_parameter.parameter = column_index_to_column_name(
                df, order_parameter.parameter
            )
        elif (
            type(order_parameter.parameter) is AggregationNode
            and type(order_parameter.parameter.column) is ColumnIndexNode
        ):
            order_parameter.parameter.column = column_index_to_column_name(
                df, order_parameter.parameter.column
            )
        elif type(order_parameter.parameter) is ColumnNameNode:
            if order_parameter.parameter.name not in test_set:
                raise Exception(
                    f"column {order_parameter.parameter.name} is not in group by"
                )

    order_columns: list[str | tuple] = [None] * len(order_parameters)
    order_ways_boolean = [None] * len(order_parameters)
    for i, order_param in enumerate(order_parameters):
        if type(order_param.parameter) is ColumnNameNode:
            order_columns[i] = order_param.parameter.name
            order_ways_boolean[i] = order_param.way.value == "asc"
        elif type(order_param.parameter) is AggregationNode:
            order_columns[i] = (
                order_param.parameter.function,
                order_param.parameter.column.name,
            )
            order_ways_boolean[i] = order_param.way.value == "asc"

    if len(order_columns) != len(set(order_columns)):
        raise Exception("there are duplicate columns in order by")

    size_columns_order = []
    for i in range(len(order_columns)):
        c = order_columns[i]
        if type(c) == tuple:
            if c == ("size", "*"):
                size_columns_order.append((i, "size_rows"))
            elif c[0] == "size":
                size_columns_order.append((i, f"size_{c[1]}"))

    size_columns = []
    for i in range(len(select_columns)):
        c = select_columns[i]
        if type(c) == tuple:
            if c == ("size", "*"):
                size_columns.append((i, "size_rows"))
            elif c[0] == "size":
                size_columns.append((i, f"size_{c[1]}"))

    for item in size_columns:
        index: int = item[0]
        select_columns[index] = ("size", df.columns[0])

    for item in size_columns_order:
        index: int = item[0]
        order_columns[index] = ("size", df.columns[0])

    new_column_names = list(
        map(lambda x: "_".join(x) if type(x) == tuple else x, select_columns)
    )
    order_columns_names = list(
        map(lambda x: "_".join(x) if type(x) == tuple else x, order_columns)
    )

    dict = {}
    aggregation_columns = list(
        filter(lambda x: type(x) == tuple, select_columns + order_columns)
    )
    for agg_function, column in aggregation_columns:
        current_functions: list = dict.get(column, list())
        current_functions.append(agg_function)
        dict[column] = current_functions

    for column, agg_functions in dict.items():
        dict[column] = list(set(agg_functions))
    grouped_df: pd.DataFrame = df.groupby(groupby_columns).agg(dict).reset_index()

    # region flatten columns
    list_of_columns = flatten_columns(grouped_df)
    grouped_df.columns = list_of_columns
    # endregion
    grouped_df = grouped_df.sort_values(
        order_columns_names, ascending=order_ways_boolean
    )[new_column_names]

    if size_columns:
        original_columns_names = new_column_names.copy()
        for i, column in size_columns:
            original_columns_names[i] = column
        grouped_df.columns = original_columns_names

    return grouped_df


def flatten_columns(grouped_df) -> list:
    """
    This function takes in a grouped DataFrame and returns a list of
    flattened column names. The function works by iterating over the
    columns of the DataFrame and checking if the column is a tuple or
    not. If the column is a tuple, it is assumed to be a multi-level
    index and the function tries to flatten the column name by
    concatenating the aggregation function and the column name with
    an underscore. If the column is not a tuple, it is simply added to
    the list of flattened column names.

    Parameters
    ----------
    grouped_df : pd.DataFrame
        The grouped DataFrame to flatten the column names of.

    Returns
    -------
    list
        A list of flattened column names.
    """
    list_of_columns = []
    for column in grouped_df.columns:
        if type(column) is tuple:
            column_name: str = column[0]
            agg: str = column[1]
            if agg.strip():
                list_of_columns.append(f"{agg}_{column_name}")
            else:
                list_of_columns.append(column_name)
        else:
            list_of_columns.append(column)
    return list_of_columns


def apply_order_by_without_groupby(data: pd.DataFrame, order_by_node: OrderByNode):
    order_parameters: list[OrderByParameter] = order_by_node.parameters
    if any(
        type(order_parameter.parameter) is AggregationNode
        for order_parameter in order_parameters
    ):
        raise Exception(
            "there are aggregation columns in order by you should use group by"
        )
    for order_parameter in order_parameters:
        if type(order_parameter.parameter) is ColumnIndexNode:
            order_parameter.parameter = column_index_to_column_name(
                data, order_parameter.parameter
            )

    order_columns = [order_param.parameter.name for order_param in order_parameters]
    order_ways_boolean = [
        order_param.way.value == "asc" for order_param in order_parameters
    ]
    if len(order_columns) != len(set(order_columns)):
        raise Exception("there are duplicate columns in order by")
    data = data.sort_values(order_columns, ascending=order_ways_boolean)
    return data


# def __get_source_type(data_source:str) -> str:
#     if data_source == 'CONSOLE':
#         return 'CONSOL'
#     elif re.search(r'.*\.csv(\.zip)?', data_source):
#         return 'CSV'
#     elif re.search(r'.*\.db/\w+', data_source):
#         return 'SQLITE'
#     elif re.search(r'Data Source.*', data_source):
#         return 'MSSQL'
#     elif re.search(r'.*\.html', data_source):
#         return 'HTML'
#     elif re.search(r'.*\.json', data_source):
#         return 'JSON'
#     elif re.search(r'.*\.xml', data_source):
#         return 'XML'
#     elif re.search( r'(.+\.xlsx)| (.+\.xls) | (.+\.xlsm)| (.+\.xlsb)| (.+\.odf)| (.+\.ods)| (.+\.odt)', data_source):
#         return 'EXCEL'
