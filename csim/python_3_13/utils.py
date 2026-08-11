from ..utils import TOKEN_TYPE_OFFSET
from .PythonParser import PythonParser
from .PythonLexer import PythonLexer
from antlr4 import Token

EXCLUDED_TOKEN_TYPES = {
    # Structural / whitespace / comment tokens
    Token.EOF,
    PythonLexer.ENCODING,
    PythonLexer.INDENT,
    PythonLexer.DEDENT,
    PythonLexer.TYPE_COMMENT,
    PythonLexer.NEWLINE,
    PythonLexer.COMMENT,
    PythonLexer.WS,
    PythonLexer.EXPLICIT_LINE_JOINING,
    PythonLexer.ERRORTOKEN,
    # Grouping / punctuation
    PythonLexer.LPAR,
    PythonLexer.LSQB,
    PythonLexer.LBRACE,
    PythonLexer.RPAR,
    PythonLexer.RSQB,
    PythonLexer.RBRACE,
    PythonLexer.DOT,
    PythonLexer.COLON,
    PythonLexer.COMMA,
    PythonLexer.SEMI,
    # F-string delimiters
    PythonLexer.FSTRING_START,
    PythonLexer.FSTRING_MIDDLE,
    PythonLexer.FSTRING_END,
    # Identifier
    PythonLexer.NAME,
    # Assignment sign
    PythonLexer.EQUAL,
    # Compound-statement keywords
    PythonLexer.IF,
    PythonLexer.ELIF,
    PythonLexer.WHILE,
    PythonLexer.FOR,
    PythonLexer.WITH,
    PythonLexer.TRY,
    # Simple-statement keywords
    PythonLexer.GLOBAL,
    PythonLexer.NONLOCAL,
    # Boolean connectives
    PythonLexer.AND,
    PythonLexer.OR,
    # AS
    PythonLexer.AS,
    # Return-type-annotation arrow
    PythonLexer.RARROW,
    # Soft keywords
    PythonLexer.NAME_OR_TYPE,
    PythonLexer.NAME_OR_MATCH,
    PythonLexer.NAME_OR_CASE,
    # DEF
    PythonLexer.DEF,
    # DEL
    PythonLexer.DEL,
    # Statement-introducing keywords whose parent rule already differs by
    # rule label (else_block, except_block, class_def_raw, finally_block,
    # function_def_raw w/ ASYNC), so the keyword token itself is redundant.
    # csim-batch-tuner sweep, scripts/report.md -- verified collision-free
    # in combination with every other entry added below (not just against
    # the pristine baseline each was individually measured against).
    PythonLexer.ELSE,
    PythonLexer.EXCEPT,
    PythonLexer.CLASS,
    PythonLexer.FINALLY,
    PythonLexer.ASYNC,
}
EXCLUDE_CHILDRENS_FROM_RULE = {
    PythonParser.RULE_for_stmt: [
        PythonLexer.IN + TOKEN_TYPE_OFFSET,
    ],
}
COLLAPSED_RULE_INDICES = {
    # Import machinery
    PythonParser.RULE_import_stmt,
    PythonParser.RULE_import_name,
    PythonParser.RULE_import_from,
    PythonParser.RULE_import_from_targets,
    PythonParser.RULE_import_from_as_names,
    PythonParser.RULE_import_from_as_name,
    PythonParser.RULE_dotted_as_names,
    PythonParser.RULE_dotted_as_name,
    PythonParser.RULE_dotted_name,
    # Static literal containers: literal *display* syntax (e.g. [1, 2, 3])
    PythonParser.RULE_list,
    PythonParser.RULE_tuple,
    PythonParser.RULE_set,
    PythonParser.RULE_dict,
}
HASHED_RULE_INDICES = {
    PythonParser.RULE_assignment,
    PythonParser.RULE_primary,
    PythonParser.RULE_comparison,
    PythonParser.RULE_return_stmt,
    PythonParser.RULE_parameters,
    PythonParser.RULE_param,
    PythonParser.RULE_decorators,
    PythonParser.RULE_kwds,
    PythonParser.RULE_args,
    PythonParser.RULE_star_targets,
    # Operator-precedence expression chains
    PythonParser.RULE_expression,
    PythonParser.RULE_yield_expr,
    PythonParser.RULE_star_expressions,
    PythonParser.RULE_star_expression,
    PythonParser.RULE_star_named_expressions,
    PythonParser.RULE_star_named_expression,
    PythonParser.RULE_assignment_expression,
    PythonParser.RULE_disjunction,
    PythonParser.RULE_conjunction,
    PythonParser.RULE_inversion,
    PythonParser.RULE_bitwise_or,
    PythonParser.RULE_bitwise_xor,
    PythonParser.RULE_bitwise_and,
    PythonParser.RULE_shift_expr,
    PythonParser.RULE_sum,
    PythonParser.RULE_term,
    PythonParser.RULE_factor,
    PythonParser.RULE_power,
    PythonParser.RULE_await_primary,
    # del_targets / del_target
    PythonParser.RULE_del_targets,
    PythonParser.RULE_del_target,
    # Body-wrapping rules: content-based hash preserves genuine differences
    # between two classes/functions/branches while collapsing the noisy
    # internal structure to a single node. csim-batch-tuner sweep,
    # scripts/report.md, verified collision-free in combination.
    PythonParser.RULE_class_def_raw,
    PythonParser.RULE_function_def,
    PythonParser.RULE_function_def_raw,
    PythonParser.RULE_if_stmt,
    PythonParser.RULE_while_stmt,
    PythonParser.RULE_for_stmt,
    PythonParser.RULE_with_stmt,
}
CONTROL_EQUIVALENCE_RULE_INDICES = {}
RULE_ASSIGNMENT = PythonParser.RULE_assignment
ASIGN_OP_NORMALIZED = {
    "+=": [
        PythonParser.RULE_sum,
        PythonLexer.PLUS + TOKEN_TYPE_OFFSET,
    ],
    "-=": [
        PythonParser.RULE_sum,
        PythonLexer.MINUS + TOKEN_TYPE_OFFSET,
    ],
    "*=": [
        PythonParser.RULE_term,
        PythonLexer.STAR + TOKEN_TYPE_OFFSET,
    ],
    "/=": [
        PythonParser.RULE_term,
        PythonLexer.SLASH + TOKEN_TYPE_OFFSET,
    ],
    "//=": [
        PythonParser.RULE_term,
        PythonLexer.DOUBLESLASH + TOKEN_TYPE_OFFSET,
    ],
    "%=": [
        PythonParser.RULE_term,
        PythonLexer.PERCENT + TOKEN_TYPE_OFFSET,
    ],
    "@=": [
        PythonParser.RULE_term,
        PythonLexer.AT + TOKEN_TYPE_OFFSET,
    ],
    "**=": [
        PythonParser.RULE_power,
        PythonLexer.DOUBLESTAR + TOKEN_TYPE_OFFSET,
    ],
    "<<=": [
        PythonParser.RULE_shift_expr,
        PythonLexer.LEFTSHIFT + TOKEN_TYPE_OFFSET,
    ],
    ">>=": [
        PythonParser.RULE_shift_expr,
        PythonLexer.RIGHTSHIFT + TOKEN_TYPE_OFFSET,
    ],
    "&=": [
        PythonParser.RULE_bitwise_and,
        PythonLexer.AMPER + TOKEN_TYPE_OFFSET,
    ],
    "^=": [
        PythonParser.RULE_bitwise_xor,
        PythonLexer.CIRCUMFLEX + TOKEN_TYPE_OFFSET,
    ],
    "|=": [
        PythonParser.RULE_bitwise_or,
        PythonLexer.VBAR + TOKEN_TYPE_OFFSET,
    ],
}
EXCLUDED_RULE_TYPES = {
    PythonParser.RULE_name,
    PythonParser.RULE_name_except_underscore,
    PythonParser.RULE_raise_stmt,
    PythonParser.RULE_assert_stmt,
    # raise_stmt/assert_stmt wrap
    PythonParser.RULE_subject_expr,
    PythonParser.RULE_guard,
    PythonParser.RULE_patterns,
    PythonParser.RULE_pattern,
    PythonParser.RULE_or_pattern,
    PythonParser.RULE_closed_pattern,
    PythonParser.RULE_literal_expr,
    PythonParser.RULE_pattern_capture_target,
    PythonParser.RULE_name_or_attr,
    PythonParser.RULE_sequence_pattern,
    PythonParser.RULE_maybe_sequence_pattern,
    PythonParser.RULE_maybe_star_pattern,
    PythonParser.RULE_mapping_pattern,
    PythonParser.RULE_items_pattern,
    PythonParser.RULE_key_value_pattern,
    PythonParser.RULE_double_star_pattern,
    PythonParser.RULE_class_pattern,
    PythonParser.RULE_keyword_patterns,
    PythonParser.RULE_keyword_pattern,
    PythonParser.RULE_type_alias,
    PythonParser.RULE_type_params,
    # Assignment/targets.
    PythonParser.RULE_star_target,
    PythonParser.RULE_t_primary,
    # csim-batch-tuner sweep (scripts/report.md), verified collision-free
    # in combination. NOTE: `block` and `params` were ALSO recommended by
    # the sweep but deliberately left OUT here -- applying `block`
    # together with the hashed body-wrapping rules above erases a
    # function/class/branch's entire content before it reaches the hash
    # (every function collapsed to the same sha256("") digest, a genuine
    # collision, not just a theoretical risk). `params` similarly
    # collided when combined with the rest. See the audit method note at
    # the end of this file.
    PythonParser.RULE_default_assignment,
    PythonParser.RULE_elif_stmt,
    PythonParser.RULE_else_block,
    PythonParser.RULE_with_item,
    PythonParser.RULE_try_stmt,
    PythonParser.RULE_except_block,
    PythonParser.RULE_except_star_block,
    PythonParser.RULE_finally_block,
}
