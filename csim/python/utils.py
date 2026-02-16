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
}


EXCLUDE_CHILDRENS_FROM_RULE = {
    PythonParser.RULE_for_stmt: [
        PythonLexer.IN + TOKEN_TYPE_OFFSET,
        PythonLexer.NAME + TOKEN_TYPE_OFFSET,
    ],
    PythonParser.RULE_function_def_raw: [
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
