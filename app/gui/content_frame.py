import sqlparse
from typing import Any, Tuple
import customtkinter as ctk
import pandas as pd
from pandas import DataFrame

from app.core.result_monad import Success
from app.etl.controllers import compile_to_python, execute_python_code
from app.gui.sql_textbox_colorizer import Colorizer


class TabContent(ctk.CTkFrame):
    def __init__(
        self,
        master: Any,
        width: int = 200,
        height: int = 200,
        corner_radius: int | str | None = None,
        border_width: int | str | None = None,
        bg_color: str | Tuple[str] = "transparent",
        fg_color: str | Tuple[str] | None = None,
        border_color: str | Tuple[str] | None = None,
        background_corner_colors: Tuple[str | Tuple[str]] | None = None,
        overwrite_preferred_drawing_method: str | None = None,
        **kwargs,
    ):
        super().__init__(
            master,
            width,
            height,
            corner_radius,
            border_width,
            bg_color,
            fg_color,
            border_color,
            background_corner_colors,
            overwrite_preferred_drawing_method,
            **kwargs,
        )
        self.add_children_widget()
        self.add_python_result_frame()
        self.add_data_frame_result_frame()

    def add_children_widget(self):
        self.sql_textbox = ctk.CTkTextbox(
            self, height=300, fg_color=("#ffffff", "#1e1e1e"), font=("Consolas", 24)
        )
        self.sql_textbox.bind(
            "<KeyRelease>",
            lambda _: Colorizer.highlight_syntax(
                self.sql_textbox, ctk.get_appearance_mode().lower()
            ),
        )
        # Button Frame (for Execute, Run, Delete, Up, Down buttons)
        self.btn_frame = ctk.CTkFrame(self, height=40, fg_color="transparent")
        # Execute Button
        self.execute_btn = ctk.CTkButton(
            self.btn_frame,
            text="Execute",
            command=self.execute_sql,
            width=80,
            fg_color="#51ab46",
            hover_color="#387731",
        )
        # Run Button
        self.run_btn = ctk.CTkButton(
            self.btn_frame,
            text="Compile",
            command=self.compile_sql,
            width=80,
        )
        self.result_frame = ctk.CTkFrame(self)

        self.sql_textbox.pack(fill="x", padx=10, pady=5)
        self.btn_frame.pack(fill="x", pady=5, padx=10)
        self.execute_btn.pack(side="left", padx=5)
        self.run_btn.pack(side="left", padx=5)
        self.result_frame.pack(fill="both", expand=True, pady=5, padx=10)
        self.result_frame.pack_propagate(False)

    def add_python_result_frame(self):
        # Create a new result section if it doesn't exist

        self.python_result_frame = ctk.CTkFrame(self.result_frame)

        self.python_code_label = ctk.CTkLabel(
            self.python_result_frame, text="Python Code", font=("Arial", 12, "bold")
        )
        self.python_code_textbox = ctk.CTkTextbox(
            self.python_result_frame, state="disabled"
        )
        # Add "Copy to Clipboard" button
        self.python_copy_button = ctk.CTkButton(
            self.python_result_frame,
            text="Copy to Clipboard",
            command=lambda: self.copy_to_clipboard(
                self.python_code_textbox.get("1.0", "end-1c").strip()
            ),
        )
        self.python_result_frame.pack(side="left", fill="both", expand=True, padx=5)
        self.python_code_label.pack(pady=5)
        self.python_code_textbox.pack(fill="both", expand=True, padx=5)
        self.python_copy_button.pack(pady=5)

    def add_data_frame_result_frame(self):
        # Right side: DataFrame
        self.data_frame_result_frame = ctk.CTkFrame(self.result_frame)
        self.data_frame_label = ctk.CTkLabel(
            self.data_frame_result_frame, text="DataFrame", font=("Arial", 12, "bold")
        )
        self.data_frame_textbox = ctk.CTkTextbox(self.data_frame_result_frame)
        # Add "Show Visualization" button
        self.visualize_button = ctk.CTkButton(
            self.data_frame_result_frame,
            text="Show Visualization",
            command=None,  # No functionality yet
            width=150,
        )
        self.data_frame_textbox.configure(state="disabled")  # Make read-only
        self.data_frame_result_frame.pack(
            side="right", fill="both", expand=True, padx=5
        )
        self.data_frame_label.pack(pady=5)
        self.data_frame_textbox.pack(fill="both", expand=True, padx=5)
        self.visualize_button.pack(pady=5)

    def execute_sql(self):
        """
        Handles the execution of SQL code entered in the SQL cell.
        - Converts SQL code to Python code using `compile_to_python`.
        - Executes Python code to generate the DataFrame.
        - Displays results or errors in their respective sections.
        """
        # Fetch SQL code from the text box
        sql_query = self.sql_textbox.get("1.0", "end-1c").strip()
        sql_query = sqlparse.format(sql_query, reindent=True, strip_whitespace=True)
        # Delete all content
        self.sql_textbox.delete("1.0", "end")
        # Insert text at the beginning (index "1.0")
        self.sql_textbox.insert("1.0", sql_query)
        Colorizer.highlight_syntax(self.sql_textbox, ctk.get_appearance_mode().lower())
        if not sql_query:
            self.display_result("SQL code is empty.", DataFrame())
            return

        # Step 1: Compile SQL code to Python
        compilation_result = compile_to_python(sql_query)

        if isinstance(compilation_result, Success):
            python_code = compilation_result.unwrap()

            # Step 2: Execute Python code
            execution_result = execute_python_code(python_code)

            if isinstance(execution_result, Success):
                # Execution succeeded; display Python code and DataFrame results
                data_frame = execution_result.unwrap()
                self.display_result(python_code, data_frame)
            else:
                # Execution failed; display Python code and error in DataFrame section
                execution_error = execution_result.unwrap_error()
                error_message = f"Python Execution Error:\n{execution_error.message}\nTraceback:\n{execution_error.code}"
                self.display_result(
                    python_code, pd.DataFrame({"Error": [error_message]})
                )
        else:
            # Compilation failed; display error in the Python Code section
            compilation_error = compilation_result.unwrap_error()
            error_message = f"SQL Compilation Error:\n{compilation_error}"
            self.display_result(error_message, pd.DataFrame())

    def compile_sql(self):
        # Fetch SQL code from the text box
        sql_query = self.sql_textbox.get("1.0", "end-1c").strip()
        sql_query = sqlparse.format(sql_query, reindent=True, strip_whitespace=True)
        # Delete all content
        self.sql_textbox.delete("1.0", "end")
        # Insert text at the beginning (index "1.0")
        self.sql_textbox.insert("1.0", sql_query)
        Colorizer.highlight_syntax(self.sql_textbox, ctk.get_appearance_mode().lower())
        if not sql_query:
            self.display_result("SQL code is empty.", DataFrame())
            return

        # Step 1: Compile SQL code to Python
        compilation_result = compile_to_python(sql_query)

        if isinstance(compilation_result, Success):
            python_code = compilation_result.unwrap()
            self.display_result(python_code, pd.DataFrame())
        else:
            # Compilation failed; display error in the Python Code section
            compilation_error = compilation_result.unwrap_error()
            error_message = f"SQL Compilation Error:\n{compilation_error}"
            self.display_result(error_message, pd.DataFrame())

    def display_result(self, python_code: str, data_frame: DataFrame) -> None:
        """
        Displays the Python code and DataFrame results (or errors) in the result section.
        """

        # Update Python code
        self.python_code_textbox.configure(state="normal")
        self.python_code_textbox.delete("1.0", "end")
        self.python_code_textbox.insert("1.0", python_code)
        # self.python_code_textbox.configure(state="disabled")

        # Update DataFrame (or error)
        self.data_frame_textbox.configure(state="normal")
        self.data_frame_textbox.delete("1.0", "end")
        if not data_frame.empty:
            self.data_frame_textbox.insert("1.0", data_frame.to_string(index=False))
        else:
            self.data_frame_textbox.insert("1.0", "No results to display.")
            # self.data_frame_textbox.configure(state="disabled")

    def copy_to_clipboard(self, text: str):
        # Copy the provided text to the clipboard
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()
