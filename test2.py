from collections import defaultdict
import pandas as pd


def is_index(value: str) -> bool:
    if value.startswith("[") and value.endswith("]"):
        return True
    return False


def column_index_to_name(df: pd.DataFrame, index_expression: str) -> str:
    column_number = int(index_expression[1:-1])
    return df.columns[column_number]


# Sample DataFrame
data = {
    "Department": ["HR", "HR", "IT", "IT", "Finance", "Finance", "IT"],
    "firstname": ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace"],
    "lastname": ["Ali", "medo", "ghareeb", "hossam", "alharery", "mark", "belbes"],
    "Salary": [70000, 80000, 90000, 95000, 85000, 88000, 91000],
    "Bonus": [5000, 6000, 7000, 7500, 8000, 8500, 7200],
    "Location": [
        "New York",
        "New York",
        "San Francisco",
        "New York",
        "San Francisco",
        "New York",
        "San Francisco",
    ],
}

df = pd.DataFrame(data)


# print(df)
# Group by 'Department' and 'Location', aggregate 'Salary' and 'Bonus'
# grouped_df = (
#     df.groupby(["Department", "Location"])
#     .agg(
#         Total_Salary=("Salary", "min"),
#         var_Salary=("Salary", "var"),
#         std_Bonus=("Bonus", "std"),
#         Count_Employee=("Employee", "size"),
#     )
#     .reset_index()
# )
def get_unique(items: list) -> list:
    unique_list = []
    seen = set()

    for item in items:
        if item not in seen:
            unique_list.append(item)
            seen.add(item)
    return unique_list


dict = {}


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


# region converting columns indices to column names
# and check if a select column name is in groupby columns
def convert_select_column_indices_to_name(
    df: pd.DataFrame,
    select_columns: list[tuple[str | str] | str],
    groupby_columns: list,
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
            if column_name not in groupby_columns:

                raise Exception("column is not in groupby columns")
    return result_columns


groupby_columns = ["Location"]
select_columns = [
    ("last", "[0]"),
    ("first", "lastname"),
    ("max", "[1]"),
    ("size", "*"),
    "Location",
]
groupby_columns = get_unique(group_by_columns_names(df, groupby_columns))

select_columns = convert_select_column_indices_to_name(
    df, select_columns
)
print(select_columns)
# endregion
# current_value = dict.get(key, [])
# current_value.append(value)
# dict[key] = current_value
grouped_df = (
    df.groupby(groupby_columns).agg({"firstname": ["last", "last"]}).reset_index()
)
print(grouped_df)
# list_of_columns = []
# for column in grouped_df.columns:
#     if type(column) is tuple:
#         if column[1].strip():
#             list_of_columns.append("_".join(column).strip())
#         else:
#             list_of_columns.append(column[0])
#     else:
#         list_of_columns.append(column)

# grouped_df.columns = list_of_columns
# print("\n----------------- grouped data --------------------\n")
# print(grouped_df)
# # first,last,min,max,mean
# # new_name = f"{aggregation}_{str(col)}"
