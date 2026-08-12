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
    """Detect assignment-shaped `expression` nodes and return a synthetic
    rule id for them, or None to leave the node's normal rule index alone.

    Why this exists: java_20 achieves most of its tolerance for cosmetic/
    computational differences by putting `assignment` (its own, separate
    grammar rule) in EXCLUDED_RULE_TYPES -- tree_processing.py's visitChildren
    drops that node AND its entire subtree (LHS, operator, RHS) outright.
    java_24's optimized grammar has no separate `assignment` rule to target
    the same way: assignment is one alternative of the unified `expression`
    rule (ruleIndex 99), and ANTLR gives it the SAME generated label,
    #BinaryOperatorExpression, as every other binary operator (+, -, *, ==,
    <, &&, ...) -- see grammars/Java24Parser.g4's `expression` rule, "Level 1,
    Assignment". Neither rule index nor label can isolate it.

    What DOES isolate it: the actual operator TOKEN. An assignment-shaped
    expression is `expression bop=(ASSIGN|ADD_ASSIGN|...) expression` --
    exactly 3 children, with child 1 being one of the 12 assignment-operator
    tokens. This is checked directly against children here (Python path) and
    mirrored in csim/native/src/java_24_bridge.cpp (native path) to relabel
    such nodes to SYNTHETIC_ASSIGNMENT_EXPR instead of RULE_expression,
    before either path builds the normalized tree -- so both paths agree,
    and csim/java_24/utils.py's EXCLUDED_RULE_TYPES can then drop
    SYNTHETIC_ASSIGNMENT_EXPR nodes (and their subtree) the same way
    java_20 drops RULE_assignment.

    Measured effect on jv_dataset/all_java/1037 (50 real files): false
    positives among pairs scoring >=0.8 similarity dropped from 532/570
    (93%) to 0/570 once this relabeling was combined with adding
    SYNTHETIC_ASSIGNMENT_EXPR to EXCLUDED_RULE_TYPES -- see CHANGELOG.md.
    """
    if node.getRuleIndex() != Java24Parser.RULE_expression:
        return None
    if node.getChildCount() != 3:
        return None
    mid = node.getChild(1)
    if isinstance(mid, TerminalNode) and mid.symbol.type in ASSIGNMENT_OPERATOR_TOKENS:
        return SYNTHETIC_ASSIGNMENT_EXPR
    return None

# Reconstructed 2026-08-12 to replace an earlier draft that (a) mistakenly
# hashed the grammar's root rule (compilationUnit), collapsing every file to
# a single node regardless of content, and (b) copied java_20/utils.py's
# rule-index tables verbatim despite java_24 using a structurally different
# grammar (grammars-v4/java/java, optimized/left-factored) instead of
# java_20's near-literal JLS transcription.
#
# Key structural difference discovered while rebuilding this: java_24 uses
# ANTLR labeled alternatives for `expression` (rule 99) and `statement`
# (rule 85) -- e.g. BinaryOperatorExpressionContext, MethodCallExpressionContext,
# UnaryOperatorExpressionContext all share getRuleIndex() == 99. Unlike
# java_20 (which has a distinct rule per JLS precedence level / statement
# kind), java_24 cannot distinguish these by rule label alone -- only by
# children shape. That means java_20's HASHED_RULE_INDICES entries for its
# separate precedence-chain rules (additiveExpression, multiplicativeExpression,
# ...) and its separate statement-kind rules (whileStatement, doStatement,
# switchStatement, tryWithResourcesStatement, assertStatement, ...) have NO
# safe 1:1 equivalent here: hashing java_24's `expression` or `statement`
# wholesale would collapse unrelated construct kinds together. Both are left
# unclassified (full structural comparison) rather than mapped.
#
# EXCLUDED_TOKEN_TYPES below is a direct, mechanical port of java_20's set:
# grammars-v4/java/java and grammars-v4/java/java20 share identical lexer
# token names, so this mapping carries over safely construct-by-construct.
# The rule-index sets (COLLAPSED/HASHED/EXCLUDED_RULE_TYPES) below are
# ported only where java_24 has a rule with equivalent scope/semantics to
# its java_20 counterpart -- verified by name and by reading
# grammars/Java24Parser.g4, not by index position.

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
}

EXCLUDE_CHILDRENS_FROM_RULE = dict()

# java_20 equivalents: importDeclaration (+ its now-inlined single/on-demand
# variants -- java_24's importDeclaration is already a single unsplit rule,
# so one entry here covers what took five in java_20), packageDeclaration,
# arrayInitializer. All three exist in java_24 with the same scope/semantics.
COLLAPSED_RULE_INDICES = {
    Java24Parser.RULE_packageDeclaration,
    Java24Parser.RULE_importDeclaration,
    Java24Parser.RULE_arrayInitializer,
}

# RULE_blockStatement (collapsed) was tried and REVERTED (2026-08-12). A
# greedy per-candidate search against a 25-pair unrelated sample from
# jv_dataset/all_java/1037 showed it raising the known-duplicate pairs to a
# perfect 1.00 (from 0.94) without raising that sample's worst case above
# 0.94 -- looked like a clean win. Re-checked against the FULL 1187-pair
# unrelated set from the same corpus: worst-case unrelated similarity also
# rose to a perfect 1.00 (70 unrelated pairs now score exactly 1.0, fully
# indistinguishable from real duplicates), and pairs scoring >=0.8 rose from
# 532 to 549. A 25-pair sample was not enough evidence to catch this --
# collapsing block-level content broadly enough makes several *different*
# simple programs (not just the intended near-duplicates) converge to
# identical trees once assignment payloads are already stripped by
# SYNTHETIC_ASSIGNMENT_EXPR. This is the same class of failure java_20's own
# corpus-tuner tooling exists to catch (see csim_native_parsers project
# memory) via much larger, cross-problem-diverse samples (hundreds of files
# spanning many different problems, not one problem's 50 submissions) --
# properly validating any further candidate here needs that scale, not an
# ad-hoc sample.

# Body-wrapping rules that exist in java_24 with equivalent scope to their
# java_20 counterpart (verified via grammars/Java24Parser.g4): each only
# wraps a class/interface/record/enum/method BODY, never gets skipped by
# visitChildren's single-child passthrough, and content-based hashing
# preserves genuine differences while collapsing internal noise, same
# reasoning as java_20/utils.py's equivalent set.
#
# Deliberately NOT included (no safe java_20-style equivalent -- see module
# docstring): compilationUnit (the grammar root -- hashing it collapses the
# entire file to one node, which is what broke the original draft).
#
# RULE_expression was tried and REJECTED (2026-08-12): java_20 achieves its
# high tolerance for cosmetic/computational differences mainly by DROPPING
# assignment/leftHandSide and forInit/forUpdate ENTIRELY (EXCLUDED_RULE_TYPES
# removes a node and all its children -- see tree_processing.py's
# visitChildren, `elif child.getRuleIndex() not in self.excluded_rule_types`).
# java_24 has no separate `assignment` rule to target the same way --
# assignment is one labeled alternative sharing ruleIndex 99 with every other
# expression kind, so hashing/excluding rule 99 wholesale was tried and
# rejected: it collapsed 33/50 unrelated files into one false-positive group
# on the real corpus (jv_dataset/all_java/1037) instead of the 3 small,
# correct groups java_20 finds. The rule 99 problem was solved differently
# instead -- see relabel_node() above and SYNTHETIC_ASSIGNMENT_EXPR in
# EXCLUDED_RULE_TYPES below, plus the matching relabeling in
# csim/native/src/java_24_bridge.cpp -- rather than by hashing/excluding the
# whole rule.
HASHED_RULE_INDICES = {
    Java24Parser.RULE_fieldDeclaration,
    Java24Parser.RULE_variableDeclarator,
    Java24Parser.RULE_localVariableDeclaration,
    Java24Parser.RULE_classBody,
    Java24Parser.RULE_methodDeclaration,
    Java24Parser.RULE_constructorDeclaration,
    Java24Parser.RULE_recordDeclaration,
    Java24Parser.RULE_interfaceDeclaration,
    Java24Parser.RULE_interfaceMethodDeclaration,
    Java24Parser.RULE_annotationTypeBody,
    Java24Parser.RULE_switchExpression,
}

CONTROL_EQUIVALENCE_RULE_INDICES = set()
# java_24 has no visitAssignment-style rewrite wired up in Visitors.py yet
# (java_20's ASIGN_OP_NORMALIZED is empty too -- this knob isn't populated
# for either language currently), so this mirrors that empty state rather
# than pointing at a rule that doesn't get used.
RULE_ASSIGNMENT = None
ASIGN_OP_NORMALIZED = dict()

# Direct java_20 equivalents that exist in java_24 with the same scope:
# identifiers/type-parameter machinery whose specific choice doesn't reflect
# an algorithmic difference (same "static container" reasoning as java_20's
# entries), plus a handful of always-mandatory wrapper rules.
EXCLUDED_RULE_TYPES = {
    Java24Parser.RULE_identifier,
    Java24Parser.RULE_typeIdentifier,
    Java24Parser.RULE_typeArguments,
    Java24Parser.RULE_typeArgument,
    Java24Parser.RULE_typeParameters,
    Java24Parser.RULE_typeParameter,
    Java24Parser.RULE_variableDeclaratorId,
    Java24Parser.RULE_annotation,
    Java24Parser.RULE_catchType,
    Java24Parser.RULE_finallyBlock,
    Java24Parser.RULE_resourceSpecification,
    # java_20 equivalent: forInit. java_24 keeps this as its own distinct
    # rule (unlike assignment), so no relabeling needed -- direct port.
    Java24Parser.RULE_forInit,
    # Engine-assisted: see relabel_node() above. Not a real grammar rule --
    # a synthetic id assigned to assignment-shaped `expression` nodes by
    # both the Python visitor (via relabel_node) and the native bridge
    # (csim/native/src/java_24_bridge.cpp), so this entry can drop them the
    # same way java_20's EXCLUDED_RULE_TYPES drops its separate
    # `assignment` rule.
    SYNTHETIC_ASSIGNMENT_EXPR,
}

# A second pass (2026-08-12) tried mapping the rest of java_20's 65-entry
# EXCLUDED_RULE_TYPES by grammar semantics -- unifying its per-context
# modifier rules (classModifier/fieldModifier/methodModifier/...) into
# java_24's shared `modifier`/`classOrInterfaceModifier`, plus a dozen
# direct 1:1 rule-name matches (receiverParameter, variableModifier,
# recordHeader, switchLabel, catchClause, ...). Measured on the real corpus
# (jv_dataset/all_java/1037) it was a NET REGRESSION, not an improvement:
# the known-duplicate pairs' similarity dropped from 0.94 to 0.83, while the
# worst unrelated-pair score rose from 0.95 to 0.90 -- MORE overlap between
# the two distributions, not less. Excluding more nodes shrinks every tree,
# but shrinks the true-duplicate pairs' remaining (already-small) edit
# distance's DENOMINATOR faster than its numerator, which can make relative
# similarity go down even as absolute differences stay flat. This is exactly
# why java_20's own config was built through per-candidate, corpus-measured
# safety+efficacy checks (see the corpus-tuner tooling referenced in
# csim_native_parsers project memory) rather than by porting entries in
# batches and eyeballing the aggregate effect -- each entry's interaction
# with every other needs individual verification. Reverted; left as a
# documented note rather than silently dropped, since the specific mappings
# identified (modifier unification, receiverParameter, variableModifier,
# recordHeader/recordComponentList/recordComponent, interfaceMethodModifier,
# defaultValue, switchBlockStatementGroup, switchLabel, catchClause,
# constDeclaration, typeTypeOrVoid for java_20's `result`, typeList for
# `interfaceTypeList`) are still valid CANDIDATES for a future corpus-tuner
# pass -- they were reverted for lacking verified safety, not for being
# wrong mappings.
