from .CLexer import CLexer
from .CParser import CParser
from antlr4 import Token

# First integration pass (2026-08-20) for grammars-v4/c. Like Kotlin (see
# csim/kotlin/utils.py), this grammar has NO ANTLR labeled alternatives
# anywhere (verified: zero `#Label` occurrences in CParser.g4), so no
# relabel_node()/synthetic-id machinery is needed -- every rule already has a
# unique rule index. get_relabel_fn() in csim/utils.py has no "c" branch and
# returns None, which is correct, not an oversight.
#
# Like Kotlin (and unlike python_3's monolithic `expr`), C's expression
# grammar is already split one rule per ISO-C precedence level
# (multiplicativeExpression -> additiveExpression -> shiftExpression ->
# relationalExpression -> equalityExpression -> andExpression ->
# exclusiveOrExpression -> inclusiveOrExpression -> logicalAndExpression ->
# logicalOrExpression -> conditionalExpression -> assignmentExpression).
# tree_processing.py's visitChildren already compresses any single-child hop
# through this chain, so no HASHED_RULE_INDICES entry is needed here for
# tractability -- revisit only if a real corpus shows the tree-edit-distance
# step becoming a bottleneck.
#
# IMPORTANT CAVEAT: there is no C corpus in jv_dataset (the project's
# real-submission benchmark set) to tune or validate grouping precision
# against, unlike Java/C++/Python. The tables below follow the same
# *categories* of exclusion already validated for other languages
# (structural punctuation, identifier text, body-wrapping content) but have
# NOT been corpus-measured for false-positive/false-negative rates. Treat
# this as a reasonable, principled starting point, not a tuned config.
#
# IMPORTANT CAVEAT #2: this grammar's lexer/parser base classes
# (CLexerBase/CParserBase, vendored into this same package) default to
# `--nopp` (no real preprocessing) for reasons documented in
# grammars/CLexerBase.h -- `#include`/`#define`/etc. lines are swallowed as
# hidden tokens, unexpanded, rather than resolved. This means macro-dependent
# code (token-pasting tricks, macros used for control flow) can genuinely
# fail to parse or parse differently than a real compiler would see it -- see
# the C spike writeup in project memory for the concrete failure cases found
# against grammars-v4's own c-testsuite. Real judge submissions essentially
# never rely on those tricks, but it's a real, known limitation, not
# something these rule tables can paper over.

EXCLUDED_TOKEN_TYPES = {
    # Structural tokens. Whitespace/comments/#include-etc. lines never reach
    # the parse tree at all (they're on the HIDDEN channel or a dedicated
    # non-default channel in the lexer -- see grammars/CLexer.g4's
    # Whitespace/Newline/Directive/LineDirective/MultiLineMacro rules), so
    # nothing needs excluding for them here.
    Token.EOF,
    # Grouping / punctuation
    CLexer.LeftParen,
    CLexer.RightParen,
    CLexer.LeftBracket,
    CLexer.RightBracket,
    CLexer.LeftBrace,
    CLexer.RightBrace,
    CLexer.Comma,
    CLexer.Dot,
    CLexer.Colon,
    CLexer.Semi,
    CLexer.Arrow,
    # Identifier text itself doesn't carry algorithmic meaning (same
    # reasoning as excluding RULE_typedefName/RULE_enumerationConstant
    # below -- the bare token also appears directly in a few contexts).
    CLexer.Identifier,
    # Bare assignment sign: `assignmentExpression` keeps the compound-
    # assignment tokens (StarAssign, PlusAssign, ...) visible since they
    # carry real extra meaning (shorthand for `x = x op y`) that a plain `=`
    # doesn't -- mirrors python_3/kotlin's ASSIGN-only exclusion.
    CLexer.Assign,
    # Single-operator precedence-chain connectives: andExpression,
    # exclusiveOrExpression, inclusiveOrExpression, logicalAndExpression, and
    # logicalOrExpression are EACH a dedicated rule with exactly one possible
    # operator (&, ^, |, &&, || respectively -- see grammars/CParser.g4), so
    # the wrapping rule index alone already distinguishes them; excluding the
    # operator token itself loses no information. This does NOT extend to
    # multiplicativeExpression/additiveExpression/shiftExpression/
    # relationalExpression/equalityExpression: those are shared rules with
    # MULTIPLE operator alternatives each (e.g. additiveExpression handles
    # both `+` and `-`), so their operator token is the only thing
    # distinguishing the alternatives and must stay.
    CLexer.And,
    CLexer.Caret,
    CLexer.Or,
    CLexer.AndAnd,
    CLexer.OrOr,
}

EXCLUDE_CHILDRENS_FROM_RULE = dict()

# "Static container" rule whose specific spelled-out content (which
# parameter names were listed) doesn't reflect an algorithmic difference --
# same reasoning as java_24/kotlin's import/package-plumbing entries. Kept as
# a COLLAPSED marker rather than EXCLUDED so a K&R-style old-declaration
# parameter list's mere PRESENCE (vs. absence) stays visible, since the
# grammar makes it optional in its parent rule.
COLLAPSED_RULE_INDICES = {
    CParser.RULE_identifierList,
}

# Body-wrapping content, hashed to a single digest for tree-edit-distance
# tractability on real (potentially large) submissions -- same tradeoff and
# reasoning as java_24/kotlin's equivalent entries.
#
# Deliberately NOT hashing `compoundStatement` itself: it's the generic
# `{ ... }` wrapper reused for if/while/for bodies too, not just function
# bodies (see grammars/CParser.g4's iterationStatement/selectionStatement) --
# hashing it wholesale would be the same over-aggressive collapse java_24
# tried (RULE_blockStatement) and reverted after it merged unrelated files
# into false-positive groups on the real corpus (see
# csim/java_24/utils.py). Hashing at the functionBody/initializer/
# structOrUnionSpecifier/enumSpecifier granularity keeps signatures
# (function name, params, struct/enum tag) individually comparable while
# still bounding how deep TED has to recurse into any one implementation or
# initializer value.
HASHED_RULE_INDICES = {
    CParser.RULE_functionBody,
    CParser.RULE_initializer,
    CParser.RULE_structOrUnionSpecifier,
    CParser.RULE_enumSpecifier,
}

# Not populated yet -- no language in csim currently uses this hook.
CONTROL_EQUIVALENCE_RULE_INDICES = set()

# No visitAssignment-style rewrite wired up in Visitors.py for this language
# (matching java_24/python_3/kotlin's current "not populated yet" state).
# C's `assignmentExpression` also has a different shape than the other
# languages' assignment rule (it's `conditionalExpression | unaryExpression
# assignementOperator assignmentExpression | DigitSequence` -- 1 or 3
# children depending on the alternative, plus an unrelated DigitSequence
# alternative for an old K&R quirk), so porting the existing visitAssignment
# pattern directly wouldn't apply cleanly even if this were populated.
RULE_ASSIGNMENT = None
ASIGN_OP_NORMALIZED = dict()

EXCLUDED_RULE_TYPES = {
    # Identifier-wrapping rules: which name was chosen doesn't reflect an
    # algorithmic difference. Both wrap a single Identifier token with no
    # other structure (see grammars/CParser.g4).
    CParser.RULE_typedefName,
    CParser.RULE_enumerationConstant,
}
