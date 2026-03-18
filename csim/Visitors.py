from .python.PythonParserVisitor import PythonParserVisitor
from .java.Java20ParserVisitor import Java20ParserVisitor
from .cpp.CPP14ParserVisitor import CPP14ParserVisitor
from zss import Node
from antlr4 import TerminalNode
from .java.utils import (
    COLLAPSED_RULE_INDICES as JAVA_COLLAPSED_RULES,
)
from .python.utils import (
    COLLAPSED_RULE_INDICES as PYTHON_COLLAPSED_RULES,
    ASIGN_OP_NORMALIZED as PYTHON_ASSIGN_OP_NORMALIZED,
    RULE_ASSIGNMENT as PYTHON_RULE_ASSIGNMENT,
)
from .cpp.utils import (
    COLLAPSED_RULE_INDICES as CPP_COLLAPSED_RULES,
)


class PythonParserVisitorExtended(PythonParserVisitor):

    def visit(self, tree):
        """Override visit to exclude certain rules from being processed.
        This helps in reducing noise in the parse tree by skipping over
        less relevant constructs.
        """
        if (
            not isinstance(tree, TerminalNode)
            and tree.getRuleIndex() in PYTHON_COLLAPSED_RULES
        ):
            list_idx = tree.getRuleIndex()
            return Node(list_idx)
        return tree.accept(self)

    def visitAssignment(self, node):
        """Rewrite assignment nodes to a normalized form based on the operator used.
        This allows different forms of the same underlying operation to be treated as equivalent in similarity comparisons.
        e.g., "x += 1" and "x = x + 1" would both be normalized to a common representation, improving the accuracy of similarity detection.
        """
        operand = node.getChild(1).getText()
        if operand in PYTHON_ASSIGN_OP_NORMALIZED:
            # Rewrite the assignment to a normalized form based on the operator
            rule, operator_token = PYTHON_ASSIGN_OP_NORMALIZED[operand]
            assignment_node = Node(PYTHON_RULE_ASSIGNMENT)
            norm_node = Node(rule)
            norm_node.addkid(self.visit(node.getChild(0)))
            norm_node.addkid(Node(operator_token))
            norm_node.addkid(self.visit(node.getChild(2)))
            assignment_node.addkid(norm_node)
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
            and tree.getRuleIndex() in JAVA_COLLAPSED_RULES
        ):
            list_idx = tree.getRuleIndex()
            return Node(list_idx)
        return tree.accept(self)


class CPP14ParserVisitorExtended(CPP14ParserVisitor):

    def visit(self, tree):
        """Override visit to exclude certain rules from being processed.
        This helps in reducing noise in the parse tree by skipping over
        less relevant constructs.
        """
        if (
            not isinstance(tree, TerminalNode)
            and tree.getRuleIndex() in CPP_COLLAPSED_RULES
        ):
            list_idx = tree.getRuleIndex()
            return Node(list_idx)
        return tree.accept(self)
