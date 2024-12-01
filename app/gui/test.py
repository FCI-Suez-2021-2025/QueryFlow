class Colorizer:
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
    KEYWORDS = [
        "SELECT",
        "FROM",
        "INTO",
        "WHERE",
        "LIKE",
        "INSERT",
        "AND",
        "ORDER",
        "OR",
        "NOT",
        "DISTINCT",
        "BY",
        "ASC",
        "DESC",
        "LIMIT",
        "TAIL",
        "VALUES",
        "UPDATE",
        "SET",
        "DELETE",
    ]
