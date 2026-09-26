from zss import distance as zss_distance


def label_distance(label1, label2):
    """Compute the substitution cost between two normalized-tree labels.

    Hashed nodes (see tree_processing.hash_children) are stored as
    "RULE_NAME|SHA256_HASH", where the hash digest is computed only from the
    hashed subtree's *children* (the rule label itself isn't part of the
    hashed input). Two hashed nodes get a partial-mismatch cost instead of a
    full one in either of two cases:
    * same rule, different hash -- structurally-different content of the
      same *kind* (e.g. two different but similarly-shaped RHS expressions).
    * different rule, same hash -- the exact same child content, just
      wrapped under a different grammar construct (since the digest doesn't
      depend on the rule label, this can genuinely happen).

    Args:
        label1: First node's label.
        label2: Second node's label.

    Returns:
        float: 0.0 if the labels are identical, 0.5 if both are hashed
            nodes matching on exactly one of {rule, hash}, otherwise 1.0.
    """
    if label1 == label2:
        return 0.0

    str1, str2 = str(label1), str(label2)
    if "|" in str1 and "|" in str2:
        rule1, hash1 = str1.split("|", 1)
        rule2, hash2 = str2.split("|", 1)
        if rule1 == rule2 or hash1 == hash2:
            return 0.5

    return 1.0


def node_weight(node):
    """Cost of inserting or deleting a node: 1, or the mass a hashed node kept."""
    return node.get("weight", 1)


def rename_cost(node1, node2):
    """Substitution cost between two tree nodes (dicts with a 'label').

    Same as label_distance, except two weighted hashed nodes of the same rule
    but different content are charged by how much of their content differs
    (multiset overlap of the labels they replaced) instead of a flat 0.5.
    """
    sig1, sig2 = node1.get("sig"), node2.get("sig")
    if sig1 is None or sig2 is None:
        return label_distance(node1["label"], node2["label"])
    if node1["label"] == node2["label"]:
        return 0.0
    rule1, hash1 = str(node1["label"]).split("|", 1)
    rule2, hash2 = str(node2["label"]).split("|", 1)
    heavy = max(node1["weight"], node2["weight"])
    if rule1 != rule2:
        return heavy if hash1 != hash2 else 0.5 * heavy
    common = sum((sig1 & sig2).values())
    total = sum(sig1.values()) + sum(sig2.values())
    # Different digest means different content even if the multisets match
    # (same labels, other order), so it never costs less than the old flat 0.5.
    return max(heavy * (1.0 - 2.0 * common / total), 0.5)


def TreeEditDistance(N1, N2, ted_algorithm="apted"):
    """Calculate the tree edit distance between two trees using the specified algorithm.
    Args:
        N1: First tree (root node).
        N2: Second tree (root node).
        ted_algorithm: The tree edit distance algorithm to use ('zss' or 'apted').
    Returns:
        int: The computed tree edit distance between the two trees.
    """
    if ted_algorithm == "zss":
        # zss takes per-node cost functions, so weighted hashed nodes work too
        d = zss_distance(
            N1,
            N2,
            get_children=lambda node: node["children"],
            insert_cost=node_weight,
            remove_cost=node_weight,
            update_cost=rename_cost,
        )
    elif ted_algorithm == "apted":
        from apted import APTED, Config

        # Custom configuration for APTED to work with dictionaries
        class CustomConfigApted(Config):
            def rename(self, node1, node2):
                """Compares attribute .value of trees"""
                return rename_cost(node1, node2)

            def delete(self, node):
                return node_weight(node)

            def insert(self, node):
                return node_weight(node)

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


#: Formulas available to SimilarityIndex, see its docstring. "ratio" is the
#: default since 4.0.0; "legacy" reproduces csim <= 3.4.2.
INDEX_FORMULAS = ("ratio", "metric", "legacy")

DEFAULT_INDEX_FORMULA = "ratio"


def SimilarityIndex(d, T1, T2, index_formula=DEFAULT_INDEX_FORMULA):
    """Calculate the similarity index between two trees.

    Normalizes the tree edit distance to a value between 0 and 1, where
    1 indicates identical trees and 0 indicates maximum dissimilarity.

    With `m = max(T1, T2)` and `s = T1 + T2`, the available formulas are:

    * ``ratio`` (default): ``m / (m + d)``. Ranks pairs exactly as ``legacy``
      does -- it is a monotone rescaling of it, so the ROC/AUC of the two is
      identical -- but stays in (0, 1] by construction and needs no fallback
      branch. A fixed cut translates as ``t_ratio = 1 / (2 - t_legacy)``:
      legacy 0.70 == ratio 0.769, legacy 0.80 == ratio 0.833.
    * ``metric``: ``(s - d) / (s + d)``, the metric normalization of tree edit
      distance (Li & Zhang, Front. Comput. Sci. 2011). Satisfies the triangle
      inequality when all insert/delete costs share one weight. Ranks
      differently from ``ratio``: it normalizes by the total size of both
      trees, not by the larger one.
    * ``legacy``: ``1 - d / m``, the index of csim <= 3.4.2, kept to reproduce
      earlier results. ``m`` does not actually bound ``d``, so this formula
      switches denominator to ``s`` above the bound, which makes its scale
      discontinuous; on 6642 real pairs that branch fires once.

    Args:
        d: Tree edit distance between the two trees.
        T1: Number of nodes in the first tree.
        T2: Number of nodes in the second tree.
        index_formula: One of INDEX_FORMULAS (default: "ratio").

    Returns:
        float: Similarity index in the range [0, 1], to 2 decimal places.
    """
    m = max(T1, T2)
    total = max(T1 + T2, 1)

    if index_formula == "ratio":
        s = m / (m + d) if m + d else 1.0
    elif index_formula == "metric":
        s = (total - d) / (total + d)
    elif index_formula == "legacy":
        # If edit distance exceeds the bound given by max(T1, T2),
        # normalize by total nodes to keep the value non-negative.
        s = 1 - (d / total) if d > m else 1 - (d / m)
    else:
        raise ValueError(
            f"Unsupported index_formula: {index_formula}. "
            f"Supported formulas are {', '.join(INDEX_FORMULAS)}."
        )

    # return similarity index with precision of 2 decimal places
    return round(min(max(s, 0.0), 1.0), 2)
