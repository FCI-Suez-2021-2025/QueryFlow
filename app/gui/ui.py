import customtkinter as ctk
import pandas as pd  # For simulating data frames

# from app import *
from app.core.result_monad import Success
from app.etl.controllers import compile_to_python, execute_python_code


class SQLCompilerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SQL Compiler")
        self.geometry("900x600")
        self.cells = []  # Store cell widgets
        self.create_ui()

    def create_ui(self):
        # Top Control Buttons
        top_frame = ctk.CTkFrame(self, height=50)
        top_frame.pack(fill="x", pady=5, padx=10)

        # "ADD New Cell" Button
        add_cell_btn = ctk.CTkButton(
            top_frame, text="ADD New Cell", command=self.add_cell, width=150
        )
        add_cell_btn.pack(side="left", padx=10)

        # "Collapse All Cells" Button
        collapse_btn = ctk.CTkButton(
            top_frame, text="Collapse Cells", command=self.toggle_collapse, width=150
        )
        collapse_btn.pack(side="left", padx=10)

        # Dark Mode Toggle Button
        dark_mode_btn = ctk.CTkSwitch(
            top_frame, text="Dark Mode", command=self.toggle_dark_mode, width=150
        )
        dark_mode_btn.pack(side="left", padx=10)

        # Scaling dropdown
        scaling_label = ctk.CTkLabel(top_frame, text="Scaling:")
        scaling_label.pack(side="left", padx=(10, 5), pady=5)

        self.scaling_options = ["100%", "125%", "150%", "175%", "200%"]
        scaling_dropdown = ctk.CTkOptionMenu(
            top_frame, values=self.scaling_options, command=self.change_scaling
        )
        scaling_dropdown.set("100%")
        scaling_dropdown.pack(side="left", padx=5, pady=5)

        # Frame to Hold the SQL Cells
        self.cell_frame = ctk.CTkScrollableFrame(self)
        self.cell_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def toggle_dark_mode(self):
        # Toggle between Light and Dark Mode
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")

    def add_cell(self):
        # Create a new SQL cell
        cell = ctk.CTkFrame(self.cell_frame, corner_radius=10, height=200)
        cell.pack(fill="x", pady=5, padx=5)

        # Add label to notify the user about lowercase SQL keywords
        notification_label = ctk.CTkLabel(
            cell,
            text="SQL keywords should be written in lowercase.",
            font=("Arial", 10, "italic"),
        )
        notification_label.pack(side="top", anchor="w", padx=10, pady=5)

        # SQL Textbox for SQL Code
        sql_textbox = ctk.CTkTextbox(cell, height=100)
        sql_textbox.pack(fill="x", padx=10, pady=5)

        # Button Frame (for Execute, Run, Delete, Up, Down buttons)
        btn_frame = ctk.CTkFrame(cell, height=40)
        btn_frame.pack(fill="x", pady=5, padx=10)

        # Execute Button
        execute_btn = ctk.CTkButton(
            btn_frame,
            text="Execute",
            command=lambda: self.execute_sql(sql_textbox, cell),
            width=80,
            fg_color="green",
        )
        execute_btn.pack(side="left", padx=5)

        # Run Button
        run_btn = ctk.CTkButton(
            btn_frame,
            text="Compile",
            command=lambda: self.run_sql(sql_textbox, cell),
            width=80,
        )
        run_btn.pack(side="left", padx=5)

        # Delete Button with red background color
        delete_btn = ctk.CTkButton(
            btn_frame,
            text="X",
            command=lambda: self.delete_cell(cell),
            width=40,
            fg_color="red",
        )
        delete_btn.pack(side="left", padx=5)

        # Up Button with Arrow Icon
        up_btn = ctk.CTkButton(
            btn_frame, text="↑", command=lambda: self.move_cell(cell, -1), width=40
        )
        up_btn.pack(side="left", padx=5)

        # Down Button with Arrow Icon
        down_btn = ctk.CTkButton(
            btn_frame, text="↓", command=lambda: self.move_cell(cell, 1), width=40
        )
        down_btn.pack(side="left", padx=5)

        # Add cell to the list
        self.cells.append(cell)

    def move_cell(self, cell, direction):
        # Get current position of the cell
        idx = self.cells.index(cell)
        new_idx = idx + direction

        if 0 <= new_idx < len(self.cells):
            # Remove and reinsert at the new position
            self.cells.pop(idx)
            self.cells.insert(new_idx, cell)

            # Rearrange the order in the UI
            for widget in self.cell_frame.winfo_children():
                widget.pack_forget()
            for cell in self.cells:
                cell.pack(fill="x", pady=5, padx=5)

    def toggle_collapse(self):
        # Collapse or expand all cells
        for cell in self.cells:
            if cell.winfo_ismapped():
                cell.pack_forget()
            else:
                cell.pack(fill="x", pady=5, padx=5)

    def change_scaling(self, scaling):
        scale_map = {"100%": 1.0, "125%": 1.25, "150%": 1.5, "175%": 1.75, "200%": 2.0}
        scaling_factor = scale_map.get(scaling, 1.0)
        ctk.set_widget_scaling(scaling_factor)

    def execute_sql(self, sql_textbox, cell):
        """
        Handles the execution of SQL code entered in the SQL cell.
        - Converts SQL code to Python code using `compile_to_python`.
        - Executes Python code to generate the DataFrame.
        - Displays results or errors in their respective sections.
        """
        # Fetch SQL code from the text box
        sql_code = sql_textbox.get("1.0", "end-1c").strip()

        if not sql_code:
            self.display_result(cell, "SQL code is empty.", pd.DataFrame())
            return

        # Step 1: Compile SQL code to Python
        compilation_result = compile_to_python(sql_code)

        if isinstance(compilation_result, Success):
            python_code = compilation_result.unwrap()

            # Step 2: Execute Python code
            execution_result = execute_python_code(python_code)

            if isinstance(execution_result, Success):
                # Execution succeeded; display Python code and DataFrame results
                df = execution_result.unwrap()
                self.display_result(cell, python_code, df)
            else:
                # Execution failed; display Python code and error in DataFrame section
                execution_error = execution_result.unwrap_error()
                error_message = f"Python Execution Error:\n{execution_error.message}\nTraceback:\n{execution_error.code}"
                self.display_result(
                    cell, python_code, pd.DataFrame({"Error": [error_message]})
                )
        else:
            # Compilation failed; display error in the Python Code section
            compilation_error = compilation_result.unwrap_error()
            error_message = f"SQL Compilation Error:\n{str(compilation_error)}"
            self.display_result(cell, error_message, pd.DataFrame())

    def run_sql(self, sql_textbox, cell):
        # Get content from the SQL Textbox and assign it to the variable 'query'
        query = sql_textbox.get("1.0", "end-1c")
        print(f"Running SQL: {query}")  # Print the query for debugging

        # Simulate Python code only for compile
        python_code = (
            f"# Simulated Python code based on SQL: {query}\nprint('Running SQL code')"
        )

        # Pass an empty DataFrame to leave the DataFrame section empty
        df = pd.DataFrame()  # Empty DataFrame for compile

        self.display_result(cell, python_code, df)

    def display_result(self, cell, python_code, df):
        """
        Displays the Python code and DataFrame results (or errors) in the result section.
        """
        # Check if result section already exists
        if hasattr(cell, "result_section") and cell.result_section.winfo_ismapped():
            # Update existing result section
            left_frame = cell.result_section.winfo_children()[0]
            right_frame = cell.result_section.winfo_children()[1]

            # Update Python code
            left_frame.winfo_children()[1].configure(state="normal")
            left_frame.winfo_children()[1].delete("1.0", "end")
            left_frame.winfo_children()[1].insert("1.0", python_code)
            left_frame.winfo_children()[1].configure(state="disabled")

            # Update DataFrame (or error)
            right_frame.winfo_children()[1].configure(state="normal")
            right_frame.winfo_children()[1].delete("1.0", "end")
            if not df.empty:
                right_frame.winfo_children()[1].insert("1.0", df.to_string(index=False))
            else:
                right_frame.winfo_children()[1].insert("1.0", "No results to display.")
            right_frame.winfo_children()[1].configure(state="disabled")
        else:
            # Create a new result section if it doesn't exist
            result_section = ctk.CTkFrame(cell)
            result_section.pack(fill="x", pady=5, padx=10)
            cell.result_section = result_section

            # Left side: Python Code
            left_frame = ctk.CTkFrame(result_section)
            left_frame.pack(side="left", fill="both", expand=True, padx=5)

            python_code_label = ctk.CTkLabel(
                left_frame, text="Python Code", font=("Arial", 12, "bold")
            )
            python_code_label.pack(pady=5)

            python_code_textbox = ctk.CTkTextbox(left_frame, height=100)
            python_code_textbox.insert("1.0", python_code)
            python_code_textbox.configure(state="disabled")  # Make read-only
            python_code_textbox.pack(fill="both", padx=5)

            # Add "Copy to Clipboard" button
            copy_button = ctk.CTkButton(
                left_frame,
                text="Copy to Clipboard",
                command=lambda: self.copy_to_clipboard(python_code),
            )
            copy_button.pack(pady=5)

            # Right side: DataFrame
            right_frame = ctk.CTkFrame(result_section)
            right_frame.pack(side="right", fill="both", expand=True, padx=5)

            df_label = ctk.CTkLabel(
                right_frame, text="DataFrame", font=("Arial", 12, "bold")
            )
            df_label.pack(pady=5)

            df_textbox = ctk.CTkTextbox(right_frame, height=100)
            if not df.empty:
                df_textbox.insert("1.0", df.to_string(index=False))
            else:
                df_textbox.insert("1.0", "No results to display.")
            df_textbox.configure(state="disabled")  # Make read-only
            df_textbox.pack(fill="both", padx=5)

            # Add "Show Visualization" button
            show_vis_button = ctk.CTkButton(
                right_frame,
                text="Show Visualization",
                command=None,  # No functionality yet
                width=150,
            )
            show_vis_button.pack(pady=5)

    def copy_to_clipboard(self, text):
        # Copy the provided text to the clipboard
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()  # Ensure the clipboard is updated
        print("Python code copied to clipboard!")

    def delete_cell(self, cell):
        # Remove the selected cell from the UI and list
        if cell in self.cells:
            self.cells.remove(cell)
            cell.destroy()
            # Repack remaining cells
            for widget in self.cell_frame.winfo_children():
                widget.pack_forget()
            for cell in self.cells:
                cell.pack(fill="x", pady=5, padx=5)


# Run the application
if __name__ == "__main__":
    app = SQLCompilerApp()
    app.mainloop()
