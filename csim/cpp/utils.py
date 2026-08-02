from .CPP14Lexer import CPP14Lexer
from .CPP14Parser import CPP14Parser
from antlr4 import Token

EXCLUDED_TOKEN_TYPES = {
    # Punctuation that does not contribute to structural similarity
    CPP14Lexer.LeftParen,
    CPP14Lexer.RightParen,
    CPP14Lexer.LeftBrace,
    CPP14Lexer.RightBrace,
    CPP14Lexer.Colon,
    CPP14Lexer.Comma,
    CPP14Lexer.Semi,
    CPP14Lexer.Identifier,
    # Keywords that do not contribute to structural similarity
    CPP14Lexer.Public,
    CPP14Lexer.Class,
    CPP14Lexer.Static,
    CPP14Lexer.New,
    CPP14Lexer.Void,
    CPP14Lexer.Return,
    CPP14Lexer.Break,
    CPP14Lexer.Continue,
    # Keywords related to control flow
    CPP14Lexer.If,
    CPP14Lexer.Else,
    CPP14Lexer.For,
    CPP14Lexer.While,
    CPP14Lexer.Do,
    CPP14Lexer.Switch,
    CPP14Lexer.Case,
    CPP14Lexer.Default,
    CPP14Lexer.Try,
    CPP14Lexer.Catch,
    CPP14Lexer.Throw,
    # Keywords related to data types
    CPP14Lexer.Int,
    CPP14Lexer.Bool,
    CPP14Lexer.BinaryLiteral,
    CPP14Lexer.Char,
    CPP14Lexer.Double,
    CPP14Lexer.Float,
    CPP14Lexer.Long,
    CPP14Lexer.Short,
    CPP14Lexer.IntegerLiteral,
    CPP14Lexer.FloatingLiteral,
    CPP14Lexer.BooleanLiteral,
    CPP14Lexer.CharacterLiteral,
    CPP14Lexer.StringLiteral,
    # Whitespace and comments
    Token.EOF,
}
EXCLUDE_CHILDRENS_FROM_RULE = dict()
COLLAPSED_RULE_INDICES = set()
HASHED_RULE_INDICES = set()
CONTROL_EQUIVALENCE_RULE_INDICES = dict()
EXCLUDED_RULE_TYPES = set()