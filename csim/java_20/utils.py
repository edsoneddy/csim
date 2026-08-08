from .Java20Lexer import Java20Lexer
from .Java20Parser import Java20Parser
from antlr4 import Token

EXCLUDED_TOKEN_TYPES = {
    # Structural / whitespace / comment tokens.
    Token.EOF,
    Java20Lexer.WS,
    Java20Lexer.COMMENT,
    Java20Lexer.LINE_COMMENT,
    # Grouping / punctuation
    Java20Lexer.LPAREN,
    Java20Lexer.RPAREN,
    Java20Lexer.LBRACE,
    Java20Lexer.RBRACE,
    Java20Lexer.LBRACK,
    Java20Lexer.RBRACK,
    Java20Lexer.SEMI,
    Java20Lexer.COMMA,
    Java20Lexer.DOT,
    Java20Lexer.COLON,
    Java20Lexer.COLONCOLON,
    # Arrow
    Java20Lexer.ARROW,
    # Single-operator precedence-chain connectives
    Java20Lexer.BITAND,
    Java20Lexer.CARET,
    Java20Lexer.BITOR,
    Java20Lexer.AND,
    Java20Lexer.OR,
    # Ternary '?'
    Java20Lexer.QUESTION,
    # Statement keywords
    Java20Lexer.IF,
    Java20Lexer.ELSE,
    Java20Lexer.WHILE,
    Java20Lexer.DO,
    Java20Lexer.SWITCH,
    Java20Lexer.SYNCHRONIZED,
    Java20Lexer.TRY,
    Java20Lexer.CATCH,
    Java20Lexer.BREAK,
    Java20Lexer.CONTINUE,
    Java20Lexer.CASE,
    Java20Lexer.DEFAULT,
    # Type-declaration keywords
    Java20Lexer.CLASS,
    Java20Lexer.ENUM,
    Java20Lexer.INTERFACE,
    Java20Lexer.RECORD,
    # NEW
    Java20Lexer.NEW,
    # EXTENDS / IMPLEMENTS / THROWS: always wrap mandatory real type-list
    Java20Lexer.EXTENDS,
    Java20Lexer.IMPLEMENTS,
    Java20Lexer.THROWS,
    # Additional tokens
    Java20Lexer.PERMITS,
    Java20Lexer.RETURN,
    Java20Lexer.STATIC,
    Java20Lexer.THROW,
    Java20Lexer.AT,
    Java20Lexer.ASSIGN,
    Java20Lexer.GT,
    Java20Lexer.LT,
    Java20Lexer.INC,
    Java20Lexer.DEC,
}
EXCLUDE_CHILDRENS_FROM_RULE = dict()
COLLAPSED_RULE_INDICES = {
    # Import/package machinery
    Java20Parser.RULE_importDeclaration,
    Java20Parser.RULE_singleTypeImportDeclaration,
    Java20Parser.RULE_typeImportOnDemandDeclaration,
    Java20Parser.RULE_singleStaticImportDeclaration,
    Java20Parser.RULE_staticImportOnDemandDeclaration,
    Java20Parser.RULE_packageDeclaration,
    # Static array-literal display syntax ('{1, 2, 3}')
    Java20Parser.RULE_arrayInitializer,
}
HASHED_RULE_INDICES = {
    Java20Parser.RULE_multiplicativeExpression,
    Java20Parser.RULE_additiveExpression,
    Java20Parser.RULE_shiftExpression,
    Java20Parser.RULE_relationalExpression,
    Java20Parser.RULE_equalityExpression,
    Java20Parser.RULE_andExpression,
    Java20Parser.RULE_exclusiveOrExpression,
    Java20Parser.RULE_inclusiveOrExpression,
    Java20Parser.RULE_conditionalAndExpression,
    Java20Parser.RULE_conditionalOrExpression,
    # Additional
    Java20Parser.RULE_fieldDeclaration,
    Java20Parser.RULE_variableDeclarator,
    Java20Parser.RULE_localVariableDeclaration,
}

CONTROL_EQUIVALENCE_RULE_INDICES = set()
RULE_ASSIGNMENT = Java20Parser.RULE_assignment
ASIGN_OP_NORMALIZED = dict()
EXCLUDED_RULE_TYPES = {
    Java20Parser.RULE_identifier,
    Java20Parser.RULE_typeIdentifier,
    Java20Parser.RULE_unqualifiedMethodIdentifier,
    # Type arguments and declarations
    Java20Parser.RULE_typeArguments,
    Java20Parser.RULE_typeArgumentList,
    Java20Parser.RULE_typeArgument,
    Java20Parser.RULE_typeName,
    Java20Parser.RULE_typeParameters,
    Java20Parser.RULE_typeParameterList,
    # Class declarations and modifiers
    Java20Parser.RULE_classModifier,
    Java20Parser.RULE_classExtends,
    Java20Parser.RULE_classPermits,
    # Field declarations
    Java20Parser.RULE_fieldModifier,
    Java20Parser.RULE_variableDeclaratorId,
    # Unann types
    Java20Parser.RULE_unannReferenceType,
    Java20Parser.RULE_unannClassOrInterfaceType,
    # Method declarations and parts
    Java20Parser.RULE_methodModifier,
    Java20Parser.RULE_result,
    # Constructors.
    Java20Parser.RULE_constructorModifier,
    Java20Parser.RULE_simpleTypeName,
    # Interfaces.
    Java20Parser.RULE_interfaceModifier,
    Java20Parser.RULE_interfaceExtends,
    # Annotations.
    Java20Parser.RULE_annotation,
    Java20Parser.RULE_markerAnnotation,
    # for-loop control clauses
    Java20Parser.RULE_forInit,
    Java20Parser.RULE_forUpdate,
    Java20Parser.RULE_statementExpressionList,
}
