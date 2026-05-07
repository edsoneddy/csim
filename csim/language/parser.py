import sys
from ..python.PythonParser import PythonParser
from ..python.PythonLexer import PythonLexer
from ..java.Java20Parser import Java20Parser
from ..java.Java20Lexer import Java20Lexer
from ..cpp.CPP14Parser import CPP14Parser
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


def ANTLR_parse(file_name, file_content, lang):
    """Parse source code into an ANTLR parse tree and handle syntax errors.

    Args:
        file_name: Name of the source file (used for error reporting).
        file_content: Source code as a string to be parsed.
        lang: programming language of the source code (e.g. python, java, etc.).

    Returns:
        ANTLR parse tree representing the code's syntactic structure.
    """

    tree = None
    parser = None
    input_stream = InputStream(file_content)
    error_listener = ExtendedErrorListener(file_name)

    if lang == "python":
        # Lexing the input code to create a token stream
        lexer = PythonLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(error_listener)
        # Parsing the token stream to create a parse tree
        token_stream = CommonTokenStream(lexer)
        parser = PythonParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)
        tree = parser.file_input()
    elif lang == "java":
        # Lexing the input code to create a token stream
        lexer = Java20Lexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(error_listener)
        # Parsing the token stream to create a parse tree
        token_stream = CommonTokenStream(lexer)
        parser = Java20Parser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)
        tree = parser.compilationUnit()
    elif lang == "cpp":
        # Lexing the input code to create a token stream
        lexer = CPP14Lexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(error_listener)
        # Parsing the token stream to create a parse tree
        token_stream = CommonTokenStream(lexer)
        parser = CPP14Parser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)
        tree = parser.translationUnit()

    return tree
