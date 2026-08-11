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
    # csim-batch-tuner sweep (scripts/report.md): each keyword/operator is
    # redundant once its parent rule already carries a distinct label
    # (module directives, yield/assert/finally/for/this statements, and
    # punctuation whose surrounding rule shape already differs). Verified
    # collision-free in combination with every other entry added below.
    Java20Lexer.EXPORTS,
    Java20Lexer.MODULE,
    Java20Lexer.OPEN,
    Java20Lexer.OPENS,
    Java20Lexer.PROVIDES,
    Java20Lexer.REQUIRES,
    Java20Lexer.TO,
    Java20Lexer.WITH,
    Java20Lexer.YIELD,
    Java20Lexer.ASSERT,
    Java20Lexer.FINALLY,
    Java20Lexer.FOR,
    Java20Lexer.THIS,
    Java20Lexer.ELLIPSIS,
    Java20Lexer.BANG,
    Java20Lexer.TILDE,
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
    # Body-wrapping rules: content-based hash preserves genuine differences
    # while collapsing internal structure to a single node.
    # csim-batch-tuner sweep, scripts/report.md, verified collision-free
    # in combination.
    Java20Parser.RULE_ordinaryCompilationUnit,
    Java20Parser.RULE_moduleDeclaration,
    Java20Parser.RULE_classBody,
    Java20Parser.RULE_methodDeclaration,
    Java20Parser.RULE_exceptionTypeList,
    Java20Parser.RULE_constructorDeclaration,
    Java20Parser.RULE_enumBody,
    Java20Parser.RULE_enumBodyDeclarations,
    Java20Parser.RULE_recordDeclaration,
    Java20Parser.RULE_normalInterfaceDeclaration,
    Java20Parser.RULE_interfaceMethodDeclaration,
    Java20Parser.RULE_annotationInterfaceBody,
    Java20Parser.RULE_assertStatement,
    Java20Parser.RULE_whileStatement,
    Java20Parser.RULE_synchronizedStatement,
    Java20Parser.RULE_tryWithResourcesStatement,
    Java20Parser.RULE_resourceList,
    Java20Parser.RULE_unaryExpression,
    Java20Parser.RULE_conditionalExpression,
    Java20Parser.RULE_switchExpression,
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
    # csim-batch-tuner sweep (scripts/report.md), verified collision-free
    # in combination with every other entry in this file. NOTE:
    # topLevelClassOrInterfaceDeclaration was DELIBERATELY EXCLUDED:
    # confirmed it drops entire class/interface bodies from every
    # compilation unit (only package/import lines survive). Also dropped
    # for causing collisions when combined with the rest of this set:
    # moduleDirective, methodHeader, methodDeclarator, formalParameterList,
    # formalParameter, staticInitializer, ifThenElseStatement, switchRule,
    # enhancedForStatement, tryStatement, catches,
    # unaryExpressionNotPlusMinus. See the audit method note at the end of
    # this file.
    Java20Parser.RULE_moduleName,
    Java20Parser.RULE_classImplements,
    Java20Parser.RULE_interfaceTypeList,
    Java20Parser.RULE_receiverParameter,
    Java20Parser.RULE_variableArityParameter,
    Java20Parser.RULE_variableModifier,
    Java20Parser.RULE_throwsT,
    Java20Parser.RULE_instanceInitializer,
    Java20Parser.RULE_constructorDeclarator,
    Java20Parser.RULE_explicitConstructorInvocation,
    Java20Parser.RULE_enumConstantList,
    Java20Parser.RULE_enumConstant,
    Java20Parser.RULE_recordHeader,
    Java20Parser.RULE_recordComponentList,
    Java20Parser.RULE_recordComponent,
    Java20Parser.RULE_interfacePermits,
    Java20Parser.RULE_constantDeclaration,
    Java20Parser.RULE_interfaceMethodModifier,
    Java20Parser.RULE_defaultValue,
    Java20Parser.RULE_statementNoShortIf,
    Java20Parser.RULE_ifThenStatement,
    Java20Parser.RULE_switchStatement,
    Java20Parser.RULE_switchBlockStatementGroup,
    Java20Parser.RULE_switchLabel,
    Java20Parser.RULE_caseConstant,
    Java20Parser.RULE_doStatement,
    Java20Parser.RULE_basicForStatement,
    Java20Parser.RULE_throwStatement,
    Java20Parser.RULE_catchClause,
    Java20Parser.RULE_catchFormalParameter,
    Java20Parser.RULE_catchType,
    Java20Parser.RULE_finallyBlock,
    Java20Parser.RULE_resourceSpecification,
    Java20Parser.RULE_yieldStatement,
    Java20Parser.RULE_arrayAccess,
    Java20Parser.RULE_preIncrementExpression,
    Java20Parser.RULE_castExpression,
    Java20Parser.RULE_assignment,
    Java20Parser.RULE_leftHandSide,
}
