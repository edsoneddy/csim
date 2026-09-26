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
# (multiplicativeExpression -> additiveExpression -> ... ->
# assignmentExpression). tree_processing.py's visitChildren already compresses
# any single-child hop through this chain.
#
# Tuning data: jv-umsa-dataset/all_c (real judge submissions). The tables were
# measured against the unpruned tree on two disjoint problem sets, see
# docs/pruning_fidelity.md (hashing policy: expression/declaration "islands"
# only, never the control-flow skeleton).
#
# IMPORTANT CAVEAT: this grammar's lexer/parser base classes
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
    # Statement keywords: the wrapping rule (selectionStatement/iterationStatement
    # -- `for`/`while`/`do` share one LOOP label) already carries the meaning,
    # and a leaked `for` vs `while` keyword leaf would break that equivalence.
    CLexer.If,
    CLexer.Else,
    CLexer.While,
    CLexer.Do,
    CLexer.For,
    CLexer.Switch,
    CLexer.Case,
    CLexer.Default,
    # Built-in type keywords: which numeric type was declared/returned is not
    # structure (`int main` vs `void solve` should line up).
    CLexer.Int,
    CLexer.Void,
    CLexer.Double,
    CLexer.Float,
    CLexer.Char,
    CLexer.Short,
    CLexer.Long,
    CLexer.Signed,
    CLexer.Unsigned,
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

# Hashing policy (see docs/pruning_fidelity.md): only "islands" --
# expressions, declarations, parameter lists and `return`/`break` statements
# that contain no control flow -- collapse to a digest. Compound statements,
# if/switch, loops and function definitions stay as real nodes so the
# program's skeleton survives. The previous policy hashed functionBody whole
# (one node per function). The island list comes from the rules that never
# contain a STRUCTURAL rule in real submissions (jv-umsa-dataset/all_c, two
# disjoint problem sets).
HASHED_RULE_INDICES = {
    CParser.RULE_multiplicativeExpression,
    CParser.RULE_additiveExpression,
    CParser.RULE_shiftExpression,
    CParser.RULE_relationalExpression,
    CParser.RULE_equalityExpression,
    CParser.RULE_andExpression,
    CParser.RULE_exclusiveOrExpression,
    CParser.RULE_inclusiveOrExpression,
    CParser.RULE_logicalAndExpression,
    CParser.RULE_logicalOrExpression,
    CParser.RULE_conditionalExpression,
    CParser.RULE_assignmentExpression,
    CParser.RULE_expression,
    CParser.RULE_unaryExpression,
    CParser.RULE_postfixExpression,
    CParser.RULE_castExpression,
    CParser.RULE_argumentExpressionList,
    CParser.RULE_initializerList,
    CParser.RULE_jumpStatement,
    CParser.RULE_declaration,
    CParser.RULE_declarationList,
    CParser.RULE_declarationSpecifiers,
    CParser.RULE_declarator,
    CParser.RULE_directDeclarator,
    CParser.RULE_initDeclarator,
    CParser.RULE_initDeclaratorList,
    CParser.RULE_parameterDeclaration,
    CParser.RULE_parameterList,
    CParser.RULE_forCondition,
    CParser.RULE_forDeclaration,
    CParser.RULE_forExpression,
    CParser.RULE_typeName,
}

# A hashed rule is NOT collapsed if its subtree contains one of these.
STRUCTURAL_RULE_INDICES = {
    CParser.RULE_compoundStatement,
    CParser.RULE_blockItemList,
    CParser.RULE_selectionStatement,
    CParser.RULE_iterationStatement,
    CParser.RULE_labeledStatement,
    CParser.RULE_functionDefinition,
    CParser.RULE_functionBody,
    CParser.RULE_structOrUnionSpecifier,
    CParser.RULE_externalDeclaration,
    CParser.RULE_translationUnit,
}

# for / while / do-while are all one grammar rule (iterationStatement) and
# interchangeable ways to write a loop (`for` <-> `while` rewrites are common
# clones), so they share one label.
CONTROL_EQUIVALENCE_RULE_INDICES = {
    CParser.RULE_iterationStatement: "LOOP",
}

# `x op= y` is rebuilt as `x = x op y` (CParserVisitorExtended): augmented
# token -> (rule of the binary operator, its operator token). Shifts left alone.
AUG_ASSIGN_OPS = {
    CLexer.PlusAssign: (CParser.RULE_additiveExpression, CLexer.Plus),
    CLexer.MinusAssign: (CParser.RULE_additiveExpression, CLexer.Minus),
    CLexer.StarAssign: (CParser.RULE_multiplicativeExpression, CLexer.Star),
    CLexer.DivAssign: (CParser.RULE_multiplicativeExpression, CLexer.Div),
    CLexer.ModAssign: (CParser.RULE_multiplicativeExpression, CLexer.Mod),
    CLexer.AndAssign: (CParser.RULE_andExpression, CLexer.And),
    CLexer.OrAssign: (CParser.RULE_inclusiveOrExpression, CLexer.Or),
    CLexer.XorAssign: (CParser.RULE_exclusiveOrExpression, CLexer.Caret),
}

RULE_ASSIGNMENT = None
ASIGN_OP_NORMALIZED = dict()

EXCLUDED_RULE_TYPES = {
    # Identifier-wrapping rules: which name was chosen doesn't reflect an
    # algorithmic difference. Both wrap a single Identifier token with no
    # other structure (see grammars/CParser.g4).
    CParser.RULE_typedefName,
    CParser.RULE_enumerationConstant,
}
