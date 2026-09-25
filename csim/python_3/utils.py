from .Python3Lexer import Python3Lexer
from .Python3Parser import Python3Parser
from antlr4 import Token
from antlr4.tree.Tree import TerminalNode
from ..utils import TOKEN_TYPE_OFFSET

# Synthetic rule ids for hub-rule alternatives that need a strategy or a
# rule identity DIFFERENT from the rest of their shared rule index -- see
# relabel_node() below. None collide with any real rule index (this grammar
# has 59 rules, 0-58) or with terminal labels (TOKEN_TYPE_OFFSET is 1000,
# per csim/utils.py). 200 mirrors java_24's SYNTHETIC_ASSIGNMENT_EXPR
# convention (see csim/java_24/utils.py) -- distinct languages, so no
# cross-language collision risk even though the numeric values repeat.
SYNTHETIC_IMPORT_STMT = 200
SYNTHETIC_TRY_STMT = 201
SYNTHETIC_IF_STMT = 202
SYNTHETIC_WHILE_STMT = 203
SYNTHETIC_FOR_STMT = 204
SYNTHETIC_WITH_STMT = 205
SYNTHETIC_CLASS_OR_FUNC_STMT = 206

# Readable names for `csim tree` output.
SYNTHETIC_NAMES = {
    SYNTHETIC_IMPORT_STMT: "import_stmt",
    SYNTHETIC_TRY_STMT: "try_stmt",
    SYNTHETIC_IF_STMT: "if_stmt",
    SYNTHETIC_WHILE_STMT: "while_stmt",
    SYNTHETIC_FOR_STMT: "for_stmt",
    SYNTHETIC_WITH_STMT: "with_stmt",
    SYNTHETIC_CLASS_OR_FUNC_STMT: "class_or_func_def_stmt",
}


def relabel_node(node):
    """Detect small_stmt/compound_stmt alternatives that need a different
    rule identity than the rest of their shared hub rule, and return a
    synthetic rule id for them, or None to leave the node's normal rule
    index alone.

    All cases below follow the same shape: a labeled ANTLR alternative
    shares its parent's rule index with unrelated alternatives (see
    grammars/Python3Parser.g4), so EXCLUDED_RULE_TYPES/COLLAPSED_RULE_INDICES/
    HASHED_RULE_INDICES can't target just one alternative, or distinguish it
    from its siblings during comparison, without this hook -- mirrors
    java_24's relabel_node() for the same underlying reason.

    Import-shaped `small_stmt` (#import_stmt: IMPORT dotted_as_names,
    #from_stmt: FROM ... IMPORT ...): routed to COLLAPSED_RULE_INDICES,
    matching python_3_13's content-free import machinery. Fixed 15 of 2211
    threshold-crossing pairs on jv_dataset/all_py/1050 (67 files) -- see
    COLLAPSED_RULE_INDICES's comment for the full writeup.

    compound_stmt's SIX labeled alternatives (#if_stmt, #while_stmt,
    #for_stmt, #with_stmt, #try_stmt, #class_or_func_def_stmt) all share
    RULE_compound_stmt, so each gets its own synthetic id here. Without it a
    `for` vs `while` swap would look like the same construct.
    None of the compound alternatives is hashed or excluded any more (see
    HASHED_RULE_INDICES): the synthetic ids only keep each construct's
    identity distinct, so a `for` vs a `while` still costs a full mismatch
    while their bodies stay as real, comparable subtrees. try/except is kept
    for the same reason (measured: keeping it lowers the error vs. the
    unpruned tree on both the tuning and validation problem sets).
    """
    rule_index = node.getRuleIndex()
    if rule_index == Python3Parser.RULE_small_stmt:
        if node.getChildCount() == 0:
            return None
        first = node.getChild(0)
        if isinstance(first, TerminalNode) and first.symbol.type in (
            Python3Lexer.IMPORT,
            Python3Lexer.FROM,
        ):
            return SYNTHETIC_IMPORT_STMT
        return None

    if rule_index == Python3Parser.RULE_compound_stmt:
        # if_stmt / while_stmt: always start with IF / WHILE.
        # for_stmt / with_stmt: ASYNC? FOR|WITH ... -- check both the first
        # and (if ASYNC) second child for the real keyword.
        # try_stmt: always starts with TRY.
        # class_or_func_def_stmt: decorator* (classdef | funcdef) -- no
        # leading keyword token; detected by looking for a classdef/funcdef
        # child instead (decorators, if any, precede it).
        for child in node.getChildren():
            if isinstance(child, TerminalNode):
                tt = child.symbol.type
                if tt == Python3Lexer.IF:
                    return SYNTHETIC_IF_STMT
                if tt == Python3Lexer.WHILE:
                    return SYNTHETIC_WHILE_STMT
                if tt == Python3Lexer.FOR:
                    return SYNTHETIC_FOR_STMT
                if tt == Python3Lexer.WITH:
                    return SYNTHETIC_WITH_STMT
                if tt == Python3Lexer.TRY:
                    return SYNTHETIC_TRY_STMT
                if tt == Python3Lexer.ASYNC:
                    continue
                break
            else:
                child_rule = child.getRuleIndex()
                if child_rule in (
                    Python3Parser.RULE_classdef,
                    Python3Parser.RULE_funcdef,
                ):
                    return SYNTHETIC_CLASS_OR_FUNC_STMT
                if child_rule == Python3Parser.RULE_decorator:
                    continue
                break
        return None

    return None

# Tuned 2026-08-12 for the grammars-v4/python/python "universal Python 2/3"
# grammar -- a separate, additional language from python_3_13 (which keeps
# its own grammar and utils.py untouched). This grammar's rule set is much
# flatter than python_3_13's (59 rules vs. python_3_13's much larger
# PEG-derived grammar) and shares no rule/token naming with it, so nothing
# here is ported 1:1 from python_3_13/utils.py -- only the general category
# of what's safe to treat as noise carries over, verified independently
# against real corpora (jv_dataset/all_py).
#
# Informed by lessons from tuning csim/java_24: the grammar's root rule
# (file_input) is NOT in HASHED_RULE_INDICES -- hashing a root/body-wrapping
# rule collapses an entire file/branch to one opaque digest per
# hashing_tree's short-circuit-on-first-match behavior (see
# tree_processing.py), which either produces a degenerate always-1-node tree
# (if done at the true root) or can make several DIFFERENT files converge to
# identical trees once combined with enough other exclusions -- both were
# measured as real failures during java_24's tuning (see
# csim_native_parsers project memory).
#
# Status: pruning fidelity is measured against the unpruned tree, not against
# python_3_13's output. On 2 disjoint sets of 12 jv-umsa-dataset/all_py
# problems (1440 pairs each), the similarity index of the pruned trees differs
# from the unpruned one by a mean of ~0.09 (vs. ~0.15 before compound
# statements stopped being hashed) at ~5x node compression -- see
# docs/pruning_fidelity.md for method and numbers.

EXCLUDED_TOKEN_TYPES = {
    # Structural / whitespace / comment tokens.
    Token.EOF,
    Python3Lexer.WS,
    Python3Lexer.COMMENT,
    Python3Lexer.NEWLINE,
    Python3Lexer.LINE_BREAK,
    Python3Lexer.LINE_JOIN,
    Python3Lexer.INDENT,
    Python3Lexer.DEDENT,
    # Grouping / punctuation
    Python3Lexer.OPEN_PAREN,
    Python3Lexer.CLOSE_PAREN,
    Python3Lexer.OPEN_BRACE,
    Python3Lexer.CLOSE_BRACE,
    Python3Lexer.OPEN_BRACKET,
    Python3Lexer.CLOSE_BRACKET,
    Python3Lexer.DOT,
    Python3Lexer.COMMA,
    Python3Lexer.COLON,
    Python3Lexer.SEMI_COLON,
    # Identifier text itself doesn't carry algorithmic meaning (same
    # reasoning as excluding RULE_name below covers rule-level identifier
    # nodes; NAME as a bare token also appears directly in some contexts).
    Python3Lexer.NAME,
    # Assignment sign
    Python3Lexer.ASSIGN,
    # Boolean connectives
    Python3Lexer.AND,
    Python3Lexer.OR,
    # AS (import/with/except aliasing)
    Python3Lexer.AS,
    # Return-type-annotation arrow
    Python3Lexer.ARROW,
    # Definition keywords: the funcdef/classdef rule already says which one it
    # is (python_3_13 drops them for the same reason).
    Python3Lexer.DEF,
    Python3Lexer.CLASS,
}

# Loop keywords/`in` add nothing once `for`/`while` share the LOOP label (see
# CONTROL_EQUIVALENCE_RULE_INDICES); without this a `for` and a `while` would
# still differ by their keyword leaf.
EXCLUDE_CHILDRENS_FROM_RULE = {
    SYNTHETIC_FOR_STMT: [
        Python3Lexer.FOR + TOKEN_TYPE_OFFSET,
        Python3Lexer.IN + TOKEN_TYPE_OFFSET,
    ],
    SYNTHETIC_WHILE_STMT: [
        Python3Lexer.WHILE + TOKEN_TYPE_OFFSET,
    ],
}

# Import machinery: which specific names were imported doesn't reflect an
# algorithmic difference (same "static container" reasoning as
# python_3_13/utils.py's equivalent entries).
COLLAPSED_RULE_INDICES = {
    Python3Parser.RULE_import_as_names,
    Python3Parser.RULE_import_as_name,
    Python3Parser.RULE_dotted_as_names,
    Python3Parser.RULE_dotted_as_name,
    Python3Parser.RULE_dotted_name,
    # Engine-assisted: see relabel_node() above. Not a real grammar rule --
    # a synthetic id assigned to import-shaped `small_stmt` nodes (both
    # `import X` and `from X import Y`), so this entry can treat any import
    # statement as a content-free marker, matching python_3_13's collapsed
    # import machinery, instead of falling under small_stmt's wholesale hash
    # below (which would make different import styles hash differently).
    SYNTHETIC_IMPORT_STMT,
}

# Critical for tractable tree-edit-distance runtime, not just grouping
# precision: this grammar merges its ENTIRE arithmetic/bitwise precedence
# chain into one left-recursive `expr` rule (unlike python_3_13, which
# splits it into ~10 separate rules it hashes individually -- see
# grammars/Python3Parser.g4's `expr` definition). Leaving it unhashed (the
# original first-pass state) produced trees 20-100x larger than
# python_3_13's for the same real files (measured on jv_dataset/all_py/1050:
# node counts of 31-123 vs. python_3_13's 1-4), which made `csim group`'s
# O(n^2)-ish tree-edit-distance step dominate so heavily that the 18.65x
# parsing speedup this grammar provides was completely negated -- a 50-file
# `csim group` run went from 0.91s (python_3_13) to 45s (python_3) before
# this was added. `comparison` and `logical_test` are the other two
# precedence-chain rules in this grammar (relational/equality, and
# and/or/not respectively).
#
# `small_stmt` is hashed instead of a narrower `assign_part`-only hash: it
# is itself a hub rule with labeled alternatives (#expr_stmt, #del_stmt,
# #pass_stmt, #break_stmt, #continue_stmt, #return_stmt, #raise_stmt,
# #import_stmt, #global_stmt, ... all sharing RULE_small_stmt -- see
# grammars/Python3Parser.g4). Hashing the ancestor makes hashing
# `assign_part` alone dead code (hashing_tree short-circuits on the first
# hashed rule reached top-down -- see tree_processing.py -- so nothing
# below `small_stmt` is ever individually visited once it matches), and
# additionally collapses PASS/BREAK/CONTINUE/etc into safe, distinguishable
# digests instead of leaving them as separate small nodes.
HASHED_RULE_INDICES = {
    Python3Parser.RULE_expr,
    Python3Parser.RULE_comparison,
    Python3Parser.RULE_logical_test,
    Python3Parser.RULE_small_stmt,
    # Parameter lists: names are noise, the arity/shape survives in the digest
    # (python_3_13 hashes `parameters`/`param` for the same reason).
    Python3Parser.RULE_def_parameters,
    # Compound statements (if/while/for/with/def/class) are deliberately NOT
    # hashed: their body is the program's control-flow skeleton, and hashing
    # them turned whole programs into 1-5 nodes (median 24x compression,
    # mean |error| of 0.14-0.16 in the similarity index vs. the unpruned
    # tree; see docs/pruning_fidelity.md). Only their leaves (expressions and
    # simple statements above) are hashed, which keeps ~5x compression at
    # roughly half that error. relabel_node() still gives each alternative
    # its own synthetic rule id so `for` vs `while` stay distinguishable
    # without hashing anything.
}

# `for` and `while` are interchangeable ways to write the same loop (the
# jv-umsa-dataset/controlled clones rewrite one as the other), so both get the
# same label; mirrors python_3_13 and the 2.0.0 behaviour.
CONTROL_EQUIVALENCE_RULE_INDICES = {
    SYNTHETIC_FOR_STMT: "LOOP",
    SYNTHETIC_WHILE_STMT: "LOOP",
}
# No visitAssignment-style rewrite wired up in Visitors.py for this language
# yet (matching java_24's current state).
RULE_ASSIGNMENT = None
ASIGN_OP_NORMALIZED = dict()

# Augmented-assignment token -> the binary operator token of its expanded
# form (`x += y` == `x = x + y`), used by Python3ParserVisitorExtended in
# Visitors.py. Values are the operator tokens of the `expr` rule.
AUG_ASSIGN_OPS = {
    Python3Lexer.ADD_ASSIGN: Python3Lexer.ADD,
    Python3Lexer.SUB_ASSIGN: Python3Lexer.MINUS,
    Python3Lexer.MULT_ASSIGN: Python3Lexer.STAR,
    Python3Lexer.AT_ASSIGN: Python3Lexer.AT,
    Python3Lexer.DIV_ASSIGN: Python3Lexer.DIV,
    Python3Lexer.MOD_ASSIGN: Python3Lexer.MOD,
    Python3Lexer.AND_ASSIGN: Python3Lexer.AND_OP,
    Python3Lexer.OR_ASSIGN: Python3Lexer.OR_OP,
    Python3Lexer.XOR_ASSIGN: Python3Lexer.XOR,
    Python3Lexer.LEFT_SHIFT_ASSIGN: Python3Lexer.LEFT_SHIFT,
    Python3Lexer.RIGHT_SHIFT_ASSIGN: Python3Lexer.RIGHT_SHIFT,
    Python3Lexer.POWER_ASSIGN: Python3Lexer.POWER,
    Python3Lexer.IDIV_ASSIGN: Python3Lexer.IDIV,
}

EXCLUDED_RULE_TYPES = {
    # Identifier nodes: which name was chosen doesn't reflect an
    # algorithmic difference.
    Python3Parser.RULE_name,
    # The `for` loop variable list (also `del` targets): identifiers only.
    Python3Parser.RULE_exprlist,
}
