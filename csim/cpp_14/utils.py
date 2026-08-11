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
    # csim-batch-tuner sweep, scripts/report.md, verified collision-free
    # in combination.
    CPP14Parser.RULE_expressionList,
    CPP14Parser.RULE_baseSpecifier,
    CPP14Parser.RULE_memInitializer,
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
    # Body-wrapping rules: content-based hash preserves genuine differences
    # while collapsing internal structure to a single node.
    # csim-batch-tuner sweep, scripts/report.md, verified collision-free
    # in combination.
    CPP14Parser.RULE_lambdaExpression,
    CPP14Parser.RULE_unaryExpression,
    CPP14Parser.RULE_newExpression_,
    CPP14Parser.RULE_labeledStatement,
    CPP14Parser.RULE_selectionStatement,
    CPP14Parser.RULE_simpleDeclaration,
    CPP14Parser.RULE_enumSpecifier,
    CPP14Parser.RULE_enumHead,
    CPP14Parser.RULE_opaqueEnumDeclaration,
    CPP14Parser.RULE_namespaceDefinition,
    CPP14Parser.RULE_linkageSpecification,
    CPP14Parser.RULE_initDeclarator,
    CPP14Parser.RULE_functionDefinition,
    CPP14Parser.RULE_classSpecifier,
    CPP14Parser.RULE_memberdeclaration,
    CPP14Parser.RULE_virtualSpecifierSeq,
    CPP14Parser.RULE_baseSpecifierList,
    CPP14Parser.RULE_memInitializerList,
    CPP14Parser.RULE_templateDeclaration,
    CPP14Parser.RULE_explicitSpecialization,
    CPP14Parser.RULE_exceptionDeclaration,
    CPP14Parser.RULE_noeExceptSpecification,
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
    # csim-batch-tuner sweep (scripts/report.md), verified collision-free
    # in combination with every other entry in this file. NOTE: several
    # recommendations were dropped for causing collisions when combined
    # with the rest of this set -- most severely declarator/
    # pointerDeclarator/noPointerDeclarator/parametersAndQualifiers/
    # declSpecifier/declSpecifierSeq/blockDeclaration, which together
    # would have erased almost all distinguishing content from ordinary
    # declarations. Also dropped: pointerMemberExpression,
    # assignmentExpression, expression, constantExpression, jumpStatement,
    # attributeSpecifierSeq, classHead, memberDeclaratorList,
    # memberDeclarator. See the audit method note at the end of this file.
    CPP14Parser.RULE_alignmentspecifier,
    CPP14Parser.RULE_asmDefinition,
    CPP14Parser.RULE_assignmentOperator,
    CPP14Parser.RULE_baseTypeSpecifier,
    CPP14Parser.RULE_classHeadName,
    CPP14Parser.RULE_classKey,
    CPP14Parser.RULE_condition,
    CPP14Parser.RULE_constructorInitializer,
    CPP14Parser.RULE_conversionFunctionId,
    CPP14Parser.RULE_conversionTypeId,
    CPP14Parser.RULE_declarationStatement,
    CPP14Parser.RULE_deleteExpression,
    CPP14Parser.RULE_dynamicExceptionSpecification,
    CPP14Parser.RULE_enumbase,
    CPP14Parser.RULE_enumerator,
    CPP14Parser.RULE_enumeratorDefinition,
    CPP14Parser.RULE_enumeratorList,
    CPP14Parser.RULE_explicitInstantiation,
    CPP14Parser.RULE_forRangeDeclaration,
    CPP14Parser.RULE_forRangeInitializer,
    CPP14Parser.RULE_literalOperatorId,
    CPP14Parser.RULE_meminitializerid,
    CPP14Parser.RULE_newDeclarator_,
    CPP14Parser.RULE_newInitializer_,
    CPP14Parser.RULE_newTypeId,
    CPP14Parser.RULE_noExceptExpression,
    CPP14Parser.RULE_operatorFunctionId,
    CPP14Parser.RULE_pureSpecifier,
    CPP14Parser.RULE_staticAssertDeclaration,
    CPP14Parser.RULE_templateParameter,
    CPP14Parser.RULE_templateparameterList,
    CPP14Parser.RULE_theOperator,
    CPP14Parser.RULE_throwExpression,
    CPP14Parser.RULE_trailingReturnType,
    CPP14Parser.RULE_typeIdList,
}
