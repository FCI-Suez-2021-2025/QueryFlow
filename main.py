from app import *
from app.etl.controllers import *
from app.gui.ui import SQLCompilerApp

# for testing the program without ui
if __name__ == "__main__":
    app = SQLCompilerApp()
    app.mainloop()


#     query = r"""
# Select hotel,
#        [lead time],
#        [3] into {csv:transformed data.csv}
# FROM {csv:testing_datasets/hotel_bookings.csv}
# Where hotel ==hotel aNd Not [2]==[3] ;"""
#     compilation_result = compile_to_python(query)
#     if type(compilation_result) == Success:

#         python_code = compilation_result.unwrap()
#         execution_result = execute_python_code(python_code)
#         if type(execution_result) == Success:
#             print(execution_result.unwrap())

#         else:
#             print(execution_result.unwrap_error())

#     # to print failure string value
#     else:
#         print(compilation_result.unwrap_error())
