from .Python3Lexer import Python3Lexer
from .Python3Parser import Python3Parser
from antlr4 import Token
from antlr4.tree.Tree import TerminalNode

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
    RULE_compound_stmt. Hashing compound_stmt wholesale (needed for tree
    size) makes distance_metrics.py's label_distance() give a `for` vs
    `while` swap only 0.5 cost ("same rule, different hash" -- SAME
    ruleIndex, since both are compound_stmt) instead of the 1.0 cost
    python_3_13 assigns (for_stmt and while_stmt are genuinely separate,
    unshared rules there, so they always fully mismatch). This under-
    penalizes a real control-flow difference. Giving each alternative its
    OWN synthetic id before hashing restores that distinction: two `for`
    loops still compare as "same rule, hash of content" (0.0 or 0.5
    depending on content), but a `for` vs a `while` now correctly costs 1.0,
    matching python_3_13. Measured: files 132244.py/789477.py in
    jv_dataset/all_py/1006 (296 files) differ mainly in loop kind (`for` vs
    `while`) and scored 0.67 (python_3_13, correctly separate) vs. 0.83
    (python_3 pre-fix, incorrectly merged) -- found via the 296-file corpus
    after the 67-file corpus showed zero remaining threshold-crossing pairs,
    a reminder that one corpus sample doesn't cover every construct.
    if/while/for/with/class_or_func_def route to HASHED_RULE_INDICES (their
    content still matters, same reasoning as `expr`/`comparison`/
    `logical_test`); try_stmt keeps routing to EXCLUDED_RULE_TYPES per the
    original try/except fix (python_3_13 drops that content entirely, it
    doesn't leave a marker behind either).
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
# Status (jv_dataset/all_py, grouping compared against python_3_13 pairwise
# for every file, threshold 0.8):
#   - all_py/1050 (67 files, 2211 pairs):  0 threshold-crossing pairs.
#     `csim group` output is byte-for-byte identical to python_3_13's.
#   - all_py/1006 (296 files):             0 threshold-crossing pairs.
#     `csim group` output is byte-for-byte identical to python_3_13's.
#   - all_py/1039 (91 files):              26 threshold-crossing pairs
#     remain, all python_3 scoring HIGHER than python_3_13. Root cause: for
#     files with few top-level statements, python_3's tree ends up SMALLER/
#     coarser overall than python_3_13's for the same source (e.g. 5 nodes
#     vs. python_3_13's 8-9 for the same two-function file) even though
#     each individual hash/exclude/collapse decision made here is
#     individually correct -- SimilarityIndex's TED-based formula is
#     sensitive to overall tree size, so a smaller tree makes any single
#     matching subtree (e.g. a boilerplate `if __name__ == "__main__":`
#     block) count for proportionally more of the total similarity. Fixing
#     this needs understanding why python_3_13 stays more granular at the
#     top-level-statement level specifically -- a new investigation, not an
#     extension of the assignment/try-except/loop-kind fixes above (see
#     relabel_node() and the other tables' comments for those). Left as a
#     known limitation rather than guessed at further.

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
}

EXCLUDE_CHILDRENS_FROM_RULE = dict()

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
    # Body-wrapping alternatives of `compound_stmt`. Unlike java_24's
    # rejected COLLAPSED experiment on a hub rule (which discarded content
    # entirely, making different constructs indistinguishable), HASHING
    # preserves a content-derived digest -- an `if` and a `while` still get
    # different digests since their content differs, so this doesn't
    # reintroduce that failure mode.
    #
    # Each alternative gets its OWN synthetic id via relabel_node() above
    # instead of hashing RULE_compound_stmt directly: `compound_stmt` itself
    # would give every alternative the SAME rule label, and
    # distance_metrics.py's label_distance() gives "same rule, different
    # hash" only 0.5 cost -- meaning a `for`-vs-`while` swap would cost half
    # what python_3_13 charges (for_stmt/while_stmt are genuinely separate,
    # unshared rules there, so they mismatch fully at 1.0). Measured: fixed
    # files 132244.py/789477.py in jv_dataset/all_py/1006 (296 files),
    # which differ mainly in loop kind and incorrectly scored 0.83 (merged)
    # instead of python_3_13's 0.67 (separate) before this. `funcdef`/
    # `classdef` are separate, non-shared rules already covered by
    # SYNTHETIC_CLASS_OR_FUNC_STMT above; listed too in case a future change
    # stops routing through the synthetic id.
    SYNTHETIC_IF_STMT,
    SYNTHETIC_WHILE_STMT,
    SYNTHETIC_FOR_STMT,
    SYNTHETIC_WITH_STMT,
    SYNTHETIC_CLASS_OR_FUNC_STMT,
    Python3Parser.RULE_funcdef,
    Python3Parser.RULE_classdef,
}

CONTROL_EQUIVALENCE_RULE_INDICES = set()
# No visitAssignment-style rewrite wired up in Visitors.py for this language
# yet (matching java_24's current state).
RULE_ASSIGNMENT = None
ASIGN_OP_NORMALIZED = dict()

EXCLUDED_RULE_TYPES = {
    # Identifier nodes: which name was chosen doesn't reflect an
    # algorithmic difference.
    Python3Parser.RULE_name,
    # Engine-assisted: see relabel_node() above. Not a real grammar rule --
    # a synthetic id assigned to try-shaped `compound_stmt` nodes, so this
    # entry can drop the whole try/except/finally structure the same way
    # python_3_13 drops it via its separate try_stmt/except_block/
    # finally_block/else_block entries, instead of it falling under
    # compound_stmt's wholesale hash below.
    SYNTHETIC_TRY_STMT,
}
