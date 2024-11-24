from app import *
from app.etl.controllers import *

# for testing the program wihtout ui
if __name__ == "__main__":
    query = "select * from [csv:E:/College/Year 4/Term 1/CS461 Intelligent Systems - Dr.Ahmed Elshewey/Section Assignments/03- Team_09_Ensemble_Models_Boosting/hotel_bookings.csv];"
    compilation_result = compile_to_python(query)
    if type(compilation_result) == Success:
        python_code = compilation_result.unwrap()
        execution_result = execute_python_code(python_code)
        if type(execution_result) == Success:
            print(execution_result.unwrap())
        else:
            print(execution_result.unwrap())
    # to print failure string value
    else:
        print(compilation_result.unwrap())
