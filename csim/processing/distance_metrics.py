from zss import simple_distance


def TreeEditDistance(N1, N2, ted_algorithm="zss"):
    """Calculate the tree edit distance between two trees using the specified algorithm.
    Args:
        N1: First tree (root node).
        N2: Second tree (root node).
        ted_algorithm: The tree edit distance algorithm to use ('zss' or 'apted').
    Returns:
        int: The computed tree edit distance between the two trees.
    """
    if ted_algorithm == "zss":
        # Custom configuration for zss to work with dictionaries
        class CustomConfigZss:
            @staticmethod
            def get_children(node):
                return node["children"]

            @staticmethod
            def get_label(node):
                return node["label"]

        d = simple_distance(
            N1,
            N2,
            get_children=CustomConfigZss.get_children,
            get_label=CustomConfigZss.get_label,
        )
    elif ted_algorithm == "apted":
        from apted import APTED, Config

        # Custom configuration for APTED to work with dictionaries
        class CustomConfigApted(Config):
            def rename(self, node1, node2):
                """Compares attribute .value of trees"""
                return 1 if node1["label"] != node2["label"] else 0

            def children(self, node):
                """Get childrens of a node"""
                return node["children"]

        apted = APTED(N1, N2, CustomConfigApted())
        d = apted.compute_edit_distance()
    else:
        d = 0
        raise ValueError(
            f"Unsupported ted_algorithm: {ted_algorithm}. "
            "Supported algorithms are 'zss' and 'apted'."
        )
    return d


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
