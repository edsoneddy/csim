from .PythonParser import PythonParser
from .PythonLexer import PythonLexer
from antlr4 import Token

# Excluded Parser Rules and Lexer Tokens
EXCLUDED_RULE_INDICES = {}

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

# Collapsed Parser Rules
COLLAPSED_RULE_INDICES = {
    PythonParser.RULE_list,  # Lists
    PythonParser.RULE_import_stmt,  # Import statements
}

# Hash-Based Pruning
HASHED_RULE_INDICES = {
    PythonParser.RULE_assignment,
    PythonParser.RULE_parameters,
    PythonParser.RULE_power,
    PythonParser.RULE_primary,
    PythonParser.RULE_comparison,
    PythonParser.RULE_star_targets,
    PythonParser.RULE_sum,
    PythonParser.RULE_del_target,
    PythonParser.RULE_term,
}
