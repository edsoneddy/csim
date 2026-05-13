import sys
from ..python.PythonLexer import PythonLexer
from ..java.Java20Lexer import Java20Lexer
from ..cpp.CPP14Lexer import CPP14Lexer
from antlr4 import InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener


class ExtendedErrorListener(ErrorListener):
    def __init__(self, file_name=""):
        super(ExtendedErrorListener, self).__init__()
        self.file_name = file_name

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print(
            f"Syntax error in file {self.file_name} line {line}:{column} {msg}",
            file=sys.stderr,
        )


def ANTLR_tokenize(file_name, file_content, lang):
    """Tokenize source code using ANTLR and handle syntax errors.

    Args:
        file_name: Name of the source file (used for error reporting).
        file_content: Source code as a string to be tokenized.
        lang: programming language of the source code (e.g. python, java, etc.).
    Returns:
        result 
    """
    input_stream = InputStream(file_content)
    error_listener = ExtendedErrorListener(file_name)

    if lang == "python":
        lexer = PythonLexer(input_stream)
    elif lang == "java":
        lexer = Java20Lexer(input_stream)
    elif lang == "cpp":
        lexer = CPP14Lexer(input_stream)
    else:
        raise ValueError(f"Unsupported language: {lang}")

    lexer.removeErrorListeners()
    lexer.addErrorListener(error_listener)
    token_stream = CommonTokenStream(lexer)
    token_stream.fill()

    return [token.type for token in token_stream.tokens]
