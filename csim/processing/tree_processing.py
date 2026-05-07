import hashlib
from antlr4 import TerminalNode
from ..Visitors import (
    PythonParserVisitorExtended,
    Java20ParserVisitorExtended,
    CPP14ParserVisitorExtended,
)
from ..utils import (
    TOKEN_TYPE_OFFSET,
    get_control_equivalence_rule_indices,
    get_exclude_childrens_from_rule,
    get_excluded_token_types,
    get_hash_rule_indices,
)


def get_parser_visitor_class(lang):
    """Factory function to create a ParserVisitor class with the correct base visitor.
    Args:
        lang (str): Programming language identifier.
    Returns:
        class: A ParserVisitor class that extends the appropriate base visitor for the given language.
    """
    base_visitor = None
    if lang == "python":
        base_visitor = PythonParserVisitorExtended
    elif lang == "java":
        base_visitor = Java20ParserVisitorExtended
    elif lang == "cpp":
        base_visitor = CPP14ParserVisitorExtended

    if base_visitor is None:
        raise ValueError(f"Unsupported language: {lang}")

    class ParserVisitor(base_visitor):
        """Custom visitor class that extends the base visitor for the specified language.
        This class can be further customized to implement language-specific normalization logic.
        """

        def __init__(self, excluded_token_types):
            super().__init__()
            self.excluded_token_types = excluded_token_types

        def visitChildren(self, node):
            """Visit and process all children of a parse tree node.

            Args:
                node: ANTLR parse tree node to process.

            Returns:
                A dictionary representing the normalized subtree.
            """
            rule_index = node.getRuleIndex()
            children_nodes = []

            for child in node.getChildren():
                if isinstance(child, TerminalNode):
                    token = child.symbol
                    if token.type not in self.excluded_token_types:
                        children_nodes.append(
                            {
                                "label": token.type + TOKEN_TYPE_OFFSET,
                                "children": [],
                            }
                        )
                else:
                    result = self.visit(child)
                    if result is not None:
                        children_nodes.append(result)

            if not children_nodes:
                return {"label": rule_index, "children": []}

            """Node compression: if a node has only one child.
            Can return the child directly to reduce unnecessary levels in the tree.
            """
            if len(children_nodes) == 1:
                # Single child: return it directly to avoid unnecessary nesting
                return children_nodes[0]

            # Create parent node for multiple children
            return {"label": rule_index, "children": children_nodes}

    return ParserVisitor


def PruneAndHash(tree, lang):
    """Prune and hash a tree to reduce noise and improve comparison efficiency.

    Args:
        tree: A dictionary-based tree to prune and hash.
        lang: The programming language of the source code.
    Returns:
        tuple: (hashed_tree, node_count) where hashed_tree is a dictionary
               and node_count is the total number of nodes in the tree.
    """
    hashed_rule_indices = get_hash_rule_indices(lang)
    control_equivalence_rule_indices = get_control_equivalence_rule_indices(lang)
    exclude_childrens_from_rule = get_exclude_childrens_from_rule(lang)

    def traverse_subtree(node):
        # Collect all labels in the subtree rooted at `node` into a single list
        elements = [node["label"]]
        for c in node["children"]:
            elements.extend(traverse_subtree(c))
        return elements

    def prunning_tree(node):
        if node is None:
            return None

        label = node["label"]
        new_node = {"label": label, "children": []}

        # Get the list of child labels to exclude for this rule, if any
        childrens_to_exclude = exclude_childrens_from_rule.get(label, [])

        # Otherwise, recurse normally.
        for children in node["children"]:
            # Skip children that are in the exclusion list for this rule
            if children["label"] in childrens_to_exclude:
                continue
            new_child = prunning_tree(children)
            if new_child is not None:
                new_node["children"].append(new_child)
        return new_node

    def hash_children(label, childrens):
        # Flatten all children subtree labels into a single sequence and hash
        flat = []
        for c in childrens:
            flat.extend(traverse_subtree(c))
        s = "|".join(map(str, flat))
        return str(label) + "|" + hashlib.sha256(s.encode("utf-8")).hexdigest()

    def hashing_tree(node):
        if node is None:
            return None, 0

        # For control flow nodes, we can consider them equivalent regardless of their specific structure
        label = node["label"]
        if label in control_equivalence_rule_indices:
            label = control_equivalence_rule_indices[label]

        # For nodes that are in the hashed rule set, we hash their entire subtree to a single digest
        if node["label"] in hashed_rule_indices:
            digest = hash_children(label, node["children"])
            return {"label": digest, "children": []}, 1

        new_node = {"label": label, "children": []}
        count = 1

        # For other nodes, we recursively hash their children as usual
        for children in node["children"]:
            new_child, child_count = hashing_tree(children)
            if new_child is not None:
                new_node["children"].append(new_child)
                count += child_count
        return new_node, count

    pruned_tree = prunning_tree(tree)
    hashed_tree, nodes_number = hashing_tree(pruned_tree)

    return hashed_tree, nodes_number


def Normalize(tree, lang):
    """Normalize an ANTLR parse tree to a ZSS tree structure, excluding irrelevant tokens and compressing certain rules.

    Args:
        tree: ANTLR parse tree to normalize.
        lang: The programming language of the source code.

    Returns:
        tuple: A ZSS Node representing the normalized tree.
    """
    excluded_token_types = get_excluded_token_types(lang)

    # Get the correct ParserVisitor class for the given language
    ParserVisitorClass = get_parser_visitor_class(lang)
    visitor = ParserVisitorClass(excluded_token_types)

    normalized_tree = visitor.visit(tree)

    return normalized_tree
