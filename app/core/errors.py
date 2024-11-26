class LexerError(Exception):
    def __init__(self, char, lineno, position):
        self.title = "Scanning Error"
        self.message = (
            f"Illegal character '{char}' at line {lineno}, position {position}."
        )
        self.full_message: str = f"{self.title}: {self.message}"
        self.char: str = char
        self.lineno: int = lineno
        self.position: int = position
        super().__init__(self.full_message)


class ParserError(Exception):
    def __init__(self, message: str, char, lineno, position):
        super().__init__(message)
        self.title = "Scanning Error"
        self.message = message
        self.full_message: str = f"{self.title}: {self.message}"
        self.char: str = char
        self.lineno: int = lineno
        self.position: int = position
        super().__init__(self.message)


class PythonExecutionError(Exception):
    def __init__(
        self,
        message: str,
        code: str = None,
        line: int = None,
        position: int = None,
    ):
        """
        Custom exception for handling errors during dynamic code execution.

        :param message: Error message.
        :param code: The code that caused the error (optional).
        :param line: Line number of the error (optional).
        :param position: Position of the error in the code (optional).
        """
        self.message_title = "Python Execution Error"
        self.message = message
        self.full_message: str = f"{self.message_title}: {message}\n"
        self.code = code
        self.line = line
        self.position = position
        self.full_message_with_code_and_line_numbers: str = (
            self.full_message
            + (f"Code:\n{self.code}\n" if self.code else "")
            + (f"Line: {self.line}, Position: {self.position}\n" if self.line else "")
        )
        super().__init__(self.full_message_with_code_and_line_numbers)
