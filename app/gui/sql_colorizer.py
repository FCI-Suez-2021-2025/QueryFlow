import customtkinter as ctk
import re

# Create a CustomTkinter application
app = ctk.CTk()
app.geometry("600x450")
app.title("SQL Syntax Highlighter")

# Color schemes for dark and light modes
COLOR_SCHEMES = {
    "dark": {
        "background": "#1E1E1E",
        "text": "#D4D4D4",
        "keyword": "#569CD6",  # Light blue
        "string": "#CE9178",  # Light orange
        "comment": "#6A9955",  # Light green
        "number": "#B5CEA8",  # Light greenish
        "brackets": {
            "square": "#C678DD",  # Purple
            "curly": "#F9A825",  # Yellow
            "round": "#61AFEF",  # Blue
            "angle": "#E5C07B",  # Light yellow
        },
    },
    "light": {
        "background": "#FFFFFF",
        "text": "#000000",
        "keyword": "#0000FF",  # Dark blue
        "string": "#A31515",  # Dark red
        "comment": "#008000",  # Green
        "number": "#098658",  # Dark teal
        "brackets": {
            "square": "#800080",  # Purple
            "curly": "#FF8C00",  # Dark orange
            "round": "#0000CD",  # Medium blue
            "angle": "#DAA520",  # Goldenrod
        },
    },
}


class SQLSyntaxHighlighter:
    def __init__(self, master):
        # List of keywords (case-insensitive)
        self.keywords = [
            "SELECT",
            "FROM",
            "WHERE",
            "TAIL",
            "LIMIT",
            "ORDER",
            "BY",
            "INSERT",
            "UPDATE",
            "DELETE",
            "AND",
            "OR",
            "NOT",
            "IN",
        ]

        self.app = master
        self.current_mode = ctk.StringVar(value="dark")

        # Create mode toggle frame
        self.mode_frame = ctk.CTkFrame(self.app)
        self.mode_frame.pack(pady=10)

        # Create mode toggle button
        self.mode_button = ctk.CTkButton(
            self.mode_frame,
            text="Switch to Light Mode",
            command=self.toggle_mode,
            fg_color="#D4D4D4",
            text_color="#1E1E1E",
        )
        self.mode_button.pack(pady=5)

        # Create text widget
        self.text_widget = ctk.CTkTextbox(
            self.app,
            wrap="word",
            width=580,
            height=360,
            fg_color="#1E1E1E",
            text_color="#D4D4D4",
        )
        self.text_widget.pack(padx=10, pady=10)

        # Bind events
        self.text_widget.bind("<KeyRelease>", self.on_text_change)

        # Insert initial text
        self.text_widget.insert(
            "1.0",
            """SELECT id, [select] FROM users WHERE id > 10 TAIL 5;
/* This is a multi-line comment
that spans multiple lines */
{Curly Braces} (Round Brackets) <Angle Brackets>
"Double Quoted String" 'Single Quoted String'
select * from table WHERE condition""",
        )

        # Apply initial syntax highlighting
        self.highlight_syntax()

    def toggle_mode(self):
        # Switch mode
        new_mode = "light" if self.current_mode.get() == "dark" else "dark"
        self.current_mode.set(new_mode)

        # Update mode button text and colors
        self.mode_button.configure(
            text=f"Switch to {'Dark' if new_mode == 'light' else 'Light'} Mode",
            fg_color=COLOR_SCHEMES[new_mode]["text"],
            text_color=COLOR_SCHEMES[new_mode]["background"],
        )

        # Reapply syntax highlighting with new mode
        self.highlight_syntax()

    def on_text_change(self, event=None):
        self.highlight_syntax()

    def highlight_syntax(self):
        # Get current mode colors
        mode = self.current_mode.get()
        colors = COLOR_SCHEMES[mode]

        # Update text widget colors
        self.text_widget.configure(
            fg_color=colors["background"], text_color=colors["text"]
        )

        # Remove existing tags
        tags = [
            "keyword",
            "string",
            "comment",
            "number",
            "square_brackets",
            "curly_brackets",
            "round_brackets",
            "angle_brackets",
        ]
        for tag in tags:
            self.text_widget.tag_remove(tag, "1.0", "end")

        # Get text content
        text_content = self.text_widget.get("1.0", "end")

        # Create keywords regex pattern
        keywords_pattern = (
            r"\b(" + "|".join(re.escape(kw) for kw in self.keywords) + r")\b"
        )

        # Syntax highlighting patterns
        patterns = [
            # Keywords (case-insensitive, avoiding bracketed column names)
            (
                "keyword",
                keywords_pattern,
                lambda match: not (
                    text_content[max(0, match.start() - 1) : match.start()].startswith(
                        "["
                    )
                    and text_content[match.end() : match.end() + 1].startswith("]")
                ),
            ),
            # Strings (both single and double quotes)
            ("string", r'".*?"|\'.*?\'', None),
            # Comments (multi-line)
            ("comment", r"/\*.*?\*/", None),
            # Numbers
            ("number", r"\b\d+\b", None),
            # Bracket types
            ("square_brackets", r"\[.*?\]", None),
            ("curly_brackets", r"\{.*?\}", None),
            ("round_brackets", r"\(.*?\)", None),
            ("angle_brackets", r"<.*?>", None),
        ]

        # Apply highlighting
        for tag_name, pattern, condition in patterns:
            for match in re.finditer(pattern, text_content, re.DOTALL | re.IGNORECASE):
                # Apply condition if provided
                if condition and not condition(match):
                    continue

                start, end = match.start(), match.end()
                start_index = f"1.0+{start}c"
                end_index = f"1.0+{end}c"

                # Add tag for highlighting
                self.text_widget.tag_add(tag_name, start_index, end_index)

        # Configure tag colors
        self.text_widget.tag_config("keyword", foreground=colors["keyword"])
        self.text_widget.tag_config("string", foreground=colors["string"])
        self.text_widget.tag_config("comment", foreground=colors["comment"])
        self.text_widget.tag_config("number", foreground=colors["number"])

        # Configure bracket colors
        self.text_widget.tag_config(
            "square_brackets", foreground=colors["brackets"]["square"]
        )
        self.text_widget.tag_config(
            "curly_brackets", foreground=colors["brackets"]["curly"]
        )
        self.text_widget.tag_config(
            "round_brackets", foreground=colors["brackets"]["round"]
        )
        self.text_widget.tag_config(
            "angle_brackets", foreground=colors["brackets"]["angle"]
        )


# Create and run the application
highlighter = SQLSyntaxHighlighter(app)

app.mainloop()
