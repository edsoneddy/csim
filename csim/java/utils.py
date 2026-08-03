from .Java20Lexer import Java20Lexer
from .Java20Parser import Java20Parser
from antlr4 import Token

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
EXCLUDE_CHILDRENS_FROM_RULE = dict()
COLLAPSED_RULE_INDICES = {
    # Import declarations
    Java20Parser.RULE_singleTypeImportDeclaration,
    Java20Parser.RULE_typeImportOnDemandDeclaration,
    Java20Parser.RULE_singleStaticImportDeclaration,
    Java20Parser.RULE_staticImportOnDemandDeclaration,
    Java20Parser.RULE_packageDeclaration,
    Java20Parser.RULE_packageModifier,
    Java20Parser.RULE_importDeclaration,
    # List wrappers
    Java20Parser.RULE_variableInitializerList,
    # Name and type wrappers that only restate identifier structure
    Java20Parser.RULE_typeArguments,
    Java20Parser.RULE_typeArgumentsOrDiamond,
    # Array dimensions
    Java20Parser.RULE_dims,
    Java20Parser.RULE_dimExpr,
    Java20Parser.RULE_dimExprs,
    # Modifier and annotation wrappers
    Java20Parser.RULE_typeParameterModifier,
    Java20Parser.RULE_classModifier,
    Java20Parser.RULE_methodModifier,
    Java20Parser.RULE_fieldModifier,
    Java20Parser.RULE_interfaceModifier,
    Java20Parser.RULE_constructorModifier,
    Java20Parser.RULE_enumConstantModifier,
    Java20Parser.RULE_recordComponentModifier,
    Java20Parser.RULE_constantModifier,
    Java20Parser.RULE_interfaceMethodModifier,
    Java20Parser.RULE_annotationInterfaceElementModifier,
    Java20Parser.RULE_annotation,
    Java20Parser.RULE_normalAnnotation,
    Java20Parser.RULE_markerAnnotation,
    Java20Parser.RULE_singleElementAnnotation,
}
HASHED_RULE_INDICES = set()
CONTROL_EQUIVALENCE_RULE_INDICES = dict()
EXCLUDED_RULE_TYPES = {
    # Identifier wrappers: the lexical names are already excluded above,
    # so keeping these rules only adds noise and extra depth.
    Java20Parser.RULE_identifier,
    Java20Parser.RULE_typeIdentifier,
    Java20Parser.RULE_unqualifiedMethodIdentifier,
    Java20Parser.RULE_contextualKeyword,
    Java20Parser.RULE_contextualKeywordMinusForTypeIdentifier,
    Java20Parser.RULE_contextualKeywordMinusForUnqualifiedMethodIdentifier,
    Java20Parser.RULE_packageName,
    Java20Parser.RULE_packageOrTypeName,
    Java20Parser.RULE_typeName,
    Java20Parser.RULE_expressionName,
    Java20Parser.RULE_methodName,
    Java20Parser.RULE_variableDeclaratorId,
}