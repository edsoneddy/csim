from .PythonParser import PythonParser
from .PythonLexer import PythonLexer
from antlr4 import Token

EXCLUDED_RULE_INDICES = {}

COLLAPSED_RULE_INDICES = {
    # Lists
    PythonParser.RULE_list,
    # Import statements
    PythonParser.RULE_import_stmt,
}

EXCLUDED_TOKEN_TYPES = {
    # Punctuation and structural tokens
    PythonLexer.LPAR,
    PythonLexer.RPAR,
    PythonLexer.COLON,
    PythonLexer.COMMA,
    PythonLexer.INDENT,
    PythonLexer.DEDENT,
    PythonLexer.NEWLINE,
    Token.EOF,
    # Keywords
    PythonLexer.DEF,
    PythonLexer.FOR,
    PythonLexer.IN,
    PythonLexer.IF,
    PythonLexer.RETURN,
    PythonLexer.AS,
    PythonLexer.WHILE,
    PythonLexer.ELSE,
    PythonLexer.ELIF,
    PythonLexer.TRY,
    PythonLexer.EXCEPT,
    PythonLexer.FINALLY,
}

HASHED_RULE_INDICES = {
    PythonParser.RULE_assignment,
}

