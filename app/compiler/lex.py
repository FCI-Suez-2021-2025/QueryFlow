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
    "tail": "TAIL",
    "values": "VALUES",
    "update": "UPDATE",
    "set": "SET",
    "delete": "DELETE",
}

tokens = [
    "FLOATNUMBER",
    "NEGATIVE_INTNUMBER",
    "POSITIVE_INTNUMBER",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "PERCENT",
    "LPAREN",
    "RPAREN",
    "SIMPLE_COLNAME",
    "BRACKETED_COLNAME",
    "COLNUMBER",
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
# the next pattern not enforce full match
bracketed_identifier = r"\[([_A-Za-z][ _A-Za-z0-9]*)\]"
simple_identifier = r"(" + nondigit + r"(" + digit + r"|" + nondigit + r")*)"


# the next line is commented to not include [column number]
# simple_identifier = simple_identifier + r"|" + r"\[" + digit + r"+\]"


# region this code to not conflict with SIMPE_COLNAME
@TOKEN(r"select")
def t_SELECT(t):
    return t


@TOKEN(r"distinct")
def t_DISTINCT(t):
    return t


@TOKEN(r"from")
def t_FROM(t):
    return t


@TOKEN(r"into")
def t_INTO(t):
    return t


@TOKEN(r"where")
def t_WHERE(t):
    return t


@TOKEN(r"like")
def t_LIKE(t):
    return t


@TOKEN(r"not")
def t_NOT(t):
    return t


@TOKEN(r"and")
def t_AND(t):
    return t


@TOKEN(r"or")
def t_OR(t):
    return t


@TOKEN(r"insert")
def t_INSERT(t):
    return t


@TOKEN(r"values")
def t_VALUES(t):
    return t


@TOKEN(r"update")
def t_UPDATE(t):
    return t


@TOKEN(r"set")
def t_SET(t):
    return t


@TOKEN(r"delete")
def t_DELETE(t):
    return t


@TOKEN(r"order")
def t_ORDER(t):
    return t


@TOKEN(r"by")
def t_BY(t):
    return t


@TOKEN(r"desc")
def t_DESC(t):
    return t


@TOKEN(r"asc")
def t_ASC(t):
    return t


@TOKEN(r"limit")
def t_LIMIT(t):
    return t


@TOKEN(r"tail")
def t_TAIL(t):
    return t


# endregion


@TOKEN(simple_identifier)
def t_SIMPLE_COLNAME(t):
    # t.type = reserved.get(t.value, "SIMPLE_COLNAME")  # Check for reserved words
    return t


@TOKEN(bracketed_identifier)
def t_BRACKETED_COLNAME(t):
    t.value = t.value[1:-1]
    return t


@TOKEN(r"\[\d+\]")
def t_COLNUMBER(t):
    return t


@TOKEN(r'"([^"\n])*"')
def t_STRING(t):
    t.value = str(t.value)[1:-1]

    return t


# region Numbers RE
# ! Don't Change the order of these functions due not cause a conflict in the lexer


# this will accept any float number except 0 or +0,-0 or ([+ or -] then any seuqence of 0s only)
@TOKEN(r"[+-]?(?!0(\.0+)?$)(\d+\.\d*|\.\d+)")
def t_FLOATNUMBER(t):
    t.value = float(t.value)
    return t


# this re will exclude 0
@TOKEN(r"-[1-9]\d*")
def t_NEGATIVE_INTNUMBER(t):
    t.value = int(t.value)
    return t


# this re will include 0 and + is optional
@TOKEN(r"\+?\d+")
def t_POSITIVE_INTNUMBER(t):
    t.value = int(t.value)
    return t


# endregion


@TOKEN(r"\{[^,{}\[]+\}")
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
