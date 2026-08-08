from ..utils import TOKEN_TYPE_OFFSET
from .CPP14Lexer import CPP14Lexer
from .CPP14Parser import CPP14Parser
from antlr4 import Token

EXCLUDED_TOKEN_TYPES = {
    # Structural / whitespace / comment / preprocessor-noise tokens
    Token.EOF,
    CPP14Lexer.Whitespace,
    CPP14Lexer.Newline,
    CPP14Lexer.BlockComment,
    CPP14Lexer.LineComment,
    CPP14Lexer.MultiLineMacro,
    CPP14Lexer.Directive,
    # Grouping / punctuation
    CPP14Lexer.LeftParen,
    CPP14Lexer.RightParen,
    CPP14Lexer.LeftBracket,
    CPP14Lexer.RightBracket,
    CPP14Lexer.LeftBrace,
    CPP14Lexer.RightBrace,
    CPP14Lexer.Comma,
    CPP14Lexer.Semi,
    CPP14Lexer.Dot,
    CPP14Lexer.Doublecolon,
    CPP14Lexer.Arrow,
    CPP14Lexer.ArrowStar,
    CPP14Lexer.DotStar,
    # Identifier
    CPP14Lexer.Identifier,
    # Ternary '?'/':'
    CPP14Lexer.Question,
    CPP14Lexer.Colon,
    # Single-operator
    CPP14Lexer.Caret,
    CPP14Lexer.AndAnd,
    CPP14Lexer.OrOr,
    # Statement keywords
    CPP14Lexer.If,
    CPP14Lexer.Switch,
    CPP14Lexer.Else,
    CPP14Lexer.While,
    CPP14Lexer.Do,
    CPP14Lexer.For,
    CPP14Lexer.Enum,
    CPP14Lexer.New,
    CPP14Lexer.Try,
    CPP14Lexer.Catch,
    # Case keywords
    CPP14Lexer.Case,
}
EXCLUDE_CHILDRENS_FROM_RULE = {
    CPP14Parser.RULE_andExpression: [
        CPP14Lexer.And + TOKEN_TYPE_OFFSET,
    ],
    CPP14Parser.RULE_inclusiveOrExpression: [
        CPP14Lexer.Or + TOKEN_TYPE_OFFSET,
    ],
}
COLLAPSED_RULE_INDICES = {
    # Namespace/using machinery
    CPP14Parser.RULE_usingDeclaration,
    CPP14Parser.RULE_usingDirective,
    CPP14Parser.RULE_namespaceAliasDefinition,
    # Aggregate-initialization literal syntax ('{1, 2, 3}', 'Point{1, 2}')
    CPP14Parser.RULE_bracedInitList,
}
HASHED_RULE_INDICES = {
    CPP14Parser.RULE_multiplicativeExpression,
    CPP14Parser.RULE_additiveExpression,
    CPP14Parser.RULE_shiftExpression,
    CPP14Parser.RULE_relationalExpression,
    CPP14Parser.RULE_equalityExpression,
    CPP14Parser.RULE_andExpression,
    CPP14Parser.RULE_exclusiveOrExpression,
    CPP14Parser.RULE_inclusiveOrExpression,
    CPP14Parser.RULE_logicalAndExpression,
    CPP14Parser.RULE_logicalOrExpression,
}
CONTROL_EQUIVALENCE_RULE_INDICES = set()
RULE_ASSIGNMENT = CPP14Parser.RULE_assignmentExpression
ASIGN_OP_NORMALIZED = dict()
EXCLUDED_RULE_TYPES = {
    CPP14Parser.RULE_nestedNameSpecifier,
    CPP14Parser.RULE_lambdaIntroducer,
    # Statements
    CPP14Parser.RULE_forInitStatement,
    # Declarations
    CPP14Parser.RULE_aliasDeclaration,
    # Type specifiers
    CPP14Parser.RULE_trailingTypeSpecifier,
    CPP14Parser.RULE_trailingTypeSpecifierSeq,
    CPP14Parser.RULE_simpleTypeSpecifier,
    CPP14Parser.RULE_theTypeName,
    # Namespace
    CPP14Parser.RULE_pointerOperator,
    CPP14Parser.RULE_cvqualifierseq,
    CPP14Parser.RULE_theTypeId,
    CPP14Parser.RULE_abstractDeclarator,
    # Functions and definitions
    CPP14Parser.RULE_className,
}
