import customtkinter as ctk
import seaborn as sns

from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame

from app.gui.results_frame.table_result_frame.multi_selection_dropdown import (
    MultiSelectionDropDown,
)


class DataVisualizer:
    def __init__(self, master_widget, data_frame: DataFrame):
        self.master = master_widget
        self.data_frame = data_frame
        self.current_figure = {"fig": None, "canvas": None}
        self.create_visualization_window()

    def create_visualization_window(self):
        if self.data_frame is None or self.data_frame.empty:
            return

        # Create a new pop-up window
        self.popup = ctk.CTkToplevel(self.master)
        self.popup.title("Select Visualization Options")
        self.popup.geometry("600x700")
        self.popup.grab_set()

        # Create tabs for different graph types
        self.tabview = ctk.CTkTabview(self.popup)
        self.tabview.pack(expand=True, fill="both", padx=10, pady=5)

        # Create tabs
        self.tab1 = self.tabview.add("Scatter/Line/Bar Plots")
        self.tab2 = self.tabview.add("Count Plot")

        self.setup_standard_plots_tab()
        self.setup_count_plot_tab()
        self.setup_buttons()

    def setup_standard_plots_tab(self):
        # Frame for controls (Scatter/Line/Bar)
        self.control_frame = ctk.CTkFrame(self.tab1)
        self.control_frame.pack(fill="x", padx=10, pady=5)

        # Graph type selection
        graph_type_label = ctk.CTkLabel(self.control_frame, text="Select Graph Type:")
        graph_type_label.pack(pady=5)
        graph_type_options = ["Scatterplot", "Line", "Bar"]
        self.graph_type_var = ctk.StringVar(value=graph_type_options[0])
        self.graph_type_dropdown = ctk.CTkOptionMenu(
            self.control_frame, values=graph_type_options, variable=self.graph_type_var
        )
        self.graph_type_dropdown.pack(pady=5)

        # Get all possible columns for selection
        all_columns = self.data_frame.columns.tolist()
        numeric_columns = self.data_frame.select_dtypes(
            include=["number"]
        ).columns.tolist()

        # X-axis variable selection (multi-selection)
        x_axis_label = ctk.CTkLabel(self.control_frame, text="Select X-axis Variables:")
        x_axis_label.pack(pady=5)
        self.x_axis_widget = MultiSelectionDropDown(
            self.control_frame, values=all_columns
        )
        self.x_axis_widget.pack(pady=5)

        # Y-axis variable selection (numeric only)
        y_axis_label = ctk.CTkLabel(self.control_frame, text="Select Y-axis Variable:")
        y_axis_label.pack(pady=5)
        self.y_axis_var = ctk.StringVar(
            value=numeric_columns[0] if numeric_columns else ""
        )
        self.y_axis_dropdown = ctk.CTkOptionMenu(
            self.control_frame, values=numeric_columns, variable=self.y_axis_var
        )
        self.y_axis_dropdown.pack(pady=5)

        # Frame for the plot
        self.plot_frame = ctk.CTkFrame(self.tab1)
        self.plot_frame.pack(fill="both", expand=True, padx=10, pady=5)

    def setup_count_plot_tab(self):
        # Frame for Count Plot
        self.countplot_frame = ctk.CTkFrame(self.tab2)
        self.countplot_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # X-axis selection for Count Plot
        all_columns = self.data_frame.columns.tolist()
        countplot_x_axis_label = ctk.CTkLabel(
            self.countplot_frame, text="Select X-axis Variable:"
        )
        countplot_x_axis_label.pack(pady=5)
        self.countplot_x_axis_var = ctk.StringVar(
            value=all_columns[0] if all_columns else ""
        )
        self.countplot_x_axis_dropdown = ctk.CTkOptionMenu(
            self.countplot_frame, values=all_columns, variable=self.countplot_x_axis_var
        )
        self.countplot_x_axis_dropdown.pack(pady=5)

    def setup_buttons(self):
        save_button = ctk.CTkButton(
            self.popup, text="Save Figure", command=self.save_figure
        )
        save_button.pack(pady=10)
        generate_button = ctk.CTkButton(
            self.popup, text="Show Plot", command=self.generate_graph
        )
        generate_button.pack(pady=10)

    def clear_current_plot(self):
        if self.current_figure["canvas"]:
            self.current_figure["canvas"].get_tk_widget().destroy()

    def generate_count_plot(self):
        x_column = self.countplot_x_axis_var.get()
        if not x_column:
            ctk.CTkLabel(
                self.popup, text="Please select an X variable for the count plot."
            ).pack(pady=5)
            return False

        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        sns.countplot(data=self.data_frame, x=x_column, ax=ax)
        ax.set_xlabel(x_column)
        ax.set_ylabel("Frequency")
        ax.set_title(f"Count Plot of {x_column}")
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.countplot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        self.current_figure = {"fig": fig, "canvas": canvas}
        return True

    def generate_standard_plot(self):
        x_columns = self.x_axis_widget.get_selected_values()
        y_column = self.y_axis_var.get()

        if not x_columns:
            ctk.CTkLabel(
                self.popup, text="Please select at least one X variable."
            ).pack(pady=5)
            return False

        if not y_column:
            ctk.CTkLabel(self.popup, text="Please select Y variable.").pack(pady=5)
            return False

        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        selected_graph_type = self.graph_type_var.get()
        for x_column in x_columns:
            y_data = self.data_frame[y_column]
            if selected_graph_type == "Scatterplot":
                ax.scatter(self.data_frame[x_column], y_data, label=x_column)
            elif selected_graph_type == "Line":
                ax.plot(self.data_frame[x_column], y_data, label=x_column)
            elif selected_graph_type == "Bar":
                ax.bar(self.data_frame[x_column], y_data, label=x_column)

        ax.set_xlabel("X Axis")
        ax.set_ylabel(y_column)
        ax.set_title(f"{selected_graph_type} of {y_column}")
        ax.grid(True)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        self.current_figure = {"fig": fig, "canvas": canvas}
        return True

    def generate_graph(self):
        self.clear_current_plot()

        if self.tabview.get() == "Count Plot":
            self.generate_count_plot()
        else:
            self.generate_standard_plot()

    def save_figure(self):
        if self.current_figure["fig"]:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("PDF files", "*.pdf"),
                ],
            )
            if file_path:
                self.current_figure["fig"].savefig(file_path)


def visualize(master_widget, data_frame: DataFrame):
    """
    Opens a pop-up window for visualization with the given DataFrame.
    """
    if data_frame is None or data_frame.empty:
        return
    DataVisualizer(master_widget, data_frame)
