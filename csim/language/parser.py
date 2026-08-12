import sys
from ..python_3_13.PythonParser import PythonParser
from ..python_3_13.PythonLexer import PythonLexer
from ..java_20.Java20Parser import Java20Parser
from ..java_20.Java20Lexer import Java20Lexer
from ..java_24.Java24Parser import Java24Parser
from ..java_24.Java24Lexer import Java24Lexer
from ..cpp_14.CPP14Parser import CPP14Parser
from ..cpp_14.CPP14Lexer import CPP14Lexer
from ..python_3.Python3Parser import Python3Parser
from ..python_3.Python3Lexer import Python3Lexer
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
        lang: programming language of the source code (e.g. python_3_13, java_20, java_24, cpp_14, etc.).

    Returns:
        ANTLR parse tree representing the code's syntactic structure.
    """

    # Fast path: ANTLR's C++ runtime, when a compiled parser is available for
    # this language. Returns None (and falls through) if unavailable or failed.
    from ..native import native_parse

    native_tree = native_parse(file_content, lang)
    if native_tree is not None:
        return native_tree

    tree = None
    parser = None
    input_stream = InputStream(file_content)
    error_listener = ExtendedErrorListener(file_name)

    if lang == "python_3_13":
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
    elif lang == "java_20":
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
    elif lang == "java_24":
        # Lexing the input code to create a token stream
        lexer = Java24Lexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(error_listener)
        # Parsing the token stream to create a parse tree
        token_stream = CommonTokenStream(lexer)
        parser = Java24Parser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)
        tree = parser.compilationUnit()
    elif lang == "cpp_14":
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
    elif lang == "python_3":
        # Lexing the input code to create a token stream
        lexer = Python3Lexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(error_listener)
        # Parsing the token stream to create a parse tree
        token_stream = CommonTokenStream(lexer)
        parser = Python3Parser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)
        tree = parser.file_input()
    else:
        raise ValueError(f"Unsupported language: {lang}")

    return tree
