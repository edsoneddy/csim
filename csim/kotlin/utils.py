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
# IMPORTANT CAVEAT: there is no Kotlin corpus in jv_dataset (the project's
# real-submission benchmark set) to tune or validate grouping precision
# against, unlike every other language here. The tables below follow the
# same *categories* of exclusion already validated for other languages
# (structural punctuation, identifier text, import/package plumbing,
# body-wrapping content) but have NOT been corpus-measured for false-
# positive/false-negative rates the way java_24's SYNTHETIC_ASSIGNMENT_EXPR
# or python_3's relabel_node() fixes were (see those modules' change
# history). Treat this as a reasonable, principled starting point, not a
# tuned config -- a real Kotlin corpus should drive the next pass, the same
# way jv_dataset drove every other language's tuning.

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

# Body-wrapping content, hashed to a single digest for tree-edit-distance
# tractability on real (potentially large) submissions -- same tradeoff and
# reasoning as java_24's classBody/methodDeclaration/... entries: each
# instance still gets its own node (so e.g. a class with one matching method
# among several differing ones remains partially comparable at the
# class-body level), but internal differences within one body are all-or-
# nothing rather than finely diffed.
#
# Deliberately NOT hashing `block` itself: `block` is the generic `{ ... }`
# wrapper reused for if/while/for/try bodies too (see controlStructureBody),
# not just function/class bodies -- hashing it wholesale would be the same
# over-aggressive collapse java_24 tried (RULE_blockStatement) and reverted
# after it merged unrelated files into false-positive groups on the real
# corpus (see csim/java_24/utils.py). Hashing at the functionBody/classBody/
# propertyDeclaration granularity keeps signatures (function name, params,
# property name, type) individually comparable while still bounding how
# deep TED has to recurse into any one implementation.
HASHED_RULE_INDICES = {
    KotlinParser.RULE_classBody,
    KotlinParser.RULE_enumClassBody,
    KotlinParser.RULE_functionBody,
    KotlinParser.RULE_propertyDeclaration,
    KotlinParser.RULE_multiVariableDeclaration,
}

# Not populated yet -- no language in csim currently uses this hook (java_24
# and python_3 both leave it empty too). Left as a documented future knob,
# not a gap specific to Kotlin.
CONTROL_EQUIVALENCE_RULE_INDICES = set()

# No visitAssignment-style rewrite wired up in Visitors.py for this language
# (matching java_24/python_3's current "not populated yet" state). Kotlin's
# `expression: disjunction (assignmentOperator disjunction)*` is also a
# repetition rather than always-3-children like the other languages'
# assignment rule, so porting the existing visitAssignment pattern directly
# wouldn't even apply cleanly -- would need its own shape-aware rewrite if
# ever added.
RULE_ASSIGNMENT = None
ASIGN_OP_NORMALIZED = dict()

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
