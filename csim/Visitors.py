from .python_3_13.PythonParserVisitor import PythonParserVisitor
from .python_3_13.PythonParser import PythonParser
from .utils import TOKEN_TYPE_OFFSET
from .java_20.Java20ParserVisitor import Java20ParserVisitor
from .java_20.Java20Lexer import Java20Lexer
from .java_20.Java20Parser import Java20Parser
from .java_24.Java24ParserVisitor import Java24ParserVisitor
from .java_24.Java24Lexer import Java24Lexer
from .java_24.Java24Parser import Java24Parser
from .cpp_14.CPP14ParserVisitor import CPP14ParserVisitor
from .cpp_14.CPP14Lexer import CPP14Lexer
from .cpp_14.CPP14Parser import CPP14Parser
from .python_3.Python3ParserVisitor import Python3ParserVisitor
from .kotlin.KotlinParserVisitor import KotlinParserVisitor
from .kotlin.KotlinLexer import KotlinLexer
from .kotlin.KotlinParser import KotlinParser
from .c.CParserVisitor import CParserVisitor
from .c.CLexer import CLexer
from .c.CParser import CParser
from antlr4 import TerminalNode
from .java_20.utils import (
    AUG_ASSIGN_OPS as JAVA_20_AUG_ASSIGN_OPS,
    TARGET_AS_OPERAND as JAVA_20_TARGET_AS_OPERAND,
    COLLAPSED_RULE_INDICES as JAVA_20_COLLAPSED_RULES,
    ASIGN_OP_NORMALIZED as JAVA_20_ASSIGN_OP_NORMALIZED,
    RULE_ASSIGNMENT as JAVA_20_RULE_ASSIGNMENT,
)
try:
    from .java_24.utils import (
        COLLAPSED_RULE_INDICES as JAVA_24_COLLAPSED_RULES,
        AUG_ASSIGN_OPS as JAVA_24_AUG_ASSIGN_OPS,
        relabel_node as java_24_relabel_node,
        SYNTHETIC_ASSIGNMENT_EXPR as JAVA_24_SYNTHETIC_ASSIGNMENT_EXPR,
        ASIGN_OP_NORMALIZED as JAVA_24_ASSIGN_OP_NORMALIZED,
        RULE_ASSIGNMENT as JAVA_24_RULE_ASSIGNMENT,
    )
except (ImportError, AttributeError):
    # java_24 utils may not be fully available yet
    JAVA_24_COLLAPSED_RULES = set()
    JAVA_24_ASSIGN_OP_NORMALIZED = dict()
    JAVA_24_RULE_ASSIGNMENT = None
from .python_3_13.utils import (
    COLLAPSED_RULE_INDICES as PYTHON_3_13_COLLAPSED_RULES,
    ASIGN_OP_NORMALIZED as PYTHON_3_13_ASSIGN_OP_NORMALIZED,
    RULE_ASSIGNMENT as PYTHON_3_13_RULE_ASSIGNMENT,
)
from .python_3.utils import (
    COLLAPSED_RULE_INDICES as PYTHON_3_COLLAPSED_RULES,
    ASIGN_OP_NORMALIZED as PYTHON_3_ASSIGN_OP_NORMALIZED,
    RULE_ASSIGNMENT as PYTHON_3_RULE_ASSIGNMENT,
    relabel_node as python_3_relabel_node,
    AUG_ASSIGN_OPS as PYTHON_3_AUG_ASSIGN_OPS,
)
from .python_3.Python3Parser import Python3Parser
from .cpp_14.utils import (
    AUG_ASSIGN_OPS as CPP_14_AUG_ASSIGN_OPS,
    DECLARATOR_AS_OPERAND as CPP_14_DECLARATOR_AS_OPERAND,
    COLLAPSED_RULE_INDICES as CPP_14_COLLAPSED_RULES,
    ASIGN_OP_NORMALIZED as CPP_14_ASSIGN_OP_NORMALIZED,
    RULE_ASSIGNMENT as CPP_14_RULE_ASSIGNMENT,
)
from .kotlin.utils import (
    AUG_ASSIGN_OPS as KOTLIN_AUG_ASSIGN_OPS,
    COLLAPSED_RULE_INDICES as KOTLIN_COLLAPSED_RULES,
)
from .c.utils import (
    AUG_ASSIGN_OPS as C_AUG_ASSIGN_OPS,
    COLLAPSED_RULE_INDICES as C_COLLAPSED_RULES,
)


class Python_3_13_ParserVisitorExtended(PythonParserVisitor):
    def visit(self, tree):
        """Override visit to exclude certain rules from being processed.
        This helps in reducing noise in the parse tree by skipping over
        less relevant constructs.
        """
        if (
            not isinstance(tree, TerminalNode)
            and tree.getRuleIndex() in PYTHON_3_13_COLLAPSED_RULES
        ):
            return {"label": tree.getRuleIndex(), "children": []}
        return tree.accept(self)

    def _target_as_reference(self, target):
        """Normalized subtree for using an augmented-assignment target as an
        operand, i.e. the same tree the grammar builds for that expression
        when it is written out on the right-hand side of `x = x <op> y`.

        A bare name reduces to an `atom`; `a[i]`/`a.b` targets are parsed by
        the grammar as `t_primary` chains, whose right-hand-side twin is the
        `primary` rule, so they are re-emitted under RULE_primary.
        """
        R = PythonParser
        excluded_tokens = getattr(self, "excluded_token_types", set())
        excluded_rules = getattr(self, "excluded_rule_types", set())

        def convert(ctx):
            if ctx.getRuleIndex() == R.RULE_single_target:
                for child in ctx.getChildren():
                    if isinstance(child, TerminalNode):
                        continue  # parentheses
                    if child.getRuleIndex() == R.RULE_name:
                        return {"label": R.RULE_atom, "children": []}
                    return convert(child)
            nodes = []
            for child in ctx.getChildren():
                if isinstance(child, TerminalNode):
                    if child.symbol.type not in excluded_tokens:
                        nodes.append(
                            {"label": child.symbol.type + TOKEN_TYPE_OFFSET, "children": []}
                        )
                    continue
                rule = child.getRuleIndex()
                if rule in (R.RULE_t_primary, R.RULE_single_subscript_attribute_target):
                    nodes.append(convert(child))
                elif rule not in excluded_rules:
                    result = self.visit(child)
                    if result is not None:
                        nodes.append(result)
            if not nodes:
                return {"label": R.RULE_primary, "children": []}
            if len(nodes) == 1:
                return nodes[0]
            return {"label": R.RULE_primary, "children": nodes}

        return convert(target)

    def visitAssignment(self, node):
        """Rewrite augmented assignments into the tree of their expanded form.

        `x += y` is rebuilt as if it had been written `x = x + y`: the target
        becomes a childless `star_targets` node (what the grammar yields for
        the target of a plain assignment once names/punctuation are excluded),
        and the right-hand side becomes the operator rule with the target
        re-emitted as its left operand, exactly as `x + y` would parse. The
        result is structurally identical to the naturally-parsed expanded
        form, so both hash to the same digest under RULE_assignment (which is
        hashed).
        """
        if (
            node.getChildCount() == 3
            and not isinstance(node.getChild(1), TerminalNode)
            and node.getChild(1).getText() in PYTHON_3_13_ASSIGN_OP_NORMALIZED
        ):
            rule, operator_token = PYTHON_3_13_ASSIGN_OP_NORMALIZED[
                node.getChild(1).getText()
            ]
            norm_node = {
                "label": rule,
                "children": [
                    self._target_as_reference(node.getChild(0)),
                    {"label": operator_token, "children": []},
                    self.visit(node.getChild(2)),
                ],
            }
            return {
                "label": PYTHON_3_13_RULE_ASSIGNMENT,
                "children": [
                    {"label": PythonParser.RULE_star_targets, "children": []},
                    norm_node,
                ],
            }
        # Regular assignment: visit the children as usual
        return self.visitChildren(node)


class Java20ParserVisitorExtended(Java20ParserVisitor):
    def visit(self, tree):
        """Override visit to exclude certain rules from being processed.
        This helps in reducing noise in the parse tree by skipping over
        less relevant constructs.
        """
        if (
            not isinstance(tree, TerminalNode)
            and tree.getRuleIndex() in JAVA_20_COLLAPSED_RULES
        ):
            return {"label": tree.getRuleIndex(), "children": []}
        return tree.accept(self)

    def visitAssignment(self, node):
        """Rebuild `x op= y` as the tree of `x = x op y` (same rules, same
        children), so both hash identically. A plain `=` is visited as usual.

        Token types only (native terminals carry no text). The assignment
        operator is a rule wrapping one token; shift compound operators are
        not in AUG_ASSIGN_OPS and fall through unchanged.
        """
        if node.getChildCount() == 3 and not isinstance(node.getChild(1), TerminalNode):
            op = node.getChild(1).getChild(0)
            if isinstance(op, TerminalNode) and op.symbol.type in JAVA_20_AUG_ASSIGN_OPS:
                excluded = getattr(self, "excluded_token_types", set())
                rule, op_token = JAVA_20_AUG_ASSIGN_OPS[op.symbol.type]
                operand = self.visit(node.getChild(0))
                operand["label"] = JAVA_20_TARGET_AS_OPERAND.get(
                    operand["label"], operand["label"]
                )
                binary = [operand]
                if op_token not in excluded:
                    binary.append({"label": op_token + TOKEN_TYPE_OFFSET, "children": []})
                binary.append(self.visit(node.getChild(2)))
                if Java20Lexer.ASSIGN in excluded:
                    assign_op = {"label": Java20Parser.RULE_assignmentOperator, "children": []}
                else:
                    assign_op = {"label": Java20Lexer.ASSIGN + TOKEN_TYPE_OFFSET, "children": []}
                return {
                    "label": node.getRuleIndex(),
                    "children": [
                        self.visit(node.getChild(0)),
                        assign_op,
                        {"label": rule, "children": binary},
                    ],
                }
        return self.visitChildren(node)


class Java24ParserVisitorExtended(Java24ParserVisitor):
    def visit(self, tree):
        """Override visit to exclude certain rules from being processed.
        This helps in reducing noise in the parse tree by skipping over
        less relevant constructs. Also rewrites `x op= y` (see
        _expand_augmented_assignment).
        """
        if not isinstance(tree, TerminalNode):
            expanded = self._expand_augmented_assignment(tree)
            if expanded is not None:
                return expanded
            if tree.getRuleIndex() in JAVA_24_COLLAPSED_RULES:
                return {"label": tree.getRuleIndex(), "children": []}
        return tree.accept(self)

    def _expand_augmented_assignment(self, node):
        """Rebuild `x op= y` as the tree of `x = x op y`, or return None.

        In this grammar an assignment is `expression bop=<assign op> expression`
        (children: target, operator token, value) and the target is itself an
        `expression`, so visiting it twice yields exactly what the grammar
        builds for the same text on the right-hand side. Done in visit() so
        the native parser path (dispatching by rule name) sees it too.
        """
        # The native bridge already stamps assignment-shaped nodes with the
        # synthetic id, the Python parser leaves them as RULE_expression.
        if node.getChildCount() != 3 or node.getRuleIndex() not in (
            Java24Parser.RULE_expression,
            JAVA_24_SYNTHETIC_ASSIGNMENT_EXPR,
        ):
            return None
        op = node.getChild(1)
        if not isinstance(op, TerminalNode) or op.symbol.type not in JAVA_24_AUG_ASSIGN_OPS:
            return None
        excluded = getattr(self, "excluded_token_types", set())
        binary_token = JAVA_24_AUG_ASSIGN_OPS[op.symbol.type]
        binary = [self.visit(node.getChild(0))]
        if binary_token not in excluded:
            binary.append({"label": binary_token + TOKEN_TYPE_OFFSET, "children": []})
        binary.append(self.visit(node.getChild(2)))
        children = [self.visit(node.getChild(0))]
        if Java24Lexer.ASSIGN not in excluded:
            children.append({"label": Java24Lexer.ASSIGN + TOKEN_TYPE_OFFSET, "children": []})
        children.append({"label": Java24Parser.RULE_expression, "children": binary})
        return {"label": java_24_relabel_node(node) or node.getRuleIndex(), "children": children}


class CPP14ParserVisitorExtended(CPP14ParserVisitor):
    def visit(self, tree):
        """Override visit to exclude certain rules from being processed.
        This helps in reducing noise in the parse tree by skipping over
        less relevant constructs.
        """
        if (
            not isinstance(tree, TerminalNode)
            and tree.getRuleIndex() in CPP_14_COLLAPSED_RULES
        ):
            return {"label": tree.getRuleIndex(), "children": []}
        return tree.accept(self)

    def _assign_operator_node(self):
        """What the grammar leaves for a plain `=` operator after token
        exclusion: the bare `assignmentOperator` rule node, or the token."""
        if CPP14Lexer.Assign in getattr(self, "excluded_token_types", set()):
            return {"label": CPP14Parser.RULE_assignmentOperator, "children": []}
        return {"label": CPP14Lexer.Assign + TOKEN_TYPE_OFFSET, "children": []}

    def visitAssignmentExpression(self, node):
        """Rebuild `x op= y` as the tree of `x = x op y` (same rules, same
        children), so both hash identically. Only the assignment alternative
        (`logicalOrExpression assignmentOperator initializerClause`) has 3
        children; a bare conditionalExpression/throwExpression has one.
        Token types only (native terminals carry no text). Shifts are not in
        AUG_ASSIGN_OPS and fall through unchanged.
        """
        if node.getChildCount() == 3 and not isinstance(node.getChild(1), TerminalNode):
            op = node.getChild(1).getChild(0)
            if isinstance(op, TerminalNode) and op.symbol.type in CPP_14_AUG_ASSIGN_OPS:
                excluded = getattr(self, "excluded_token_types", set())
                rule, op_token = CPP_14_AUG_ASSIGN_OPS[op.symbol.type]
                binary = [self.visit(node.getChild(0))]
                if op_token not in excluded:
                    binary.append({"label": op_token + TOKEN_TYPE_OFFSET, "children": []})
                binary.append(self.visit(node.getChild(2)))
                return {
                    "label": node.getRuleIndex(),
                    "children": [
                        self.visit(node.getChild(0)),
                        self._assign_operator_node(),
                        {"label": rule, "children": binary},
                    ],
                }
        return self.visitChildren(node)

    def visitSimpleDeclaration(self, node):
        """`x = e;` (no type) parses as a *declaration* in this grammar
        (declSpecifierSeq is optional), while `x += e;` and `p->n = e;` are
        expression statements. Rebuild the declaration form as the
        assignmentExpression the expression forms produce, so `x = x + y;`
        and `x += y;` (and `a[i] = ...` / `p->n = ...`) all meet in one shape.
        Real declarations (`int x = 1;`) have a declSpecifierSeq and are left
        alone.
        """
        pseudo = self._pseudo_assignment_parts(node)
        if pseudo is None:
            return self.visitChildren(node)
        declarator, clause = pseudo
        lhs = self.visit(declarator)
        # Declarator rules twin the operand rules of the expression grammar.
        lhs["label"] = CPP_14_DECLARATOR_AS_OPERAND.get(lhs["label"], lhs["label"])
        return {
            "label": CPP14Parser.RULE_assignmentExpression,
            "children": [lhs, self._assign_operator_node(), self.visit(clause)],
        }

    @staticmethod
    def _pseudo_assignment_parts(node):
        """(declarator, initializerClause) when `node` is `<declarator> = <clause>;`
        with no decl-specifiers, else None."""
        rules = [c for c in node.getChildren() if not isinstance(c, TerminalNode)]
        if len(rules) != 1 or rules[0].getRuleIndex() != CPP14Parser.RULE_initDeclaratorList:
            return None
        lst = rules[0]
        if lst.getChildCount() != 1:
            return None
        decl = lst.getChild(0)
        if decl.getRuleIndex() != CPP14Parser.RULE_initDeclarator or decl.getChildCount() != 2:
            return None
        init = decl.getChild(1)
        if init.getRuleIndex() != CPP14Parser.RULE_initializer or init.getChildCount() != 1:
            return None
        eq = init.getChild(0)
        if eq.getRuleIndex() != CPP14Parser.RULE_braceOrEqualInitializer or eq.getChildCount() != 2:
            return None
        sign, clause = eq.getChild(0), eq.getChild(1)
        if not isinstance(sign, TerminalNode) or sign.symbol.type != CPP14Lexer.Assign:
            return None
        if isinstance(clause, TerminalNode) or clause.getRuleIndex() != CPP14Parser.RULE_initializerClause:
            return None
        return decl.getChild(0), clause


class KotlinParserVisitorExtended(KotlinParserVisitor):
    def visit(self, tree):
        """Override visit to exclude certain rules from being processed.
        This helps in reducing noise in the parse tree by skipping over
        less relevant constructs.

        No relabel_node() hook is needed: Kotlin's grammar has no ANTLR
        labeled alternatives at all (unlike java_24/python_3) -- see
        csim/kotlin/utils.py's module docstring.
        """
        if (
            not isinstance(tree, TerminalNode)
            and tree.getRuleIndex() in KOTLIN_COLLAPSED_RULES
        ):
            return {"label": tree.getRuleIndex(), "children": []}
        return tree.accept(self)

    def visitExpression(self, node):
        """Rebuild `x op= y` as the tree of `x = x op y` (same rules, same
        children), so both hash identically. Assignment is an ordinary
        `expression` here: `disjunction assignmentOperator disjunction`.
        Token types only (native terminals carry no text).
        """
        if node.getChildCount() == 3 and not isinstance(node.getChild(1), TerminalNode):
            op = node.getChild(1).getChild(0)
            if isinstance(op, TerminalNode) and op.symbol.type in KOTLIN_AUG_ASSIGN_OPS:
                excluded = getattr(self, "excluded_token_types", set())
                rule, op_token = KOTLIN_AUG_ASSIGN_OPS[op.symbol.type]
                binary = [self.visit(node.getChild(0))]
                if op_token not in excluded:
                    binary.append({"label": op_token + TOKEN_TYPE_OFFSET, "children": []})
                binary.append(self.visit(node.getChild(2)))
                if KotlinLexer.ASSIGNMENT in excluded:
                    assign_op = {"label": KotlinParser.RULE_assignmentOperator, "children": []}
                else:
                    assign_op = {"label": KotlinLexer.ASSIGNMENT + TOKEN_TYPE_OFFSET, "children": []}
                return {
                    "label": node.getRuleIndex(),
                    "children": [
                        self.visit(node.getChild(0)),
                        assign_op,
                        {"label": rule, "children": binary},
                    ],
                }
        return self.visitChildren(node)


class CParserVisitorExtended(CParserVisitor):
    def visit(self, tree):
        """Override visit to exclude certain rules from being processed.
        This helps in reducing noise in the parse tree by skipping over
        less relevant constructs.

        No relabel_node() hook is needed -- see csim/c/utils.py's module
        docstring (this grammar has no ANTLR labeled alternatives at all).
        """
        if (
            not isinstance(tree, TerminalNode)
            and tree.getRuleIndex() in C_COLLAPSED_RULES
        ):
            return {"label": tree.getRuleIndex(), "children": []}
        return tree.accept(self)

    def visitAssignmentExpression(self, node):
        """Rebuild `x op= y` as the tree of `x = x op y` (same rules, same
        children), so both hash identically. Only the assignment alternative
        (`unaryExpression <assign op token> assignmentExpression`) has 3
        children, the operator being a bare terminal (this grammar has no
        assignment-operator rule). Token types only (native terminals carry
        no text); shift compounds are not in AUG_ASSIGN_OPS and fall through
        unchanged.
        """
        if node.getChildCount() == 3:
            op = node.getChild(1)
            if isinstance(op, TerminalNode) and op.symbol.type in C_AUG_ASSIGN_OPS:
                excluded = getattr(self, "excluded_token_types", set())
                rule, op_token = C_AUG_ASSIGN_OPS[op.symbol.type]
                binary = [self.visit(node.getChild(0))]
                if op_token not in excluded:
                    binary.append({"label": op_token + TOKEN_TYPE_OFFSET, "children": []})
                binary.append(self.visit(node.getChild(2)))
                children = [self.visit(node.getChild(0))]
                if CLexer.Assign not in excluded:
                    children.append({"label": CLexer.Assign + TOKEN_TYPE_OFFSET, "children": []})
                children.append({"label": rule, "children": binary})
                return {"label": node.getRuleIndex(), "children": children}
        return self.visitChildren(node)


class Python3ParserVisitorExtended(Python3ParserVisitor):
    def visit(self, tree):
        """Override visit to exclude certain rules from being processed.
        This helps in reducing noise in the parse tree by skipping over
        less relevant constructs.

        Applies relabel_node() first (see csim/python_3/utils.py) so an
        import-shaped `small_stmt` node is checked against
        PYTHON_3_COLLAPSED_RULES under its synthetic id, not its raw
        RULE_small_stmt -- otherwise this check would never fire for it
        (small_stmt itself is in HASHED_RULE_INDICES, not collapsed) and
        the relabeling would only affect the EXCLUDED_RULE_TYPES check in
        tree_processing.py's shared visitChildren, not this one.
        """
        if not isinstance(tree, TerminalNode):
            expanded = self._expand_augmented_assignment(tree)
            if expanded is not None:
                return expanded
            rule_index = python_3_relabel_node(tree) or tree.getRuleIndex()
            if rule_index in PYTHON_3_COLLAPSED_RULES:
                return {"label": rule_index, "children": []}
        return tree.accept(self)

    def _expand_augmented_assignment(self, node):
        """Rebuild `x op= y` as the tree of `x = x op y`, or return None.

        Done here in visit() (not a labeled-alternative visitExpr_stmt)
        because the native parser dispatches on rule names, so it would never
        reach visitExpr_stmt; visit() sees every node on both paths. Only
        token types are used -- native terminals carry no text.

        `expr` is this grammar's merged operator rule, so the expanded form is
        small_stmt[target, expr[target, <op token>, rhs]]; the target is
        visited twice (a fresh subtree each time), which reproduces exactly
        what the grammar builds for the same target as a plain expression.
        """
        if (
            node.getRuleIndex() != Python3Parser.RULE_small_stmt
            or node.getChildCount() != 2
        ):
            return None
        target, assign_part = node.getChild(0), node.getChild(1)
        if (
            isinstance(target, TerminalNode)
            or isinstance(assign_part, TerminalNode)
            or assign_part.getRuleIndex() != Python3Parser.RULE_assign_part
            or assign_part.getChildCount() != 2
        ):
            return None
        op = assign_part.getChild(0)
        if not isinstance(op, TerminalNode) or op.symbol.type not in PYTHON_3_AUG_ASSIGN_OPS:
            return None
        return {
            "label": Python3Parser.RULE_small_stmt,
            "children": [
                self.visit(target),
                {
                    "label": Python3Parser.RULE_expr,
                    "children": [
                        self.visit(target),
                        {
                            "label": PYTHON_3_AUG_ASSIGN_OPS[op.symbol.type] + TOKEN_TYPE_OFFSET,
                            "children": [],
                        },
                        self.visit(assign_part.getChild(1)),
                    ],
                },
            ],
        }
