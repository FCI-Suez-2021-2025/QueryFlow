from app.compiler import parser
from returns.result import Success, Failure
from typing import Union
import traceback
from pandas import DataFrame


def compile_to_python(query: str) -> Union[Success[str], Failure[str]]:
    """
    Compiles a SQL-like query string into corresponding Python code or returns an error string if it fails to parse the query.

    Args:
          query (str): The SQL-like query to be compiled. For example:
            - A successful query: "SELECT * FROM [csv:data/players.csv] WHERE age > 30;"
            - A query with an error: "SELECT * FROM WHERE age > 30"
    Returns:
        Union[Success[str], Failure[str]]: A `Success` monad containing the compiled Python code if parsing is successful,
                                           or a `Failure` monad containing the error string if parsing fails.
    """
    try:
        # Assuming parser.parse() is some parsing logic for the SQL-like query
        return Success(str(parser.parse(query)))  # type: ignore
    except Exception:
        # Return a Failure monad containing the stack trace in case of an error
        return Failure(traceback.format_exc())


def execute_python_code(python_code: str) -> Union[Success[DataFrame], Failure[str]]:
    """
    Executes the given Python code and returns the resulting transformed data as a `DataFrame`,
    or an error message in case of failure.

    Args:
        python_code (str): The Python code to be executed as a string. The code should perform
                           transformations on data that result in a variable named `transformed_data`
                           being created, which will be returned as a `DataFrame` on success.
                           Example of `python_code` argument value:

                           **Example 1**
                           ```python
                            from app import etl

                            extracted_data= etl.extract('csv','data_sets/hotel_bookings.csv')
                            transformed_data = etl.transform(
                            extracted_data,
                            {
                                    'COLUMNS':  '__all__',
                                    'DISTINCT': False,
                                    'FILTER':   None,
                                    'ORDER':    None,
                                    'LIMIT_OR_TAIL':    ('limit', 10),
                                }
                            )
                           ```

                           **Example 2**

                           ```python
                            from app import etl
                            extracted_data = etl.extract("csv", "data_sets/hotel_bookings.csv")
                            transformed_data = etl.transform(
                                extracted_data,
                                {
                                    "COLUMNS": "__all__",
                                    "DISTINCT": False,
                                    "FILTER": {"type": "==", "left": "hotel", "right": "City Hotel"},
                                    "ORDER": ("arrival_date_year", "ASC"),
                                    "LIMIT_OR_TAIL": ("limit", 10),
                                },
                            )
                           ```

                           **Example 3**

                           ```python
                            from app import etl
                            extracted_data = etl.extract('csv','data_sets/hotel_bookings.csv')
                            transformed_data = etl.transform(
                            extracted_data,
                            {
                                    'COLUMNS':  [0, 1, 2],
                                    'DISTINCT': False,
                                    'FILTER':   None,
                                    'ORDER':    None,
                                    'LIMIT_OR_TAIL':    None,
                                }
                            )
                            etl.load(transformed_data,'csv','e.csv')
                           ```
    Returns:
        Union[Success[DataFrame], Failure[str]]:
            - A `Success` monad containing a `DataFrame` of the transformed data if the code executes successfully.
            - A `Failure` monad containing a string with the error message and stack trace if execution fails.
    """
    try:
        exec(python_code)
        from app.etl.core import transformed_data

        return Success(transformed_data)

    except Exception:
        return Failure(traceback.format_exc())
