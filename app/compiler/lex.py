from ply.lex import TOKEN

# To handle reserved words
reserved = {
    "select": "SELECT",
    "from": "FROM",
    "into": "INTO",
    "where": "WHERE",
    "like": "LIKE",
    "insert": "INSERT",
    "and": "AND",
    "or": "OR",
    "not": "NOT",
    "distinct": "DISTINCT",
    "order": "ORDER",
    "by": "BY",
    "asc": "ASC",
    "desc": "DESC",
    "limit": "LIMIT",
    "values": "VALUES",
    "update": "UPDATE",
    "set": "SET",
    "delete": "DELETE",
}

tokens = [
    "INTNUMBER",
    "FLOATNUMBER",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "PERCENT",
    "LPAREN",
    "RPAREN",
    "COLNAME",
    "DATASOURCE",
    "EQUAL",
    "NOTEQUAL",
    "BIGGER_EQUAL",
    "BIGGER",
    "SMALLER_EQUAL",
    "SMALLER",
    "SIMICOLON",
    "COMMA",
    "STRING",
    "PATTERN",
    "COLNUMBER",
] + list(reserved.values())

# Regular expression rules for simple tokens
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_PERCENT = r"%"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_EQUAL = r"=="
t_NOTEQUAL = r"<>"
t_BIGGER_EQUAL = r">="
t_BIGGER = r">"
t_SMALLER_EQUAL = r"<="
t_SMALLER = r"<"
t_SIMICOLON = r";"
t_COMMA = r","

# ignored characters
t_ignore = " \t"  # Spaces and tabs
t_ignore_COMMENT = r"/\*.*\*/"  # Comment

digit = r"([0-9])"
nondigit = r"([_A-Za-z])"
identifier = r"(" + nondigit + r"(" + digit + r"|" + nondigit + r")*)"
# the next line is commented to not include [column number]
# identifier = identifier + r"|" + r"\[" + digit + r"+\]"


@TOKEN(identifier)
def t_COLNAME(t):
    t.type = reserved.get(t.value, "COLNAME")  # Check for reserved words
    return t


@TOKEN(r'"([^"\n])*"')
def t_STRING(t):
    t.value = str(t.value)[1:-1]
    return t


@TOKEN(r"\[\d+\]")
def t_COLNUMBER(t):
    t.value = int(t.value[1:-1])
    return t


# for only positive integers
# @TOKEN(r'\d+')
# for positive and negative integers & integers
# @TOKEN(r"^[+-]?(\d+(\.\d*)?|\.\d+)$")
# def t_FLOATNUMBER(t):
#     t.value = float(t.value)
#     return t


@TOKEN(r"-?\d*.?\d+")
def t_FLOATNUMBER(t):
    t.value = float(t.value)
    return t


@TOKEN(r"\d+")
def t_INTNUMBER(t):
    t.value = int(t.value)
    return t


@TOKEN(r"\[[^,\]\[]+\]")
def t_DATASOURCE(t):
    t.value = str(t.value[1:-1])
    return t


@TOKEN(r"\n+")
def t_newline(t):
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_error(t):
    print(f"Illegal entity {t.value}")
    t.lexer.skip(1)
