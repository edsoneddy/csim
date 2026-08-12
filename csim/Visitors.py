from .python_3_13.PythonParserVisitor import PythonParserVisitor
from .java_20.Java20ParserVisitor import Java20ParserVisitor
from .java_24.Java24ParserVisitor import Java24ParserVisitor
from .cpp_14.CPP14ParserVisitor import CPP14ParserVisitor
from .python_3.Python3ParserVisitor import Python3ParserVisitor
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
)
from .cpp_14.utils import (
    COLLAPSED_RULE_INDICES as CPP_14_COLLAPSED_RULES,
    ASIGN_OP_NORMALIZED as CPP_14_ASSIGN_OP_NORMALIZED,
    RULE_ASSIGNMENT as CPP_14_RULE_ASSIGNMENT,
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

    def visitAssignment(self, node):
        """Rewrite assignment nodes to a normalized form based on the operator used.
        This allows different forms of the same underlying operation to be treated as equivalent in similarity comparisons.
        e.g., "x += 1" and "x = x + 1" would both be normalized to a common representation, improving the accuracy of similarity detection.
        """
        operand = node.getChild(1).getText()
        if operand in PYTHON_3_13_ASSIGN_OP_NORMALIZED:
            # Rewrite the assignment to a normalized form based on the operator
            rule, operator_token = PYTHON_3_13_ASSIGN_OP_NORMALIZED[operand]
            assignment_node = {"label": PYTHON_3_13_RULE_ASSIGNMENT, "children": []}
            norm_node = {"label": rule, "children": []}
            norm_node["children"].append(self.visit(node.getChild(0)))
            norm_node["children"].append({"label": operator_token, "children": []})
            norm_node["children"].append(self.visit(node.getChild(2)))
            assignment_node["children"].append(norm_node)
            return assignment_node
        else:
            # For regular assignment, just visit the children as usual
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
            rule_index = python_3_relabel_node(tree) or tree.getRuleIndex()
            if rule_index in PYTHON_3_COLLAPSED_RULES:
                return {"label": rule_index, "children": []}
        return tree.accept(self)
