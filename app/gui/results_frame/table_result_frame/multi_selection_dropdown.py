from typing import Any
import customtkinter as ctk


import tkinter as tk


class MultiSelectionDropDown(ctk.CTkFrame):
    def __init__(
        self,
        master,
        width=200,
        height=200,
        corner_radius=None,
        border_width=None,
        bg_color="transparent",
        fg_color=None,
        border_color=None,
        background_corner_colors=None,
        overwrite_preferred_drawing_method=None,
        values: list[Any] = None,
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
        if values is None:
            values = []

        # Create a frame for the selection menu with the same color
        self.menu_frame = ctk.CTkFrame(
            self, fg_color="#1985BA", corner_radius=3, border_width=3
        )
        self.menu_frame.pack(expand=True, fill="both", padx=5, pady=5)

        # Menubutton for the multi-selection dropdown with the same color
        self.menubutton = ctk.CTkButton(
            self.menu_frame,
            text="X Axis Columns",
            corner_radius=3,
            fg_color="#1985BA",
            hover_color="#1985BA",
            width=135,
            height=25,
        )
        self.menubutton.pack(expand=True, fill="both")

        # Create a frame for the menu
        self.menu = tk.Menu(self.menubutton, tearoff=False)
        self.menubutton.configure(command=self.toggle_menu)
        self.choices = dict[Any, tk.BooleanVar]()
        self.__add_values_to_menu(values)

    def __add_values_to_menu(self, values: list[Any]) -> None:
        for choice in values:
            self.choices[choice] = tk.BooleanVar(value=False)
            self.menu.add_checkbutton(
                label=choice,
                variable=self.choices[choice],
                onvalue=True,
                offvalue=False,
                font=("Arial", 10),
            )

    def toggle_menu(self):
        if self.menu.winfo_ismapped():
            self.menu.unpost()
        else:
            self.menu.post(self.winfo_rootx(), self.winfo_rooty() + self.winfo_height())

    def deselect_values(self) -> None:
        for _, is_selected in self.choices.items():
            is_selected.set(False)

    def clear_values(self) -> None:
        self.choices.clear()
        self.menu.delete(0, "end")

    def set_values(self, values: list[Any] = None) -> None:
        if not values:
            values = []
        self.__add_values_to_menu(values)

    def get_selected_values(self) -> list[Any]:
        return list(
            map(
                lambda pair: pair[0],
                filter(lambda pair: pair[1].get(), self.choices.items()),
            )
        )
