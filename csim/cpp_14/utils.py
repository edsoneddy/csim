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
    # Built-in type keywords: which numeric type was declared/returned is not
    # structure (`int main` vs `void solve` should line up).
    CPP14Lexer.Int,
    CPP14Lexer.Void,
    CPP14Lexer.Double,
    CPP14Lexer.Float,
    CPP14Lexer.Long,
    CPP14Lexer.Short,
    CPP14Lexer.Char,
    CPP14Lexer.Bool,
    CPP14Lexer.Signed,
    CPP14Lexer.Unsigned,
    CPP14Lexer.Auto,
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
    # csim-batch-tuner sweep (scripts/report.md): each keyword/operator is
    # redundant once its parent rule already carries a distinct label.
    # Verified collision-free in combination with every other entry added
    # below. NOTE: MinusMinus was ALSO recommended by the sweep but left
    # OUT here -- combined with PlusPlus it erases the one difference
    # between postfix ++ and -- (both reduce to just the operand). See the
    # audit method note at the end of this file.
    CPP14Lexer.Alignas,
    CPP14Lexer.Asm,
    CPP14Lexer.Const_cast,
    CPP14Lexer.Default,
    CPP14Lexer.Delete,
    CPP14Lexer.Dynamic_cast,
    CPP14Lexer.Extern,
    CPP14Lexer.Namespace,
    CPP14Lexer.Noexcept,
    CPP14Lexer.Operator,
    CPP14Lexer.Reinterpret_cast,
    CPP14Lexer.Return,
    CPP14Lexer.Sizeof,
    CPP14Lexer.Static_assert,
    CPP14Lexer.Static_cast,
    CPP14Lexer.Template,
    CPP14Lexer.Throw,
    CPP14Lexer.Union,
    CPP14Lexer.Assign,
    CPP14Lexer.PlusPlus,
}
EXCLUDE_CHILDRENS_FROM_RULE = dict()

COLLAPSED_RULE_INDICES = {
    # Namespace/using machinery
    CPP14Parser.RULE_usingDeclaration,
    CPP14Parser.RULE_usingDirective,
    CPP14Parser.RULE_namespaceAliasDefinition,
    # Aggregate-initialization literal syntax ('{1, 2, 3}', 'Point{1, 2}')
    CPP14Parser.RULE_bracedInitList,
    CPP14Parser.RULE_expressionList,
    CPP14Parser.RULE_baseSpecifier,
    CPP14Parser.RULE_memInitializer,
}

# Hashing policy (see docs/pruning_fidelity.md): only "islands" -- expressions,
# declarations, parameter lists and type specifiers that contain no control
# flow -- collapse to a digest. Compound statements, if/switch, loops, function
# definitions, classes and namespaces stay as real nodes so the program's
# skeleton survives. The previous policy also hashed selectionStatement/
# functionDefinition/classSpecifier/... and excluded declarationStatement,
# condition and assignmentOperator: median 3 nodes per file and the index
# moved by ~0.3 (bias +0.26) vs. the unpruned tree. This one: ~7x
# compression at ~0.1 error. The island list comes from the rules that never
# contain a STRUCTURAL rule in real submissions (jv-umsa-dataset/all_cpp, two
# disjoint problem sets).
HASHED_RULE_INDICES = {
    CPP14Parser.RULE_multiplicativeExpression,
    CPP14Parser.RULE_additiveExpression,
    CPP14Parser.RULE_shiftExpression,
    CPP14Parser.RULE_shiftOperator,
    CPP14Parser.RULE_relationalExpression,
    CPP14Parser.RULE_equalityExpression,
    CPP14Parser.RULE_andExpression,
    CPP14Parser.RULE_exclusiveOrExpression,
    CPP14Parser.RULE_inclusiveOrExpression,
    CPP14Parser.RULE_logicalAndExpression,
    CPP14Parser.RULE_logicalOrExpression,
    CPP14Parser.RULE_conditionalExpression,
    CPP14Parser.RULE_assignmentExpression,
    CPP14Parser.RULE_expression,
    CPP14Parser.RULE_unaryExpression,
    CPP14Parser.RULE_postfixExpression,
    CPP14Parser.RULE_castExpression,
    CPP14Parser.RULE_newExpression_,
    CPP14Parser.RULE_lambdaExpression,
    CPP14Parser.RULE_declaration,
    CPP14Parser.RULE_simpleDeclaration,
    CPP14Parser.RULE_initDeclarator,
    CPP14Parser.RULE_initDeclaratorList,
    CPP14Parser.RULE_forRangeDeclaration,
    CPP14Parser.RULE_declSpecifierSeq,
    CPP14Parser.RULE_typeSpecifierSeq,
    CPP14Parser.RULE_simpleTypeSpecifier,
    CPP14Parser.RULE_theTypeId,
    CPP14Parser.RULE_pointerDeclarator,
    CPP14Parser.RULE_noPointerDeclarator,
    CPP14Parser.RULE_parameterDeclaration,
    CPP14Parser.RULE_parameterDeclarationList,
    CPP14Parser.RULE_qualifiedId,
    CPP14Parser.RULE_simpleTemplateId,
    CPP14Parser.RULE_templateArgumentList,
    CPP14Parser.RULE_templateparameterList,
    CPP14Parser.RULE_theOperator,
}

# A hashed rule is NOT collapsed if its subtree contains one of these (e.g. a
# lambda with a compound-statement body).
STRUCTURAL_RULE_INDICES = {
    CPP14Parser.RULE_compoundStatement,
    CPP14Parser.RULE_statementSeq,
    CPP14Parser.RULE_selectionStatement,
    CPP14Parser.RULE_iterationStatement,
    CPP14Parser.RULE_labeledStatement,
    CPP14Parser.RULE_functionBody,
    CPP14Parser.RULE_functionDefinition,
    CPP14Parser.RULE_classSpecifier,
    CPP14Parser.RULE_namespaceDefinition,
    CPP14Parser.RULE_templateDeclaration,
    CPP14Parser.RULE_tryBlock,
    CPP14Parser.RULE_handler,
    CPP14Parser.RULE_functionTryBlock,
    CPP14Parser.RULE_linkageSpecification,
}

# for / while / do-while / range-for are all one grammar rule
# (iterationStatement) and interchangeable ways to write a loop -- `for` <->
# `while` rewrites are common clones -- so they share one label.
CONTROL_EQUIVALENCE_RULE_INDICES = {
    CPP14Parser.RULE_iterationStatement: "LOOP",
}
RULE_ASSIGNMENT = CPP14Parser.RULE_assignmentExpression
ASIGN_OP_NORMALIZED = dict()

# `x op= y` is rebuilt as `x = x op y` (CPP14ParserVisitorExtended): augmented
# token -> (rule of the binary operator, its operator token). Shifts left alone.
AUG_ASSIGN_OPS = {
    CPP14Lexer.PlusAssign: (CPP14Parser.RULE_additiveExpression, CPP14Lexer.Plus),
    CPP14Lexer.MinusAssign: (CPP14Parser.RULE_additiveExpression, CPP14Lexer.Minus),
    CPP14Lexer.StarAssign: (CPP14Parser.RULE_multiplicativeExpression, CPP14Lexer.Star),
    CPP14Lexer.DivAssign: (CPP14Parser.RULE_multiplicativeExpression, CPP14Lexer.Div),
    CPP14Lexer.ModAssign: (CPP14Parser.RULE_multiplicativeExpression, CPP14Lexer.Mod),
    CPP14Lexer.AndAssign: (CPP14Parser.RULE_andExpression, CPP14Lexer.And),
    CPP14Lexer.OrAssign: (CPP14Parser.RULE_inclusiveOrExpression, CPP14Lexer.Or),
    CPP14Lexer.XorAssign: (CPP14Parser.RULE_exclusiveOrExpression, CPP14Lexer.Caret),
}

# A type-less `x = e;` parses as a declaration: its declarator rules are the
# twins of the operand rules the same text gets in an expression.
DECLARATOR_AS_OPERAND = {
    CPP14Parser.RULE_noPointerDeclarator: CPP14Parser.RULE_postfixExpression,
    CPP14Parser.RULE_pointerDeclarator: CPP14Parser.RULE_unaryExpression,
}

# Identifier text is already dropped at token level; no rule is pure noise.
# (The old list excluded declarationStatement, condition, assignmentOperator,
# type specifiers, pointer operators, ... -- measured as signal loss.)
EXCLUDED_RULE_TYPES = set()
