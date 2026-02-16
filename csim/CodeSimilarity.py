import sys
from .python.PythonParser import PythonParser
from .python.PythonLexer import PythonLexer
from .Visitors import PythonParserVisitorExtended
from .utils import (
    TOKEN_TYPE_OFFSET,
    get_control_equivalence_rule_indices,
    get_exclude_childrens_from_rule,
    get_excluded_token_types,
    get_hash_rule_indices,
)
import hashlib
from antlr4 import InputStream, CommonTokenStream, TerminalNode
from antlr4.error.ErrorListener import ErrorListener
from zss import simple_distance, Node


class ExtendedErrorListener(ErrorListener):
    def __init__(self, file_name=""):
        super(ExtendedErrorListener, self).__init__()
        self.file_name = file_name

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print(
            f"Syntax error in file {self.file_name} line {line}:{column} {msg}",
            file=sys.stderr,
        )


def get_parser_visitor_class(lang):
    """
    Factory function to create a ParserVisitor class with the correct base visitor.
    """
    base_visitor = None
    if lang == "python":
        base_visitor = PythonParserVisitorExtended

    if base_visitor is None:
        raise ValueError(f"Unsupported language: {lang}")

    class ParserVisitor(base_visitor):
        """ParserVisitor pattern implementation for traversing and normalizing ANTLR parse trees.

        Converts the ANTLR parse tree into a normalized ZSS tree structure while
        compressing redundant nodes and counting total nodes for similarity metrics.
        """

        def __init__(self, excluded_token_types):
            super().__init__()
            self.excluded_token_types = excluded_token_types

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
                    if token.type not in self.excluded_token_types:
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
            parent_node = Node(rule_index)
            for c in children_nodes:
                parent_node.addkid(c)
            return parent_node

    return ParserVisitor


def PruneAndHash(tree, lang):
    """Prune and hash an ANTLR parse tree.

    Args:
        tree: ANTLR parse tree to prune and hash.
        lang: The programming language of the source code.
    Returns:
        tuple: (pruned_tree, node_count) where pruned_tree is a ZSS Node
               and node_count is the total number of nodes in the pruned tree.
    """
    hashed_rule_indices = get_hash_rule_indices(lang)
    control_equivalence_rule_indices = get_control_equivalence_rule_indices(lang)
    exclude_childrens_from_rule = get_exclude_childrens_from_rule(lang)

    def traverse_subtree(node):
        # Collect all labels in the subtree rooted at `node` into a single list
        elements = [node.label]
        for c in node.children:
            elements.extend(traverse_subtree(c))
        return elements

    def hash_children(label, childrens):
        # Flatten all children subtree labels into a single sequence and hash
        flat = []
        for c in childrens:
            flat.extend(traverse_subtree(c))
        s = "|".join(map(str, flat))
        return str(label) + "|" + hashlib.sha256(s.encode("utf-8")).hexdigest()

    def traverse(node):
        if node is None:
            return None, 0

        count = 1
        label = node.label

        if label in control_equivalence_rule_indices:
            label = control_equivalence_rule_indices[label]

        if node.label in hashed_rule_indices:
            digest = hash_children(label, node.children)
            new_node = Node(digest)
            return new_node, count

        new_node = Node(label)

        # Get the list of child labels to exclude for this rule, if any
        childrens_to_exclude = exclude_childrens_from_rule.get(node.label, [])

        # Otherwise, recurse normally.
        for children in node.children:

            # Skip children that are in the exclusion list for this rule
            if children.label in childrens_to_exclude:
                continue

            new_child, child_count = traverse(children)
            if new_child is not None:
                new_node.addkid(new_child)
                count += child_count
        return new_node, count

    pruned_tree, pruned_count = traverse(tree)

    return pruned_tree, pruned_count


def Normalize(tree, lang):
    """Normalize an ANTLR parse tree into a ZSS tree structure.

    Args:
        tree: ANTLR parse tree to normalize.
        lang: The programming language of the source code.

    Returns:
        tuple: (normalized_tree, node_count) where normalized_tree is a ZSS Node
               and node_count is the total number of nodes in the tree.
    """
    excluded_token_types = get_excluded_token_types(lang)

    # Get the correct ParserVisitor class for the given language
    ParserVisitorClass = get_parser_visitor_class(lang)
    visitor = ParserVisitorClass(excluded_token_types)

    normalized_tree = visitor.visit(tree)

    return normalized_tree


def ANTLR_parse(file_name, file_content, lang):
    """Parse source code into an ANTLR parse tree and handle syntax errors.


    Args:
        file_name: Name of the source file (used for error reporting).
        file_content: Source code as a string to be parsed.
        lang: programming language of the source code (e.g. python, java, etc.).

    Returns:
        ANTLR parse tree representing the code's syntactic structure.
    """

    tree = None
    parser = None
    input_stream = InputStream(file_content)
    error_listener = ExtendedErrorListener(file_name)

    if lang == "python":
        # Lexing the input code to create a token stream
        lexer = PythonLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(error_listener)
        # Parsing the token stream to create a parse tree
        token_stream = CommonTokenStream(lexer)
        parser = PythonParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)
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
    # If edit distance exceeds the bound given by max(T1, T2),
    # normalize by total nodes to keep the value non-negative.
    if d > max(T1, T2):
        s_alt = 1 - (d / max(T1 + T2, 1))
        s_alt = round(s_alt, 2)
        return s_alt

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


def Compare(
    name_a="Snippet A", content_a="", name_b="Snippet B", content_b="", lang="python"
):
    """Compare two Python code snippets and compute their similarity.

    The comparison process:
    1. Parse both code snippets into ANTLR parse trees
    2. Normalize the parse trees into ZSS tree structures
    3. Compute tree edit distance using Zhang-Shasha algorithm
    4. Calculate normalized similarity index

    Args:
        name_a: Name of the first code snippet (used for error reporting).
        content_a: First Python code snippet as a string.
        name_b: Name of the second code snippet (used for error reporting).
        content_b: Second Python code snippet as a string.
        lang: Programming language of the code snippets (default is "python").

    Returns:
        float: Similarity score in the range [0, 1], where 1 indicates
               identical code structure and 0 indicates maximum difference.
    """

    try:
        # Parse both code snippets into ANTLR parse trees
        T1 = ANTLR_parse(name_a, content_a, lang)
        T2 = ANTLR_parse(name_b, content_b, lang)

        # Normalize parse trees and get node counts
        NT1 = Normalize(T1, lang)
        NT2 = Normalize(T2, lang)

        # Prune and hash the normalized tree
        PT1, len_PT1 = PruneAndHash(NT1, lang)
        PT2, len_PT2 = PruneAndHash(NT2, lang)

        # Compute tree edit distance using Zhang-Shasha algorithm
        d = simple_distance(PT1, PT2, label_dist=label_dist)

        # Calculate and return normalized similarity index
        s = SimilarityIndex(d, len_PT1, len_PT2)
    except Exception as e:
        print(f"Error during comparison: {e}")
        s = None

    return s
