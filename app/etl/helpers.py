import pandas as pd
import re
from typing import Any, Tuple


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
    # region get the value in the right operand and check if it is a int or float or string or its a column passed by name or number
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
    elif operator == "!=":
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
