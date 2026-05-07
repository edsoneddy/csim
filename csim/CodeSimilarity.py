from .language.parser import ANTLR_parse
from .processing.tree_processing import Normalize, PruneAndHash
from .processing.distance_metrics import TreeEditDistance, SimilarityIndex


def Compare(
    name_a="Snippet A",
    content_a="",
    name_b="Snippet B",
    content_b="",
    lang="python",
    ted_algorithm="zss",
):
    """Compare two Python code snippets and compute their similarity.

    The comparison process:
    1. Parse both code snippets into ANTLR parse trees
    2. Normalize the parse trees to a ZSS tree structure, excluding irrelevant tokens and collapsing certain rules.
    3. Prune and hash the normalized trees to reduce noise and improve comparison efficiency.
    4. Compute the tree edit distance using the specified algorithm (e.g., ZSS or APTED).
    5. Calculate and return a normalized similarity index based on the edit distance and tree sizes.

    Args:
        name_a: Name of the first code snippet (used for error reporting).
        content_a: First Python code snippet as a string.
        name_b: Name of the second code snippet (used for error reporting).
        content_b: Second Python code snippet as a string.
        lang: Programming language of the code snippets (default is "python").
        ted_algorithm: The tree edit distance algorithm to use ('zss' or 'apted').
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

        # Compute tree edit distance using the specified algorithm
        d = TreeEditDistance(PT1, PT2, ted_algorithm=ted_algorithm)

        # Calculate and return normalized similarity index
        s = SimilarityIndex(d, len_PT1, len_PT2)
    except Exception as e:
        print(f"Error during comparison: {e}")
        s = None

    return s
