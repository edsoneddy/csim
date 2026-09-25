from .KotlinLexer import KotlinLexer
from .KotlinParser import KotlinParser
from antlr4 import Token

# First integration pass (2026-08-20) for grammars-v4/kotlin/kotlin. Unlike
# java_24/python_3, this grammar has NO ANTLR labeled alternatives anywhere
# (verified: zero `#Label` occurrences in KotlinParser.g4) -- every rule has
# its own dedicated rule index, so none of the relabel_node()/synthetic-id
# machinery those two languages need applies here. get_relabel_fn() in
# csim/utils.py has no "kotlin" branch and returns None, which is correct,
# not an oversight.
#
# Also unlike python_3's monolithic `expr` (which merges an entire
# precedence chain into one left-recursive rule and required hashing it just
# to keep trees a sane size -- see csim/python_3/utils.py), Kotlin's
# expression grammar is already split one rule per precedence level
# (disjunction -> conjunction -> equalityComparison -> comparison ->
# namedInfix -> elvisExpression -> infixFunctionCall -> rangeExpression ->
# additiveExpression -> multiplicativeExpression -> typeRHS ->
# prefixUnaryExpression -> postfixUnaryExpression -> atomicExpression),
# closer in shape to python_3_13's finer-grained style. tree_processing.py's
# visitChildren already compresses any single-child hop through this chain
# (the common case when a lower-precedence operator isn't used), so no
# HASHED_RULE_INDICES entry is needed here for tractability the way
# python_3's `expr` needed one -- revisit only if a real corpus shows the
# tree-edit-distance step becoming a bottleneck.
#
# IMPORTANT CAVEAT: there is still no *real* Kotlin corpus. The hashing policy
# (expression "islands" only, never the control-flow skeleton -- see
# HASHED_RULE_INDICES below and docs/pruning_fidelity.md) was measured against
# the unpruned tree on a synthetic judge-style corpus generated for this
# purpose (jv-umsa-dataset/all_kotlin: 12 problems x 3 algorithms x 3
# variants), so treat the numbers as indicative. A real Kotlin corpus should
# drive the next pass.

EXCLUDED_TOKEN_TYPES = {
    # Structural / whitespace / comment tokens. WS is `-> skip` in the
    # lexer (never reaches a token at all) and comments go to the HIDDEN
    # channel (never reach the parse tree) -- only NL is both a real,
    # default-channel token AND structurally mandatory (Kotlin's `semi`/
    # `anysemi` rules consume it for statement-termination inference), so
    # it's the only whitespace-shaped token that needs excluding here.
    Token.EOF,
    KotlinLexer.NL,
    # Grouping / punctuation
    KotlinLexer.LPAREN,
    KotlinLexer.RPAREN,
    KotlinLexer.LSQUARE,
    KotlinLexer.RSQUARE,
    KotlinLexer.LCURL,
    KotlinLexer.RCURL,
    KotlinLexer.COMMA,
    KotlinLexer.DOT,
    KotlinLexer.COLON,
    KotlinLexer.SEMICOLON,
    KotlinLexer.DOUBLE_SEMICOLON,
    KotlinLexer.COLONCOLON,
    KotlinLexer.Q_COLONCOLON,
    KotlinLexer.ARROW,
    KotlinLexer.DOUBLE_ARROW,
    KotlinLexer.HASH,
    KotlinLexer.AT,
    KotlinLexer.SINGLE_QUOTE,
    # String-template/string-literal delimiter punctuation (not content --
    # LineStrText/MultiLineStrText, the actual string contents, are left
    # alone, same treatment as other languages' StringLiteral tokens).
    KotlinLexer.QUOTE_OPEN,
    KotlinLexer.QUOTE_CLOSE,
    KotlinLexer.TRIPLE_QUOTE_OPEN,
    KotlinLexer.TRIPLE_QUOTE_CLOSE,
    KotlinLexer.LineStrExprStart,
    KotlinLexer.MultiLineStrExprStart,
    # Identifier text itself doesn't carry algorithmic meaning (same
    # reasoning as excluding RULE_identifier/RULE_simpleIdentifier below --
    # the bare token also appears directly in a few contexts, e.g. labels).
    KotlinLexer.Identifier,
    KotlinLexer.LabelReference,
    KotlinLexer.LabelDefinition,
    KotlinLexer.FieldIdentifier,
    # Bare assignment sign: the surrounding `expression`/`assignmentOperator`
    # structure already marks this as an assignment; the compound-assignment
    # tokens (ADD_ASSIGNMENT, SUB_ASSIGNMENT, ...) are left alone since they
    # carry real extra meaning (shorthand for `x = x op y`) that a plain `=`
    # doesn't -- mirrors python_3's ASSIGN-only exclusion.
    KotlinLexer.ASSIGNMENT,
    # Boolean connectives: disjunction/conjunction are dedicated rules with
    # exactly one possible operator each (DISJ, CONJ respectively), so the
    # wrapping rule index alone already distinguishes `||` from `&&` --
    # excluding the operator token itself loses no information. This does
    # NOT extend to comparisonOperator/equalityOperation/additiveOperator/
    # multiplicativeOperation: those are shared sub-rules with MULTIPLE
    # alternatives (e.g. additiveOperator: ADD | SUB), so their actual
    # operator token is the only thing distinguishing the alternatives and
    # must stay.
    KotlinLexer.DISJ,
    KotlinLexer.CONJ,
}

EXCLUDE_CHILDRENS_FROM_RULE = dict()

# "Static container" rules whose specific spelled-out content (which names
# were imported, what the package is called) doesn't reflect an algorithmic
# difference -- same reasoning as java_24's packageDeclaration/
# importDeclaration and python_3's dotted_name family.
COLLAPSED_RULE_INDICES = {
    KotlinParser.RULE_packageHeader,
    KotlinParser.RULE_importList,
    KotlinParser.RULE_importHeader,
    KotlinParser.RULE_importAlias,
}

# Hashing policy (see docs/pruning_fidelity.md): only "islands" -- expressions,
# property declarations, call arguments and parameter lists that contain no
# control flow -- collapse to a digest. Function/class bodies, blocks, `if`,
# `when`, `try` and loops stay as real nodes so the program's skeleton
# survives. The previous policy hashed functionBody/classBody whole (one node
# per function). Kotlin has no real-submission corpus, so the island list was
# derived on the synthetic judge-style corpus in jv-umsa-dataset/all_kotlin
# (12 problems x 3 algorithms x 3 variants; two disjoint problem halves).
HASHED_RULE_INDICES = {
    KotlinParser.RULE_expression,
    KotlinParser.RULE_disjunction,
    KotlinParser.RULE_conjunction,
    KotlinParser.RULE_equalityComparison,
    KotlinParser.RULE_comparison,
    KotlinParser.RULE_namedInfix,
    KotlinParser.RULE_elvisExpression,
    KotlinParser.RULE_infixFunctionCall,
    KotlinParser.RULE_rangeExpression,
    KotlinParser.RULE_additiveExpression,
    KotlinParser.RULE_multiplicativeExpression,
    KotlinParser.RULE_prefixUnaryExpression,
    KotlinParser.RULE_postfixUnaryExpression,
    KotlinParser.RULE_postfixUnaryOperation,
    KotlinParser.RULE_callSuffix,
    KotlinParser.RULE_valueArguments,
    KotlinParser.RULE_functionLiteral,
    KotlinParser.RULE_lambdaParameters,
    KotlinParser.RULE_functionValueParameters,
    KotlinParser.RULE_propertyDeclaration,
    KotlinParser.RULE_multiVariableDeclaration,
    KotlinParser.RULE_preamble,
}

# A hashed rule is NOT collapsed if its subtree contains one of these (e.g. a
# lambda whose body holds an `if` or a loop).
STRUCTURAL_RULE_INDICES = {
    KotlinParser.RULE_block,
    KotlinParser.RULE_ifExpression,
    KotlinParser.RULE_whenExpression,
    KotlinParser.RULE_whenEntry,
    KotlinParser.RULE_tryExpression,
    KotlinParser.RULE_catchBlock,
    KotlinParser.RULE_finallyBlock,
    KotlinParser.RULE_loopExpression,
    KotlinParser.RULE_forExpression,
    KotlinParser.RULE_whileExpression,
    KotlinParser.RULE_doWhileExpression,
    KotlinParser.RULE_functionDeclaration,
    KotlinParser.RULE_functionBody,
    KotlinParser.RULE_classDeclaration,
    KotlinParser.RULE_classBody,
    KotlinParser.RULE_objectDeclaration,
    KotlinParser.RULE_controlStructureBody,
    KotlinParser.RULE_kotlinFile,
    KotlinParser.RULE_topLevelObject,
    KotlinParser.RULE_secondaryConstructor,
    KotlinParser.RULE_anonymousInitializer,
}

# `for` and `while` are interchangeable ways to write the same loop (a common
# clone rewrite), so they share one label; do-while keeps its own.
CONTROL_EQUIVALENCE_RULE_INDICES = {
    KotlinParser.RULE_forExpression: "LOOP",
    KotlinParser.RULE_whileExpression: "LOOP",
}

RULE_ASSIGNMENT = None
ASIGN_OP_NORMALIZED = dict()

# `x op= y` is rebuilt as `x = x op y` (KotlinParserVisitorExtended): augmented
# token -> (rule of the binary operator, its operator token). In this grammar
# an assignment is a plain `expression`: `disjunction assignmentOperator disjunction`.
AUG_ASSIGN_OPS = {
    KotlinLexer.ADD_ASSIGNMENT: (KotlinParser.RULE_additiveExpression, KotlinLexer.ADD),
    KotlinLexer.SUB_ASSIGNMENT: (KotlinParser.RULE_additiveExpression, KotlinLexer.SUB),
    KotlinLexer.MULT_ASSIGNMENT: (KotlinParser.RULE_multiplicativeExpression, KotlinLexer.MULT),
    KotlinLexer.DIV_ASSIGNMENT: (KotlinParser.RULE_multiplicativeExpression, KotlinLexer.DIV),
    KotlinLexer.MOD_ASSIGNMENT: (KotlinParser.RULE_multiplicativeExpression, KotlinLexer.MOD),
}

EXCLUDED_RULE_TYPES = {
    # Identifier nodes: which name was chosen doesn't reflect an algorithmic
    # difference.
    KotlinParser.RULE_identifier,
    KotlinParser.RULE_simpleIdentifier,
    KotlinParser.RULE_labelDefinition,
    # Pure statement-terminator noise: `semi`/`anysemi` exist only to
    # consume NL/SEMICOLON tokens for statement-boundary inference (see
    # grammars/KotlinParser.g4) and carry no content of their own once those
    # tokens are excluded above -- dropping the rule itself (rather than
    # leaving a degenerate always-empty node) avoids cluttering every
    # statement boundary with a content-free marker node.
    KotlinParser.RULE_semi,
    KotlinParser.RULE_anysemi,
    # Generic-type and annotation metadata: same "static container"
    # reasoning as java_24's equivalent entries (RULE_typeArguments,
    # RULE_typeParameters, RULE_annotation, ...) -- which specific type
    # parameter/argument or annotation was used doesn't reflect the
    # algorithmic structure being compared.
    KotlinParser.RULE_typeParameters,
    KotlinParser.RULE_typeParameter,
    KotlinParser.RULE_typeArguments,
    KotlinParser.RULE_typeProjection,
    KotlinParser.RULE_typeProjectionModifierList,
    KotlinParser.RULE_annotations,
    KotlinParser.RULE_annotation,
    KotlinParser.RULE_annotationList,
    KotlinParser.RULE_annotationUseSiteTarget,
    KotlinParser.RULE_unescapedAnnotation,
    KotlinParser.RULE_fileAnnotation,
    KotlinParser.RULE_fileAnnotations,
}
