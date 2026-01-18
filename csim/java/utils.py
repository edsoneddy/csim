from .Java20Lexer import Java20Lexer
from antlr4 import Token

EXCLUDED_TOKEN_TYPES = {
    Java20Lexer.LPAREN,
    Java20Lexer.RPAREN,
    Java20Lexer.COLON,
    Java20Lexer.COMMA,
    Token.EOF,
}