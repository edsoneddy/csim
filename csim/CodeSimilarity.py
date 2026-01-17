from .PythonParser import PythonParser
from .PythonLexer import PythonLexer
from .PythonParserVisitor import PythonParserVisitor
from .utils import EXCLUDED_TOKEN_TYPES, GROUP_INDEX, TOKEN_TYPE_OFFSET
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
                    # Offset token types to avoid collision with parser rule indices
                    token_type_index = token.type + TOKEN_TYPE_OFFSET
                    children_nodes.append(Node(token_type_index))
            else:
                result = self.visit(child)
                if result is not None:
                    children_nodes.append(result)

        # Node compression: simplify tree structure
        if len(children_nodes) == 1:
            # Single child: return it directly to avoid unnecessary nesting
            return children_nodes[0]
        elif len(children_nodes) > 1:
            # Multiple children: group them under a single parent node
            self.node_count += 1
            group = Node(GROUP_INDEX)
            for c in children_nodes:
                group.addkid(c)
            return group

        # Leaf node: create a node representing the current rule
        self.node_count += 1
        zss_node = Node(rule_index)
        return zss_node

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


def annotate_hashes(node):
    """Recursively annotate each node with a structural hash.
    
    The hash is computed based on the node's label and the hashes of its children,
    enabling fast comparison of identical subtrees during tree edit distance computation.
    
    Args:
        node: ZSS Node to annotate (modified in place).
    """
    # Recursively process all children first (post-order traversal)
    for c in node.children:
        annotate_hashes(c)

    # Leaf node: hash is based solely on its label
    if not node.children:
        node.struct_hash = hash(node.label)
    else:
        # Internal node: hash combines label with all children's hashes
        node.struct_hash = hash(
            (node.label, tuple(c.struct_hash for c in node.children))
        )


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

    # Annotate each node with structural hashes for efficient subtree comparison
    annotate_hashes(normalized_tree)

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
    return s


def node_dist(a, b):
    """Calculate the distance between two tree nodes for ZSS algorithm.
    
    Uses a hierarchical comparison strategy:
    1. First checks structural hashes for fast identical subtree detection
    2. Falls back to label comparison if hashes differ
    
    Args:
        a: First node (or string for insertion/deletion operations).
        b: Second node (or string for insertion/deletion operations).
        
    Returns:
        int: 0 if nodes match (or subtrees are identical), 1 otherwise.
    """
    # Handle insertion and deletion operations (represented as strings by ZSS)
    if isinstance(a, str) or isinstance(b, str):
        return 1

    # Fast path: check if entire subtrees are structurally identical
    if a.struct_hash == b.struct_hash:
        return 0

    # Fallback: compare node labels only
    return 0 if a.label == b.label else 1


def get_node(node):
    """Label extraction function for ZSS algorithm.
    
    Returns the node itself rather than just its label, allowing node_dist
    to access the structural hash for optimization.
    
    Args:
        node: ZSS Node to extract label from.
        
    Returns:
        The node itself (not just its label).
    """
    return node


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
    d = simple_distance(N1, N2, get_label=get_node, label_dist=node_dist)
    
    # Calculate and return normalized similarity index
    s = SimilarityIndex(d, len_N1, len_N2)
    return s
