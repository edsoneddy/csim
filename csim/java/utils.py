from .Java20Lexer import Java20Lexer
from .Java20Parser import Java20Parser
from antlr4 import Token

EXCLUDED_RULE_INDICES = {
    # Modifiers and type identifiers
    Java20Parser.RULE_classModifier,
    Java20Parser.RULE_typeIdentifier,
    Java20Parser.RULE_fieldModifier,
    Java20Parser.RULE_unannPrimitiveType,
    Java20Parser.RULE_unannType,
    Java20Parser.RULE_primitiveType,
    Java20Parser.RULE_unannClassOrInterfaceType,
    Java20Parser.RULE_methodModifier,
}

COLLAPSED_RULE_INDICES = {
    # Import declarations
    Java20Parser.RULE_singleTypeImportDeclaration,
    Java20Parser.RULE_singleTypeImportDeclaration,
    Java20Parser.RULE_typeImportOnDemandDeclaration,
    Java20Parser.RULE_singleStaticImportDeclaration,
    Java20Parser.RULE_staticImportOnDemandDeclaration,
    # Miscellaneous declarations
    Java20Parser.RULE_variableInitializerList,
    # Array dimensions
    Java20Parser.RULE_dims,
    Java20Parser.RULE_dimExpr,
}

EXCLUDED_TOKEN_TYPES = {
    # Punctuation that does not contribute to structural similarity
    Java20Lexer.LPAREN,
    Java20Lexer.RPAREN,
    Java20Lexer.LBRACE,
    Java20Lexer.RBRACE,
    Java20Lexer.COLON,
    Java20Lexer.COMMA,
    Java20Lexer.SEMI,
    Java20Lexer.Identifier,
    # Keywords that do not contribute to structural similarity
    Java20Lexer.PUBLIC,
    Java20Lexer.CLASS,
    Java20Lexer.STATIC,
    Java20Lexer.NEW,
    Java20Lexer.VOID,
    Java20Lexer.RETURN,
    Java20Lexer.BREAK,
    # Keywords related to control flow
    Java20Lexer.IF,
    Java20Lexer.ELSE,
    Java20Lexer.FOR,
    Java20Lexer.WHILE,
    Java20Lexer.DO,
    Java20Lexer.SWITCH,
    Java20Lexer.CASE,
    # Keywords related to data types
    Java20Lexer.INT,
    Java20Lexer.BOOLEAN,
    Java20Lexer.BYTE,
    Java20Lexer.CHAR,
    Java20Lexer.DOUBLE,
    Java20Lexer.FLOAT,
    Java20Lexer.LONG,
    Java20Lexer.SHORT,
    Java20Lexer.IntegerLiteral,
    Java20Lexer.FloatingPointLiteral,
    Java20Lexer.BooleanLiteral,
    Java20Lexer.CharacterLiteral,
    Java20Lexer.StringLiteral,
    # Whitespace and comments
    Token.EOF,
}
