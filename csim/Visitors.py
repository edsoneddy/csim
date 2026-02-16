from .python.PythonParserVisitor import PythonParserVisitor
from zss import Node
from antlr4 import TerminalNode
from .python.utils import (
    COLLAPSED_RULE_INDICES as PYTHON_COLLAPSED_RULES,
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
