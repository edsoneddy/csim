from .python.PythonParser import PythonParser
from .python.PythonLexer import PythonLexer
from .python.PythonParserVisitor import PythonParserVisitor
from .python.py_utils import EXCLUDED_TOKEN_TYPES, TOKEN_TYPE_OFFSET
from antlr4 import InputStream, CommonTokenStream, TerminalNode
from antlr4 import CommonTokenStream
from zss import simple_distance, Node


class Visitor(PythonParserVisitor):
    """Visitor pattern implementation for traversing and normalizing ANTLR parse trees.

    Converts the ANTLR parse tree into a normalized ZSS tree structure while
    compressing redundant nodes and counting total nodes for similarity metrics.
    """

    def __init__(self):
        super().__init__()
        self.node_count = 0

    def visitChildren(self, node):
        """Visit and process all children of a parse tree node.

        Args:
            node: ANTLR parse tree node to process.

        Returns:
            A ZSS Node representing the normalized subtree.
        """
        rule_index = node.getRuleIndex()
        children_nodes = []

        for child in node.getChildren():
            if isinstance(child, TerminalNode):
                token = child.symbol
                if token.type not in EXCLUDED_TOKEN_TYPES:
                    self.node_count += 1
                    children_nodes.append(Node(token.type + TOKEN_TYPE_OFFSET))
            else:
                result = self.visit(child)
                if result is not None:
                    children_nodes.append(result)

        # Node compression: simplify tree structure
        if len(children_nodes) == 1:
            # Single child: return it directly to avoid unnecessary nesting
            return children_nodes[0]

        # Create parent node for multiple children
        self.node_count += 1
        parent_node = Node(rule_index)
        for c in children_nodes:
            parent_node.addkid(c)
        return parent_node

    def visitStar_named_expressions(self, node):
        """Handle star_named_expressions to avoid creating excessive nodes.

        This special case prevents deeply nested structures in list/tuple literals,
        replacing them with a single node.

        Example: [1, 2, 3, ..., k] is collapsed into one node.

        Args:
            node: The star_named_expressions parse tree node.

        Returns:
            A single ZSS Node representing the entire expression list.
        """
        list_idx = node.getRuleIndex()
        self.node_count += 1
        return Node(list_idx)


def Normalize(tree):
    """Normalize an ANTLR parse tree into a ZSS tree structure.

    Args:
        tree: ANTLR parse tree to normalize.

    Returns:
        tuple: (normalized_tree, node_count) where normalized_tree is a ZSS Node
               and node_count is the total number of nodes in the tree.
    """
    visitor = Visitor()
    normalized_tree = visitor.visit(tree)

    return normalized_tree, visitor.node_count


def ANTLR_parse(code):
    """Parse Python source code into an ANTLR parse tree.

    Args:
        code: Python source code as a string.

    Returns:
        ANTLR parse tree representing the code's syntactic structure.
    """
    input_stream = InputStream(code)
    lexer = PythonLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = PythonParser(token_stream)
    tree = parser.file_input()
    return tree


def SimilarityIndex(d, T1, T2):
    """Calculate the similarity index between two trees.

    Normalizes the tree edit distance to a value between 0 and 1, where
    1 indicates identical trees and 0 indicates maximum dissimilarity.

    Args:
        d: Tree edit distance between the two trees.
        T1: Number of nodes in the first tree.
        T2: Number of nodes in the second tree.

    Returns:
        float: Similarity index in the range [0, 1].
    """
    m = max(T1, T2)
    s = 1 - (d / m)

    # return similarity index with precision of 2 decimal places
    s = round(s, 2)
    return s


def label_dist(a, b):
    """Calculate the distance between two tree nodes for ZSS algorithm.

    Args:
        a: label of node a.
        b: label of node b.

    Returns:
        int: 0 if nodes match (or subtrees are identical), 1 otherwise.
    """
    return 0 if a == b else 1


def Compare(code_a, code_b):
    """Compare two Python code snippets and compute their similarity.

    The comparison process:
    1. Parse both code snippets into ANTLR parse trees
    2. Normalize the parse trees into ZSS tree structures
    3. Compute tree edit distance using Zhang-Shasha algorithm
    4. Calculate normalized similarity index

    Args:
        code_a: First Python code snippet as a string.
        code_b: Second Python code snippet as a string.

    Returns:
        float: Similarity score in the range [0, 1], where 1 indicates
               identical code structure and 0 indicates maximum difference.
    """
    # Parse both code snippets into ANTLR parse trees
    T1 = ANTLR_parse(code_a)
    T2 = ANTLR_parse(code_b)

    # Normalize parse trees and get node counts
    N1, len_N1 = Normalize(T1)
    N2, len_N2 = Normalize(T2)

    # Compute tree edit distance using Zhang-Shasha algorithm
    d = simple_distance(N1, N2, label_dist=label_dist)

    # Calculate and return normalized similarity index
    s = SimilarityIndex(d, len_N1, len_N2)
    return s
