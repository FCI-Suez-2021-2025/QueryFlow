from app import *
from app.etl.controllers import *

# for testing the program wihtout ui
if __name__ == "__main__":

    query = (
        "select arrival_date_month from [csv:testing_datasets/hotel_bookings.csv] "
        " order by arrival_date_month asc"
        ";"
    )
    compilation_result = compile_to_python(query)
    if type(compilation_result) == Success:
        python_code = compilation_result.unwrap()
        execution_result = execute_python_code(python_code)
        if type(execution_result) == Success:
            print(execution_result.unwrap())
        else:
            print(execution_result.unwrap_error())

    # to print failure string value
    else:
        print(compilation_result.unwrap_error())
