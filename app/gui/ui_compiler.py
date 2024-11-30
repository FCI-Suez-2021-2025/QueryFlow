import customtkinter as ctk

from vertical_tab_view import VerticalTabView


# Initialize customtkinter
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"


class UICompiler(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Vertical Tab View Example")
        self.geometry("800x500")
        self.current_tab_index = -1
        # Create a top frame for controls (buttons and dropdown)
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(
            side="top", fill="x", padx=20, pady=5
        )  # Full width of the window
        self.toggle_button = ctk.CTkButton(
            self.top_frame, text="Collapse Tabs", command=self.toggle_tabs
        )
        self.toggle_button.pack(side="left", padx=10, pady=5)
        # Add Tab button
        add_tab_button = ctk.CTkButton(
            self.top_frame, text="Add Tab", command=self.add_tab
        )
        add_tab_button.pack(side="left", padx=5, pady=5)

        # Theme toggle switch
        self.theme_switch = ctk.CTkSwitch(
            self.top_frame, text="Dark Mode", command=self.toggle_theme
        )
        self.theme_switch.pack(side="left", padx=10, pady=5)
        self.theme_switch.select()  # Set initial state to "Dark"

        # Scaling dropdown
        scaling_label = ctk.CTkLabel(self.top_frame, text="Scaling:")
        scaling_label.pack(side="left", padx=(10, 5), pady=5)

        self.scaling_options = ["100%", "125%", "150%", "175%", "200%"]
        scaling_dropdown = ctk.CTkOptionMenu(
            self.top_frame, values=self.scaling_options, command=self.change_scaling
        )
        scaling_dropdown.set("100%")
        scaling_dropdown.pack(side="left", padx=5, pady=5)

        # Create a main frame for the layout
        self.vertical_tab_view = VerticalTabView(self)
        self.vertical_tab_view.pack(fill="both", expand=True, padx=20, pady=10)

        self.current_tab_index = 0

    def add_tab(self):
        self.vertical_tab_view.add_tab()

    def toggle_tabs(self):
        self.vertical_tab_view.toggle_tabs()

    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        new_mode = "Dark" if current_mode == "Light" else "Light"
        ctk.set_appearance_mode(new_mode)

    def change_scaling(self, scaling):
        scale_map = {"100%": 1.0, "125%": 1.25, "150%": 1.5, "175%": 1.75, "200%": 2.0}
        scaling_factor = scale_map.get(scaling, 1.0)
        ctk.set_widget_scaling(scaling_factor)
