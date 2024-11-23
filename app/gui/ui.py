import customtkinter as ctk

def show_fly_window(input_cell):
    """Show the fly window with the Python code."""
    fly_window = ctk.CTkToplevel(root)
    fly_window.title("Python Code")
    fly_window.geometry("500x350")
    fly_window.transient(root)
    fly_window.grab_set()

    python_code = ctk.CTkTextbox(
        fly_window,
        wrap="word",
        fg_color="#1E1E1E",
        text_color="#00FFCC",
        font=("JetBrains Mono", 12),
    )
    python_code.insert("0.0", f"Generated Python code:\n{input_cell.get()}")
    python_code.pack(fill="both", expand=True, padx=10, pady=10)

    # Copy to clipboard button
    def copy_code():
        root.clipboard_clear()
        root.clipboard_append(python_code.get("0.0", "end").strip())
        root.update()

    button_frame = ctk.CTkFrame(fly_window)
    button_frame.pack(fill="x", pady=5, padx=10)
    ctk.CTkButton(button_frame, text="Copy to Clipboard", command=copy_code).pack(
        side="left", padx=5
    )
    ctk.CTkButton(button_frame, text="Close", command=fly_window.destroy).pack(
        side="right", padx=5
    )


def run_output(input_cell, output_label):
    """Create the output section and display the output when the Run button is clicked."""
    # Create the output section dynamically
    output_section = ctk.CTkFrame(input_cell.master, corner_radius=10, fg_color="#2E2E2E")
    output_section.pack(fill="x", padx=10, pady=5, ipadx=5, ipady=5)

    # Output label
    output_label = ctk.CTkLabel(
        output_section, text="Output", text_color="#FFCC00", font=("JetBrains Mono", 12)
    )
    output_label.pack(anchor="w", padx=5)

    output_cell = ctk.CTkLabel(
        output_section,
        text="Output will be displayed here!",
        text_color="#FFFFFF",
        font=("JetBrains Mono", 12),
    )
    output_cell.pack(fill="x", padx=5, pady=5)

    # Update the output label with the result
    output_cell.configure(text=f"Output: {input_cell.get()}")


def add_new_cell():
    """Add a new input-output row to the UI."""
    create_input_row()


def delete_cell(input_frame):
    """Delete the specific input-output row."""
    input_frame.destroy()


def toggle_theme():
    """Toggle between Light and Dark modes."""
    current_mode = ctk.get_appearance_mode()
    if current_mode == "Dark":
        ctk.set_appearance_mode("Light")
        update_button_colors("Light")
        toggle_button.configure(text="Turn to Dark")  # Update button text for light mode
    else:
        ctk.set_appearance_mode("Dark")
        update_button_colors("Dark")
        toggle_button.configure(text="Turn to Light")  # Update button text for dark mode


def update_button_colors(mode):
    """Update the button colors based on the current mode."""
    for button in sidebar.winfo_children():
        if isinstance(button, ctk.CTkButton):
            if mode == "Light":
                button.configure(fg_color="white", text_color="black")
            else:
                button.configure(fg_color="#00CC66", text_color="white")


# Add Input and Output rows
def create_input_row():
    input_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color="#1E1E1E")
    input_frame.pack(fill="x", padx=10, pady=10, ipadx=10, ipady=5)

    # Input Section
    input_section = ctk.CTkFrame(input_frame, corner_radius=10, fg_color="#2E2E2E")
    input_section.pack(fill="x", padx=10, pady=5, ipadx=5, ipady=5)
    input_label = ctk.CTkLabel(
        input_section, text="Input", text_color="#00FFCC", font=("JetBrains Mono", 12)
    )
    input_label.pack(anchor="w", padx=5)

    input_cell = ctk.CTkEntry(
        input_section,
        placeholder_text="Type your input here...",
        font=("JetBrains Mono", 12),
    )
    input_cell.pack(fill="x", padx=5, pady=5)

    # Button Row
    button_row = ctk.CTkFrame(input_section, fg_color="#2E2E2E")
    button_row.pack(fill="x", padx=5, pady=5)

    ctk.CTkButton(
        button_row,
        text="Run",
        command=lambda: run_output(input_cell, output_label),
        corner_radius=5,
        fg_color="#00CC66",
        hover_color="#AA3333",
).pack(fill="x", pady=10, padx=10)

# Content Area
content_frame = ctk.CTkScrollableFrame(root_frame, corner_radius=10)
content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

# Initial Cell
create_input_row()

# Run the App
root.mainloop()