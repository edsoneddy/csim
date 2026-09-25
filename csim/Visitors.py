from .python_3_13.PythonParserVisitor import PythonParserVisitor
from .python_3_13.PythonParser import PythonParser
from .utils import TOKEN_TYPE_OFFSET
from .java_20.Java20ParserVisitor import Java20ParserVisitor
from .java_24.Java24ParserVisitor import Java24ParserVisitor
from .cpp_14.CPP14ParserVisitor import CPP14ParserVisitor
from .python_3.Python3ParserVisitor import Python3ParserVisitor
from .kotlin.KotlinParserVisitor import KotlinParserVisitor
from .c.CParserVisitor import CParserVisitor
from antlr4 import TerminalNode
from .java_20.utils import (
    COLLAPSED_RULE_INDICES as JAVA_20_COLLAPSED_RULES,
    ASIGN_OP_NORMALIZED as JAVA_20_ASSIGN_OP_NORMALIZED,
    RULE_ASSIGNMENT as JAVA_20_RULE_ASSIGNMENT,
)
try:
    from .java_24.utils import (
        COLLAPSED_RULE_INDICES as JAVA_24_COLLAPSED_RULES,
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
    COLLAPSED_RULE_INDICES as CPP_14_COLLAPSED_RULES,
    ASIGN_OP_NORMALIZED as CPP_14_ASSIGN_OP_NORMALIZED,
    RULE_ASSIGNMENT as CPP_14_RULE_ASSIGNMENT,
)
from .kotlin.utils import (
    COLLAPSED_RULE_INDICES as KOTLIN_COLLAPSED_RULES,
)
from .c.utils import (
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
        """Rewrite assignment nodes to a normalized form based on the operator used.
        This allows different forms of the same underlying operation to be treated as equivalent in similarity comparisons.
        e.g., "x += 1" and "x = x + 1" would both be normalized to a common representation, improving the accuracy of similarity detection.
        """
        operand = node.getChild(1).getText()
        if operand in JAVA_20_ASSIGN_OP_NORMALIZED:
            # Rewrite the assignment to a normalized form based on the operator
            rule, operator_token = JAVA_20_ASSIGN_OP_NORMALIZED[operand]
            assignment_node = {"label": JAVA_20_RULE_ASSIGNMENT, "children": []}
            norm_node = {"label": rule, "children": []}
            norm_node["children"].append(self.visit(node.getChild(0)))
            norm_node["children"].append({"label": operator_token, "children": []})
            norm_node["children"].append(self.visit(node.getChild(2)))
            assignment_node["children"].append(norm_node)
            return assignment_node
        else:
            # For regular assignment, just visit the children as usual
            return self.visitChildren(node)


class Java24ParserVisitorExtended(Java24ParserVisitor):
    def visit(self, tree):
        """Override visit to exclude certain rules from being processed.
        This helps in reducing noise in the parse tree by skipping over
        less relevant constructs.
        """
        if (
            not isinstance(tree, TerminalNode)
            and tree.getRuleIndex() in JAVA_24_COLLAPSED_RULES
        ):
            return {"label": tree.getRuleIndex(), "children": []}
        return tree.accept(self)

    def visitAssignment(self, node):
        """Rewrite assignment nodes to a normalized form based on the operator used.
        This allows different forms of the same underlying operation to be treated as equivalent in similarity comparisons.
        e.g., "x += 1" and "x = x + 1" would both be normalized to a common representation, improving the accuracy of similarity detection.
        """
        operand = node.getChild(1).getText()
        if operand in JAVA_24_ASSIGN_OP_NORMALIZED:
            # Rewrite the assignment to a normalized form based on the operator
            rule, operator_token = JAVA_24_ASSIGN_OP_NORMALIZED[operand]
            assignment_node = {"label": JAVA_24_RULE_ASSIGNMENT, "children": []}
            norm_node = {"label": rule, "children": []}
            norm_node["children"].append(self.visit(node.getChild(0)))
            norm_node["children"].append({"label": operator_token, "children": []})
            norm_node["children"].append(self.visit(node.getChild(2)))
            assignment_node["children"].append(norm_node)
            return assignment_node
        else:
            # For regular assignment, just visit the children as usual
            return self.visitChildren(node)


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

    def visitAssignmentExpression(self, node):
        """Rewrite assignment nodes to a normalized form based on the operator used.
        This allows different forms of the same underlying operation to be treated as equivalent in similarity comparisons.
        e.g., "x += 1" and "x = x + 1" would both be normalized to a common representation, improving the accuracy of similarity detection.

        Unlike Python/Java, C++'s assignmentExpression rule also matches non-assignment
        alternatives (a bare conditionalExpression, or a throwExpression), which only ever
        have a single child. Only the actual assignment alternative has 3 children
        (logicalOrExpression assignmentOperator initializerClause), so that count is checked
        before treating child(1) as an operator.
        """
        if node.getChildCount() != 3:
            return self.visitChildren(node)
        operand = node.getChild(1).getText()
        if operand in CPP_14_ASSIGN_OP_NORMALIZED:
            # Rewrite the assignment to a normalized form based on the operator
            rule, operator_token = CPP_14_ASSIGN_OP_NORMALIZED[operand]
            assignment_node = {"label": CPP_14_RULE_ASSIGNMENT, "children": []}
            norm_node = {"label": rule, "children": []}
            norm_node["children"].append(self.visit(node.getChild(0)))
            norm_node["children"].append({"label": operator_token, "children": []})
            norm_node["children"].append(self.visit(node.getChild(2)))
            assignment_node["children"].append(norm_node)
            return assignment_node
        else:
            # For regular assignment, just visit the children as usual
            return self.visitChildren(node)


class KotlinParserVisitorExtended(KotlinParserVisitor):
    def visit(self, tree):
        """Override visit to exclude certain rules from being processed.
        This helps in reducing noise in the parse tree by skipping over
        less relevant constructs.

        No visitAssignment-style override here: Kotlin's grammar has no
        ANTLR labeled alternatives at all (unlike java_24/python_3), so
        there's no relabel_node() hook needed either -- see
        csim/kotlin/utils.py's module docstring.
        """
        if (
            not isinstance(tree, TerminalNode)
            and tree.getRuleIndex() in KOTLIN_COLLAPSED_RULES
        ):
            return {"label": tree.getRuleIndex(), "children": []}
        return tree.accept(self)


class CParserVisitorExtended(CParserVisitor):
    def visit(self, tree):
        """Override visit to exclude certain rules from being processed.
        This helps in reducing noise in the parse tree by skipping over
        less relevant constructs.

        No visitAssignment-style override here: no relabel_node() hook is
        needed either -- see csim/c/utils.py's module docstring (this
        grammar has no ANTLR labeled alternatives at all).
        """
        if (
            not isinstance(tree, TerminalNode)
            and tree.getRuleIndex() in C_COLLAPSED_RULES
        ):
            return {"label": tree.getRuleIndex(), "children": []}
        return tree.accept(self)


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
