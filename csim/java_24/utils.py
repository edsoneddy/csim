from .Java24Lexer import Java24Lexer
from .Java24Parser import Java24Parser
from antlr4 import Token
from antlr4.tree.Tree import TerminalNode

# Synthetic rule id for assignment-shaped `expression` nodes -- see
# relabel_node() below. Must not collide with any real rule index (java_24's
# grammar has 129 rules, 0-128) or with terminal labels (which get
# TOKEN_TYPE_OFFSET=1000 added in csim/utils.py/tree_processing.py). 200 is
# clear of both ranges.
SYNTHETIC_ASSIGNMENT_EXPR = 200

# Synthetic ids for the control-flow alternatives of the unified `statement`
# rule (they all share RULE_statement with `return`, `break`, `x;`, ...), so
# STRUCTURAL_RULE_INDICES/CONTROL_EQUIVALENCE_RULE_INDICES can single them out.
# Python-side only: relabel_node() runs on both the Python and native parse
# trees (it only reads children), unlike the assignment id which the native
# bridge also stamps.
SYNTHETIC_IF_STMT = 201
SYNTHETIC_FOR_STMT = 202
SYNTHETIC_WHILE_STMT = 203
SYNTHETIC_DO_STMT = 204
SYNTHETIC_TRY_STMT = 205
SYNTHETIC_SWITCH_STMT = 206
SYNTHETIC_SYNC_STMT = 207
SYNTHETIC_LABELED_STMT = 208

# Readable names for `csim tree` output.
SYNTHETIC_NAMES = {
    SYNTHETIC_ASSIGNMENT_EXPR: "assignment_expr",
    SYNTHETIC_IF_STMT: "if_stmt",
    SYNTHETIC_FOR_STMT: "for_stmt",
    SYNTHETIC_WHILE_STMT: "while_stmt",
    SYNTHETIC_DO_STMT: "do_stmt",
    SYNTHETIC_TRY_STMT: "try_stmt",
    SYNTHETIC_SWITCH_STMT: "switch_stmt",
    SYNTHETIC_SYNC_STMT: "synchronized_stmt",
    SYNTHETIC_LABELED_STMT: "labeled_stmt",
}

_STATEMENT_KEYWORDS = {
    Java24Lexer.IF: SYNTHETIC_IF_STMT,
    Java24Lexer.FOR: SYNTHETIC_FOR_STMT,
    Java24Lexer.WHILE: SYNTHETIC_WHILE_STMT,
    Java24Lexer.DO: SYNTHETIC_DO_STMT,
    Java24Lexer.TRY: SYNTHETIC_TRY_STMT,
    Java24Lexer.SWITCH: SYNTHETIC_SWITCH_STMT,
    Java24Lexer.SYNCHRONIZED: SYNTHETIC_SYNC_STMT,
}

# The `bop` token that distinguishes an assignment-shaped `expression` from
# every other binary operator sharing the same rule index and the same
# #BinaryOperatorExpression label (see relabel_node()'s docstring).
ASSIGNMENT_OPERATOR_TOKENS = {
    Java24Lexer.ASSIGN,
    Java24Lexer.ADD_ASSIGN,
    Java24Lexer.SUB_ASSIGN,
    Java24Lexer.MUL_ASSIGN,
    Java24Lexer.DIV_ASSIGN,
    Java24Lexer.AND_ASSIGN,
    Java24Lexer.OR_ASSIGN,
    Java24Lexer.XOR_ASSIGN,
    Java24Lexer.MOD_ASSIGN,
    Java24Lexer.LSHIFT_ASSIGN,
    Java24Lexer.RSHIFT_ASSIGN,
    Java24Lexer.URSHIFT_ASSIGN,
}


def relabel_node(node):
    """Return a synthetic rule id for nodes that share a rule index with
    unrelated alternatives, or None to leave the node's normal rule index alone.

    java_24's grammar is optimized/left-factored: `expression` and `statement`
    are single rules whose labeled alternatives (#BinaryOperatorExpression,
    #MethodCallExpression, ... / if, for, while, return, `x;`, ...) ALL share
    one rule index, so neither the rule index nor the ANTLR label can tell an
    assignment from `a + b`, or an `if` from a `return`. What does tell them
    apart is the children shape, checked here (this function only reads
    children, so it works on both the Python and the native parse tree):

    * `expression` with exactly 3 children whose middle one is an assignment
      operator token -> SYNTHETIC_ASSIGNMENT_EXPR. That id is hashed as an
      island (HASHED_RULE_INDICES) and is what the visitor rewrites for
      `x op= y` (Visitors.py). The native bridge
      (csim/native/src/java_24_bridge.cpp) stamps the same id.
    * `statement` starting with `if`/`for`/`while`/`do`/`try`/`switch`/
      `synchronized`, or `identifier :` (labeled) -> SYNTHETIC_*_STMT, so
      STRUCTURAL_RULE_INDICES (control flow is never hashed) and
      CONTROL_EQUIVALENCE_RULE_INDICES (for/while share one label) can target
      them.
    """
    if node.getRuleIndex() == Java24Parser.RULE_statement:
        if node.getChildCount() == 0:
            return None
        first = node.getChild(0)
        if isinstance(first, TerminalNode):
            return _STATEMENT_KEYWORDS.get(first.symbol.type)
        if (
            node.getChildCount() == 3
            and first.getRuleIndex() == Java24Parser.RULE_identifier
            and isinstance(node.getChild(1), TerminalNode)
            and node.getChild(1).symbol.type == Java24Lexer.COLON
        ):
            return SYNTHETIC_LABELED_STMT
        return None
    if node.getRuleIndex() != Java24Parser.RULE_expression:
        return None
    if node.getChildCount() != 3:
        return None
    mid = node.getChild(1)
    if isinstance(mid, TerminalNode) and mid.symbol.type in ASSIGNMENT_OPERATOR_TOKENS:
        return SYNTHETIC_ASSIGNMENT_EXPR
    return None

# Policy notes (see docs/pruning_fidelity.md): only expression/declaration
# "islands" are hashed and the control-flow skeleton never is. An earlier draft
# hashed the grammar root (compilationUnit), which collapses every file to a
# single node; the version after it hashed classBody/methodDeclaration and
# dropped every assignment, which left ~1-5 nodes per file.
#
# EXCLUDED_TOKEN_TYPES below is a direct, mechanical port of java_20's set:
# grammars-v4/java/java and grammars-v4/java/java20 share identical lexer
# token names, so this mapping carries over safely construct-by-construct.

EXCLUDED_TOKEN_TYPES = {
    # Structural / whitespace / comment tokens.
    Token.EOF,
    Java24Lexer.WS,
    Java24Lexer.COMMENT,
    Java24Lexer.LINE_COMMENT,
    # Grouping / punctuation
    Java24Lexer.LPAREN,
    Java24Lexer.RPAREN,
    Java24Lexer.LBRACE,
    Java24Lexer.RBRACE,
    Java24Lexer.LBRACK,
    Java24Lexer.RBRACK,
    Java24Lexer.SEMI,
    Java24Lexer.COMMA,
    Java24Lexer.DOT,
    Java24Lexer.COLON,
    Java24Lexer.COLONCOLON,
    # Arrow
    Java24Lexer.ARROW,
    # Single-operator precedence-chain connectives
    Java24Lexer.BITAND,
    Java24Lexer.CARET,
    Java24Lexer.BITOR,
    Java24Lexer.AND,
    Java24Lexer.OR,
    # Ternary '?'
    Java24Lexer.QUESTION,
    # Statement keywords
    Java24Lexer.IF,
    Java24Lexer.ELSE,
    Java24Lexer.WHILE,
    Java24Lexer.DO,
    Java24Lexer.SWITCH,
    Java24Lexer.SYNCHRONIZED,
    Java24Lexer.TRY,
    Java24Lexer.CATCH,
    Java24Lexer.BREAK,
    Java24Lexer.CONTINUE,
    Java24Lexer.CASE,
    Java24Lexer.DEFAULT,
    # Type-declaration keywords
    Java24Lexer.CLASS,
    Java24Lexer.ENUM,
    Java24Lexer.INTERFACE,
    Java24Lexer.RECORD,
    # NEW
    Java24Lexer.NEW,
    # EXTENDS / IMPLEMENTS / THROWS: always wrap mandatory real type-list
    Java24Lexer.EXTENDS,
    Java24Lexer.IMPLEMENTS,
    Java24Lexer.THROWS,
    # Additional tokens
    Java24Lexer.PERMITS,
    Java24Lexer.RETURN,
    Java24Lexer.STATIC,
    Java24Lexer.THROW,
    Java24Lexer.AT,
    Java24Lexer.ASSIGN,
    Java24Lexer.GT,
    Java24Lexer.LT,
    Java24Lexer.INC,
    Java24Lexer.DEC,
    Java24Lexer.EXPORTS,
    Java24Lexer.MODULE,
    Java24Lexer.OPEN,
    Java24Lexer.OPENS,
    Java24Lexer.PROVIDES,
    Java24Lexer.REQUIRES,
    Java24Lexer.TO,
    Java24Lexer.WITH,
    Java24Lexer.YIELD,
    Java24Lexer.ASSERT,
    Java24Lexer.FINALLY,
    Java24Lexer.FOR,
    Java24Lexer.THIS,
    Java24Lexer.ELLIPSIS,
    Java24Lexer.BANG,
    Java24Lexer.TILDE,
    # Built-in type keywords: which primitive type was declared/returned is not
    # structure (`int f` vs `void g` should line up).
    Java24Lexer.VOID,
    Java24Lexer.INT,
    Java24Lexer.LONG,
    Java24Lexer.SHORT,
    Java24Lexer.BYTE,
    Java24Lexer.CHAR,
    Java24Lexer.DOUBLE,
    Java24Lexer.FLOAT,
    Java24Lexer.BOOLEAN,
}

EXCLUDE_CHILDRENS_FROM_RULE = dict()

COLLAPSED_RULE_INDICES = {
    Java24Parser.RULE_packageDeclaration,
    Java24Parser.RULE_importDeclaration,
    Java24Parser.RULE_arrayInitializer,
}

# Hashing policy (see docs/pruning_fidelity.md and java_20/utils.py): only
# "islands" -- expressions, declarations, loop headers and parameter lists that
# contain no control flow -- collapse to a digest. `expression` is java_24's
# unified operator rule, so hashing it whole is safe now: it is only hashed
# when its subtree holds nothing in STRUCTURAL_RULE_INDICES, and the digest
# covers every operator/operand label below it. The previous policy hashed
# classBody/methodDeclaration/... (the whole program in one or two nodes) and
# dropped every assignment, which collapsed files to a handful of nodes.
HASHED_RULE_INDICES = {
    Java24Parser.RULE_expression,
    Java24Parser.RULE_expressionList,
    SYNTHETIC_ASSIGNMENT_EXPR,
    Java24Parser.RULE_creator,
    Java24Parser.RULE_arrayCreatorRest,
    Java24Parser.RULE_lambdaExpression,
    Java24Parser.RULE_forControl,
    Java24Parser.RULE_enhancedForControl,
    Java24Parser.RULE_localVariableDeclaration,
    Java24Parser.RULE_fieldDeclaration,
    Java24Parser.RULE_variableDeclarator,
    Java24Parser.RULE_variableDeclarators,
    Java24Parser.RULE_formalParameter,
    Java24Parser.RULE_formalParameterList,
    Java24Parser.RULE_formalParameters,
    Java24Parser.RULE_typeArguments,
    Java24Parser.RULE_classType,
}

# A hashed rule is NOT collapsed if its subtree contains one of these (e.g. a
# lambda or switch expression with a block body).
STRUCTURAL_RULE_INDICES = {
    Java24Parser.RULE_block,
    Java24Parser.RULE_switchBlockStatementGroup,
    Java24Parser.RULE_switchLabeledRule,
    Java24Parser.RULE_switchExpression,
    Java24Parser.RULE_catchClause,
    Java24Parser.RULE_finallyBlock,
    Java24Parser.RULE_methodDeclaration,
    Java24Parser.RULE_constructorDeclaration,
    Java24Parser.RULE_genericMethodDeclaration,
    Java24Parser.RULE_genericConstructorDeclaration,
    Java24Parser.RULE_compactConstructorDeclaration,
    Java24Parser.RULE_classBody,
    Java24Parser.RULE_classDeclaration,
    Java24Parser.RULE_interfaceDeclaration,
    Java24Parser.RULE_interfaceBody,
    Java24Parser.RULE_enumDeclaration,
    Java24Parser.RULE_recordDeclaration,
    Java24Parser.RULE_recordBody,
    Java24Parser.RULE_methodBody,
    Java24Parser.RULE_lambdaBody,
    Java24Parser.RULE_annotationTypeBody,
    Java24Parser.RULE_typeDeclaration,
    Java24Parser.RULE_compilationUnit,
    SYNTHETIC_IF_STMT,
    SYNTHETIC_FOR_STMT,
    SYNTHETIC_WHILE_STMT,
    SYNTHETIC_DO_STMT,
    SYNTHETIC_TRY_STMT,
    SYNTHETIC_SWITCH_STMT,
    SYNTHETIC_SYNC_STMT,
    SYNTHETIC_LABELED_STMT,
}

# `for` and `while` are interchangeable ways to write the same loop (a common
# clone rewrite), so they share one label; do-while keeps its own.
CONTROL_EQUIVALENCE_RULE_INDICES = {
    SYNTHETIC_FOR_STMT: "LOOP",
    SYNTHETIC_WHILE_STMT: "LOOP",
}
RULE_ASSIGNMENT = SYNTHETIC_ASSIGNMENT_EXPR
ASIGN_OP_NORMALIZED = dict()

# `x op= y` is rebuilt as `x = x op y` (Java24ParserVisitorExtended): the
# augmented token -> the binary operator token of the expanded form. Shifts are
# left alone (`>>` is several tokens in this grammar).
AUG_ASSIGN_OPS = {
    Java24Lexer.ADD_ASSIGN: Java24Lexer.ADD,
    Java24Lexer.SUB_ASSIGN: Java24Lexer.SUB,
    Java24Lexer.MUL_ASSIGN: Java24Lexer.MUL,
    Java24Lexer.DIV_ASSIGN: Java24Lexer.DIV,
    Java24Lexer.MOD_ASSIGN: Java24Lexer.MOD,
    Java24Lexer.AND_ASSIGN: Java24Lexer.BITAND,
    Java24Lexer.OR_ASSIGN: Java24Lexer.BITOR,
    Java24Lexer.XOR_ASSIGN: Java24Lexer.CARET,
}

# Only identifier text is noise (the old set also dropped types, annotations,
# for-init, resources and -- via SYNTHETIC_ASSIGNMENT_EXPR -- every assignment).
EXCLUDED_RULE_TYPES = {
    Java24Parser.RULE_identifier,
    Java24Parser.RULE_typeIdentifier,
    # Modifiers (`public`, `static`, `final`, ...): declaration boilerplate that
    # differs between equivalent programs and that java_20 folds into its hashed
    # methodHeader. Without this a wrapped/extracted method scores ~0.64 instead
    # of ~0.7+ on the controlled clone set (see docs/pruning_fidelity.md).
    Java24Parser.RULE_classOrInterfaceModifier,
    Java24Parser.RULE_modifier,
}
