from csim.utils import TOKEN_TYPE_OFFSET
from .PythonParser import PythonParser
from .PythonLexer import PythonLexer
from antlr4 import Token

# Excluded token types that do not contribute to code semantics
EXCLUDED_TOKEN_TYPES = {
    # Structural tokens
    Token.EOF,
    PythonLexer.INDENT,
    PythonLexer.DEDENT,
    PythonLexer.NEWLINE,
    PythonLexer.COMMENT,
    # Grouping tokens
    PythonLexer.LPAR,
    PythonLexer.RPAR,
    PythonLexer.LBRACE,
    PythonLexer.RBRACE,
    PythonLexer.LSQB,
    PythonLexer.RSQB,
    # Punctuation tokens
    PythonLexer.COMMA,
    PythonLexer.COLON,
    PythonLexer.SEMI,
    PythonLexer.DOT,
    # Reserved keywords
    PythonLexer.DEF,
    PythonLexer.CLASS,
    PythonLexer.IF,
    PythonLexer.ELSE,
    PythonLexer.ELIF,
    PythonLexer.FOR,
    PythonLexer.WHILE,
    PythonLexer.TRY,
    PythonLexer.RAISE,
    PythonLexer.GLOBAL,
    PythonLexer.WITH,
    # Irrelevant tokens
    PythonLexer.EQUAL,
}

# Rules whose children should be excluded from similarity comparison
EXCLUDE_CHILDRENS_FROM_RULE = {
    PythonParser.RULE_for_stmt: [
        PythonLexer.IN + TOKEN_TYPE_OFFSET,
        PythonLexer.NAME + TOKEN_TYPE_OFFSET,
    ],
    PythonParser.RULE_function_def_raw: [
        PythonLexer.NAME + TOKEN_TYPE_OFFSET,
    ],
    PythonParser.RULE_assignment: [
        PythonLexer.NAME + TOKEN_TYPE_OFFSET,
    ],
}

# Collapsed Parser Rules
COLLAPSED_RULE_INDICES = {
    # Import statements
    PythonParser.RULE_import_stmt,
    PythonParser.RULE_import_name,
    PythonParser.RULE_import_from,
    PythonParser.RULE_import_from_targets,
    PythonParser.RULE_import_from_as_names,
    PythonParser.RULE_import_from_as_name,
    # Data structures
    PythonParser.RULE_list,
    PythonParser.RULE_tuple,
    PythonParser.RULE_dict,
    PythonParser.RULE_set,
}

# Rules to hash instead of comparing structurally
HASHED_RULE_INDICES = {
    PythonParser.RULE_assignment,
    PythonParser.RULE_primary,
    PythonParser.RULE_star_targets,
    PythonParser.RULE_comparison,
    PythonParser.RULE_return_stmt,
    PythonParser.RULE_parameters,
    PythonParser.RULE_param,
    PythonParser.RULE_except_block,
    PythonParser.RULE_decorators,
    PythonParser.RULE_kwds,
    PythonParser.RULE_args,
}

# Rules that are considered equivalent for control flow analysis
CONTROL_EQUIVALENCE_RULE_INDICES = {
    PythonParser.RULE_for_stmt: "LOOP",
    PythonParser.RULE_while_stmt: "LOOP",
}

# Specific rule indices for special handling
RULE_ASSIGNMENT = PythonParser.RULE_assignment

# Augmented assignments mapped to normalized forms
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
