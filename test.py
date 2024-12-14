from typing import Tuple
import pandas as pd


def get_scaler_aggregate(df: pd.DataFrame, aggregate: str, column: str):
    if aggregate == "sum":
        return df[column].sum()
    elif aggregate == "count":
        return df[column].shape[0]
    elif aggregate == "first":
        return df[column].iloc[0]
    elif aggregate == "last":
        return df[column].iloc[-1]
    elif aggregate == "mean":
        return df[column].mean()
    elif aggregate == "median":
        return df[column].median()
    elif aggregate == "min":
        return df[column].min()
    elif aggregate == "max":
        return df[column].max()
    elif aggregate == "std":
        return df[column].std()
    elif aggregate == "var":
        return df[column].var()
    elif aggregate == "prod":
        return df[column].prod()
    elif aggregate == "sem":
        return df[column].sem()
    elif aggregate == "describe":
        return df[column].describe()
    elif aggregate == "size":
        return df.shape[0]
    elif aggregate == "quantile":
        return df[column].quantile()
    elif aggregate == "nunique":
        return df[column].nunique()
    else:
        return None


# Sample DataFrame
data = {
    "size": [1, 2, 3, 4],
    "id": [10, 20, 30, 40],
    "profession": ["Engineer", "Doctor", "Teacher", "Artist"],
}
df = pd.DataFrame(data)

# Dynamic list of aggregation rules
aggregation_list = [
    ("size", "*"),
    ("sum", "id"),
    ("mean", "id"),
    ("sum", "id"),
]


# Dynamically build the aggregation dictionary
def generate_aggregation_row_new(
    df: pd.DataFrame, aggregation_list: list[Tuple[str, str]]
):
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


def generate_aggregation_row(df: pd.DataFrame, aggregation_list: list[Tuple[str, str]]):
    """
    Generates a single row DataFrame with aggregated values of the input DataFrame, based on the given aggregation rules.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame to be aggregated.
    aggregation_list : list[Tuple[str, str]]
        A list of tuples, where each tuple contains an aggregation function as a string, and a column name as a string.
        The aggregation function can be one of the following: "sum", "count", "first", "last", "mean", "median", "min", "max", "std", "var", "prod", "sem", "size", "quantile", "nunique".
        The column name can be any column name in the input DataFrame, or "*". If the column name is "*", the aggregation function is applied to all columns in the input DataFrame.

    Returns
    -------
    pd.DataFrame
        A single row DataFrame with the aggregated values of the input DataFrame, according to the given aggregation rules.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    >>> aggregation_list = [("sum", "A"), ("size", "*")]
    >>> result_df = generate_aggregation_row(df, aggregation_list)
    >>> result_df
       sum_A  size_rows
    0      6           3
    """

    agg_dict = {}
    for agg_func, column in aggregation_list:
        if column == "*":
            column = "rows"
        new_column_name = f"{agg_func}_{column}"
        column_value = get_scaler_aggregate(df, agg_func, column)
        # to handle duplicated aggregation column names
        if new_column_name not in agg_dict:
            agg_dict[new_column_name] = column_value
        else:
            i = 1
            name = new_column_name
            while name in agg_dict:
                name = f"{new_column_name}_{i}"
                i += 1
            agg_dict[name] = [column_value]

    # Aggregate the DataFrame
    result_df = pd.DataFrame(agg_dict, index=[0])
    return result_df


result_df = generate_aggregation_row_new(df, aggregation_list)

# Convert the result into a DataFrame with one row

print(result_df)
grouped_df = (
    df.groupby(["Department", "Location"])
    .agg(
        "ad":["min","max"]
    )
    .reset_index()
)
min(ad),min(x),max(ad)
"ad":["min","max"]
min(ad),max(ad),min(x)