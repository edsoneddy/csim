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

# Hashing policy (see docs/pruning_fidelity.md): only "islands" -- expressions,
# simple statements, declarations and parameter lists that contain no control
# flow -- collapse to a digest. Blocks, loops, conditionals, try/catch, switch,
# methods and classes stay as real nodes, so the program's skeleton survives.
# The previous policy also hashed classBody/methodDeclaration/whileStatement/
# compilationUnit and dropped assignments, if/for/switch/throw/catch entirely:
# 93% of real files collapsed to ONE node and the index moved by ~0.15 vs. the
# unpruned tree. This one: ~7x compression at ~0.065-0.08 error.
# The island list comes from the rules that never contain a STRUCTURAL rule in
# real submissions (jv-umsa-dataset/all_java, 2 disjoint problem sets).
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
    Java20Parser.RULE_conditionalExpression,
    Java20Parser.RULE_unaryExpression,
    Java20Parser.RULE_postfixExpression,
    Java20Parser.RULE_postIncrementExpression,
    Java20Parser.RULE_postDecrementExpression,
    Java20Parser.RULE_preIncrementExpression,
    Java20Parser.RULE_preDecrementExpression,
    Java20Parser.RULE_castExpression,
    Java20Parser.RULE_methodInvocation,
    Java20Parser.RULE_argumentList,
    Java20Parser.RULE_arrayAccess,
    Java20Parser.RULE_arrayCreationExpressionWithoutInitializer,
    Java20Parser.RULE_dimExprs,
    Java20Parser.RULE_primaryNoNewArray,
    Java20Parser.RULE_lambdaExpression,
    Java20Parser.RULE_unqualifiedClassInstanceCreationExpression,
    Java20Parser.RULE_assignment,
    Java20Parser.RULE_localVariableDeclaration,
    Java20Parser.RULE_fieldDeclaration,
    Java20Parser.RULE_variableDeclarator,
    Java20Parser.RULE_variableDeclaratorList,
    Java20Parser.RULE_methodHeader,
    Java20Parser.RULE_formalParameter,
    Java20Parser.RULE_formalParameterList,
    Java20Parser.RULE_catchFormalParameter,
    Java20Parser.RULE_arrayType,
    Java20Parser.RULE_unannArrayType,
    Java20Parser.RULE_unannClassOrInterfaceType,
    Java20Parser.RULE_typeArgumentList,
}

# A hashed rule is NOT collapsed if its subtree contains one of these (e.g. a
# lambda or anonymous class with a block body): its statements are the skeleton.
STRUCTURAL_RULE_INDICES = {
    Java20Parser.RULE_block,
    Java20Parser.RULE_blockStatements,
    Java20Parser.RULE_ifThenStatement,
    Java20Parser.RULE_ifThenElseStatement,
    Java20Parser.RULE_ifThenElseStatementNoShortIf,
    Java20Parser.RULE_whileStatement,
    Java20Parser.RULE_whileStatementNoShortIf,
    Java20Parser.RULE_doStatement,
    Java20Parser.RULE_forStatement,
    Java20Parser.RULE_forStatementNoShortIf,
    Java20Parser.RULE_basicForStatement,
    Java20Parser.RULE_basicForStatementNoShortIf,
    Java20Parser.RULE_enhancedForStatement,
    Java20Parser.RULE_enhancedForStatementNoShortIf,
    Java20Parser.RULE_switchStatement,
    Java20Parser.RULE_switchBlock,
    Java20Parser.RULE_switchBlockStatementGroup,
    Java20Parser.RULE_switchExpression,
    Java20Parser.RULE_tryStatement,
    Java20Parser.RULE_tryWithResourcesStatement,
    Java20Parser.RULE_catchClause,
    Java20Parser.RULE_finallyBlock,
    Java20Parser.RULE_synchronizedStatement,
    Java20Parser.RULE_labeledStatement,
    Java20Parser.RULE_labeledStatementNoShortIf,
    Java20Parser.RULE_methodDeclaration,
    Java20Parser.RULE_constructorDeclaration,
    Java20Parser.RULE_classBody,
    Java20Parser.RULE_classDeclaration,
    Java20Parser.RULE_normalClassDeclaration,
    Java20Parser.RULE_enumBody,
    Java20Parser.RULE_interfaceBody,
    Java20Parser.RULE_recordBody,
    Java20Parser.RULE_lambdaBody,
    Java20Parser.RULE_methodBody,
    Java20Parser.RULE_constructorBody,
    Java20Parser.RULE_instanceInitializer,
    Java20Parser.RULE_staticInitializer,
    Java20Parser.RULE_ordinaryCompilationUnit,
}

# The four loop statements are interchangeable ways to write the same loop
# (`for` <-> `while` rewrites are common clones), so they share one label.
# do-while keeps its own: its body always runs once.
CONTROL_EQUIVALENCE_RULE_INDICES = {
    Java20Parser.RULE_basicForStatement: "LOOP",
    Java20Parser.RULE_enhancedForStatement: "LOOP",
    Java20Parser.RULE_whileStatement: "LOOP",
}
RULE_ASSIGNMENT = Java20Parser.RULE_assignment
ASIGN_OP_NORMALIZED = dict()

# `x op= y` is rebuilt as `x = x op y` (see Java20ParserVisitorExtended):
# augmented-assignment token -> (rule of the binary operator, its operator
# token). Shift compound operators are left alone: `>>` is two tokens here.
AUG_ASSIGN_OPS = {
    Java20Lexer.ADD_ASSIGN: (Java20Parser.RULE_additiveExpression, Java20Lexer.ADD),
    Java20Lexer.SUB_ASSIGN: (Java20Parser.RULE_additiveExpression, Java20Lexer.SUB),
    Java20Lexer.MUL_ASSIGN: (Java20Parser.RULE_multiplicativeExpression, Java20Lexer.MUL),
    Java20Lexer.DIV_ASSIGN: (Java20Parser.RULE_multiplicativeExpression, Java20Lexer.DIV),
    Java20Lexer.MOD_ASSIGN: (Java20Parser.RULE_multiplicativeExpression, Java20Lexer.MOD),
    Java20Lexer.AND_ASSIGN: (Java20Parser.RULE_andExpression, Java20Lexer.BITAND),
    Java20Lexer.OR_ASSIGN: (Java20Parser.RULE_inclusiveOrExpression, Java20Lexer.BITOR),
    Java20Lexer.XOR_ASSIGN: (Java20Parser.RULE_exclusiveOrExpression, Java20Lexer.CARET),
}
# The grammar parses an assignment target and the same expression on the
# right-hand side under different rules for array access.
TARGET_AS_OPERAND = {
    Java20Parser.RULE_arrayAccess: Java20Parser.RULE_primaryNoNewArray,
    # `this.x` / `obj.f()` targets: fieldAccess collapses to primaryNoNewArray,
    # its operand twin is pNNA.
    Java20Parser.RULE_primaryNoNewArray: Java20Parser.RULE_pNNA,
}

# Only identifier text is noise. (The old list also dropped types, modifiers,
# annotations, loop headers, switch/throw/catch and every assignment: measured
# as pure signal loss, and the shared boilerplate is already neutralized by
# hashing.)
EXCLUDED_RULE_TYPES = {
    Java20Parser.RULE_identifier,
    Java20Parser.RULE_typeIdentifier,
    Java20Parser.RULE_unqualifiedMethodIdentifier,
}
