import argparse
from pathlib import Path
import os
from .DataStructures import UFDS as UnionFind


def get_file(file_path):
    if not Path(file_path).is_file():
        raise argparse.ArgumentTypeError(f"File '{file_path}' does not exist.")
    return file_path


def get_rule_names(lang):
    """Retrieve the parser rule names for a language, indexed by rule index.

    Args:
        lang (str): Programming language identifier.

    Returns:
        list: Rule names indexed by rule index, or None if unavailable.
    """
    if lang == "python_3_13":
        from .python_3_13.PythonParser import PythonParser
        return PythonParser.ruleNames
    elif lang == "java_20":
        from .java_20.Java20Parser import Java20Parser
        return Java20Parser.ruleNames
    elif lang == "java_24":
        from .java_24.Java24Parser import Java24Parser
        return Java24Parser.ruleNames
    elif lang == "cpp_14":
        from .cpp_14.CPP14Parser import CPP14Parser
        return CPP14Parser.ruleNames
    else:
        return None


def get_symbolic_names(lang):
    """Retrieve the lexer symbolic token names for a language, indexed by token type.

    Args:
        lang (str): Programming language identifier.

    Returns:
        list: Symbolic token names indexed by token type, or None if unavailable.
    """
    if lang == "python_3_13":
        from .python_3_13.PythonLexer import PythonLexer
        return PythonLexer.symbolicNames
    elif lang == "java_20":
        from .java_20.Java20Lexer import Java20Lexer
        return Java20Lexer.symbolicNames
    elif lang == "java_24":
        from .java_24.Java24Lexer import Java24Lexer
        return Java24Lexer.symbolicNames
    elif lang == "cpp_14":
        from .cpp_14.CPP14Lexer import CPP14Lexer
        return CPP14Lexer.symbolicNames
    else:
        return None


def format_label(label, rule_names=None, symbolic_names=None):
    """Resolve a normalized-tree label to a human-readable string.

    A label is either a rule index (int), a token type offset by
    TOKEN_TYPE_OFFSET (int), a control-equivalence tag such as "LOOP" (str),
    or a hashed subtree digest in the form "<label>|<hexdigest>" (str).

    Args:
        label: The node label to resolve.
        rule_names: Parser rule names indexed by rule index, or None.
        symbolic_names: Lexer symbolic token names indexed by token type, or None.

    Returns:
        str: Human-readable representation of the label.
    """
    if isinstance(label, str):
        if "|" in label:
            prefix, digest = label.split("|", 1)
            if rule_names and prefix.isdigit() and int(prefix) < len(rule_names):
                prefix = rule_names[int(prefix)]
            return f"{prefix} [hashed:{digest[:8]}]"
        return label
    if isinstance(label, int):
        if label >= TOKEN_TYPE_OFFSET:
            token_type = label - TOKEN_TYPE_OFFSET
            if symbolic_names and 0 <= token_type < len(symbolic_names):
                return symbolic_names[token_type]
            return f"TOKEN<{token_type}>"
        if rule_names and 0 <= label < len(rule_names):
            return rule_names[label]
    return str(label)


def print_tree(node, indent=0, lang=None):
    """Print a normalized/pruned tree with visual indentation.

    Args:
        node: A dict-based tree with "label" and "children" keys.
        indent (int): Current indentation depth.
        lang (str): If given, resolve labels to rule/token names for readability.
    """
    if node is None:
        return

    rule_names = get_rule_names(lang) if lang else None
    symbolic_names = get_symbolic_names(lang) if lang else None

    def _print(n, depth):
        print("   " * depth + format_label(n["label"], rule_names, symbolic_names))
        for child in n["children"]:
            _print(child, depth + 1)

    _print(node, indent)


def print_antlr_tree(node, lang, indent=0):
    """Print a raw ANTLR parse tree with visual indentation, resolving rule names
    and printing terminal token text as leaves.

    Args:
        node: ANTLR parse tree node (rule context or terminal node).
        lang (str): Programming language identifier, used to resolve rule names.
        indent (int): Current indentation depth.
    """
    from antlr4 import TerminalNode

    rule_names = get_rule_names(lang)

    def _print(n, depth):
        if isinstance(n, TerminalNode):
            print("   " * depth + repr(n.getText()))
            return
        rule_index = n.getRuleIndex()
        label = (
            rule_names[rule_index]
            if rule_names and 0 <= rule_index < len(rule_names)
            else str(rule_index)
        )
        print("   " * depth + label)
        for child in n.getChildren():
            _print(child, depth + 1)

    _print(node, indent)


def get_file(file_path):
    if not Path(file_path).is_file():
        raise argparse.ArgumentTypeError(f"File '{file_path}' does not exist.")
    return file_path


def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return file_path, content
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return file_path, None


def get_extension_by_lang(lang):
    if lang == "python_3_13":
        return ".py"
    elif lang == "java_20":
        return ".java"
    elif lang == "java_24":
        return ".java"
    elif lang == "cpp_14":
        return ".cpp"
    else:
        raise ValueError(f"Unsupported language: {lang}")


def process_files(path, lang):
    file_names = []
    file_contents = []

    if path:
        if not os.path.isdir(path):
            raise NotADirectoryError(f"The path '{path}' is not a valid directory.")

        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path) and file.endswith(get_extension_by_lang(lang)):
                file_name, content = read_file(file_path)
                file_names.append(file_name)
                file_contents.append(content)

    return file_names, file_contents


# offset to avoid collision between token types and rule indices
TOKEN_TYPE_OFFSET = 1000


def get_excluded_token_types(lang):
    """Retrieve excluded token types based on the programming language.

    Args:
        lang (str): Programming language identifier.

    Returns:
        set: Set of excluded token types.
    """
    if lang == "python_3_13":
        from .python_3_13.utils import EXCLUDED_TOKEN_TYPES as python_3_13_excluded

        return python_3_13_excluded
    elif lang == "java_20":
        from .java_20.utils import EXCLUDED_TOKEN_TYPES as java_20_excluded

        return java_20_excluded
    elif lang == "java_24":
        from .java_24.utils import EXCLUDED_TOKEN_TYPES as java_24_excluded

        return java_24_excluded
    elif lang == "cpp_14":
        from .cpp_14.utils import EXCLUDED_TOKEN_TYPES as cpp_14_excluded

        return cpp_14_excluded
    else:
        return set()  # Default to empty set for unsupported languages

def get_excluded_rule_types(lang):
    """Retrieve excluded rule types based on the programming language.

    Args:
        lang (str): Programming language identifier.

    Returns:
        set: Set of excluded rule types.
    """
    if lang == "python_3_13":
        from .python_3_13.utils import EXCLUDED_RULE_TYPES as python_3_13_excluded

        return python_3_13_excluded
    elif lang == "java_20":
        from .java_20.utils import EXCLUDED_RULE_TYPES as java_20_excluded

        return java_20_excluded
    elif lang == "java_24":
        from .java_24.utils import EXCLUDED_RULE_TYPES as java_24_excluded

        return java_24_excluded
    elif lang == "cpp_14":
        from .cpp_14.utils import EXCLUDED_RULE_TYPES as cpp_14_excluded

        return cpp_14_excluded
    else:
        return set()  # Default to empty set for unsupported languages

def get_hash_rule_indices(lang):
    """Retrieve hashed rule indices based on the programming language.
    Args:
        lang (str): Programming language identifier.
    Returns:
        set: Set of hashed rule indices.
    """
    if lang == "python_3_13":
        from .python_3_13.utils import HASHED_RULE_INDICES as python_3_13_hashed_rules
        return python_3_13_hashed_rules
    if lang == "java_20":
        from .java_20.utils import HASHED_RULE_INDICES as java_20_hashed_rules
        return java_20_hashed_rules
    if lang == "java_24":
        from .java_24.utils import HASHED_RULE_INDICES as java_24_hashed_rules
        return java_24_hashed_rules
    if lang == "cpp_14":
        from .cpp_14.utils import HASHED_RULE_INDICES as cpp_14_hashed_rules
        return cpp_14_hashed_rules
    else:
        return set()  # Default to empty set for unsupported languages


def get_relabel_fn(lang):
    """Retrieve a language-specific node relabeling hook, if any.

    Some grammars fold constructs that another language's grammar keeps as
    separate rules into one unified rule with ANTLR labeled alternatives
    (e.g. java_24's `expression` covers binary operators, assignments, casts,
    etc. under a single rule index) -- EXCLUDED_RULE_TYPES/HASHED_RULE_INDICES
    can't target just one of those alternatives by rule index alone. This
    hook lets a language's utils.py inspect a node's actual children (e.g.
    the specific operator token) and return a synthetic rule id to use
    instead of the real one, before the rest of Normalize's classification
    runs -- see csim/java_24/utils.py's relabel_node() for the concrete case
    this exists for.

    Args:
        lang (str): Programming language identifier.

    Returns:
        callable(node) -> Optional[int], or None if this language needs no
            relabeling (the default for every language but java_24).
    """
    if lang == "java_24":
        from .java_24.utils import relabel_node
        return relabel_node
    return None


def get_exclude_childrens_from_rule(lang):
    """Retrieve rule indices whose children should be excluded from similarity comparison based on the programming language.

    Args:
        lang (str): Programming language identifier.

    Returns:
        dict: Dictionary mapping rule indices to lists of child indices to exclude.
    """
    if lang == "python_3_13":
        from .python_3_13.utils import (
            EXCLUDE_CHILDRENS_FROM_RULE as python_3_13_exclude_childrens_from_rule,
        )
        return python_3_13_exclude_childrens_from_rule
    if lang == "java_20":
        from .java_20.utils import (
            EXCLUDE_CHILDRENS_FROM_RULE as java_20_exclude_childrens_from_rule,
        )
        return java_20_exclude_childrens_from_rule
    if lang == "java_24":
        from .java_24.utils import (
            EXCLUDE_CHILDRENS_FROM_RULE as java_24_exclude_childrens_from_rule,
        )
        return java_24_exclude_childrens_from_rule
    if lang == "cpp_14":
        from .cpp_14.utils import (
            EXCLUDE_CHILDRENS_FROM_RULE as cpp_14_exclude_childrens_from_rule,
        )
        return cpp_14_exclude_childrens_from_rule
    else:
        return dict()  # Default to empty dict for unsupported languages


def get_control_equivalence_rule_indices(lang):
    """Retrieve control equivalence rule indices based on the programming language.

    Args:
        lang (str): Programming language identifier.

    Returns:
        dict: Dictionary mapping rule indices to their equivalence classes for control flow analysis.
    """
    if lang == "python_3_13":
        from .python_3_13.utils import (
            CONTROL_EQUIVALENCE_RULE_INDICES as python_3_13_control_equivalence_rules,
        )
        return python_3_13_control_equivalence_rules
    if lang == "java_20":
        from .java_20.utils import (
            CONTROL_EQUIVALENCE_RULE_INDICES as java_20_control_equivalence_rules,
        )
        return java_20_control_equivalence_rules
    if lang == "java_24":
        from .java_24.utils import (
            CONTROL_EQUIVALENCE_RULE_INDICES as java_24_control_equivalence_rules,
        )
        return java_24_control_equivalence_rules
    if lang == "cpp_14":
        from .cpp_14.utils import (
            CONTROL_EQUIVALENCE_RULE_INDICES as cpp_14_control_equivalence_rules,
        )
        return cpp_14_control_equivalence_rules
    else:
        return dict()  # Default to empty dict for unsupported languages


def preprocess_code(file_name, file_content, lang="python_3_13"):
    # Local import to avoid circular dependency at module import time
    from .CodeSimilarity import ANTLR_parse, Normalize, PruneAndHash

    T1 = ANTLR_parse(file_name, file_content, lang)
    normalized_tree = Normalize(T1, lang)
    pruned_tree, pruned_count = PruneAndHash(normalized_tree, lang)

    return pruned_tree, pruned_count


def get_similarity_coefficient(proccesed_code1, proccesed_code2, ted_algorithm):
    N1, len_N1 = proccesed_code1
    N2, len_N2 = proccesed_code2

    # Local import to avoid circular dependency at module import time
    from .CodeSimilarity import SimilarityIndex, TreeEditDistance

    d = TreeEditDistance(N1, N2, ted_algorithm)
    result = SimilarityIndex(d, len_N1, len_N2)
    return result


def report_pairwise_similarity(file_names, file_contents, lang, ted_algorithm):

    file_number = len(file_names)
    proccesed_files = [
        preprocess_code(file_names[idx], file_contents[idx], lang)
        for idx in range(file_number)
    ]

    # Create a matrix to store similarity percentages
    similarity_matrix = [
        [None for _ in range(file_number + 1)] for _ in range(file_number + 1)
    ]

    # Fill the first row and first column with file names
    for i in range(file_number):
        display_name = Path(file_names[i]).name
        similarity_matrix[0][i + 1] = display_name
        similarity_matrix[i + 1][0] = display_name

    results = []
    # Calculate similarity percentages and fill the matrix
    for i in range(file_number):
        file_a = proccesed_files[i]
        for j in range(file_number):
            if similarity_matrix[i + 1][j + 1] != None:
                continue
            elif i == j:
                similarity_matrix[i + 1][j + 1] = 1.00
            else:
                file_b = proccesed_files[j]
                similarity_index = get_similarity_coefficient(
                    file_a, file_b, ted_algorithm
                )
                similarity_matrix[i + 1][j + 1] = round(similarity_index, 2)
                similarity_matrix[j + 1][i + 1] = round(similarity_index, 2)
                results.append(
                    f"{file_names[i]} is similar to {file_names[j]} with similarity index: {similarity_index}"
                )

    return "\n".join(results)


def get_output_by_group(file_names, groups, similarity_indices, threshold, printable_output=True):
    result = []
    similarity_groups = []
    similarity_groups_avg = []
    unique_groups = []

    result.append(f"Threshold: {threshold}")
    result.append(f"Total files processed: {len(file_names)}")

    groups_cnt = 1
    for file_group in groups:
        if len(file_group) > 1:
            avg_similarity = sum(
                similarity_indices[file] for file in file_group[1:]
            ) / (len(file_group) - 1)
            result.append(
                f"Group {groups_cnt} (Average Similarity: {avg_similarity:.2f}):"
            )
            result.extend([file_names[file] for file in file_group])
            groups_cnt += 1
            similarity_groups_avg.append(avg_similarity)
            similarity_groups.append([file_names[file] for file in file_group])
        else:
            unique_groups.append(file_names[file_group[0]])

    if len(similarity_groups) > 0 and len(similarity_groups_avg) > 0:
        # Sort the similarity groups by average similarity in descending order
        similarity_groups_avg, similarity_groups = zip(
            *sorted(
                zip(similarity_groups_avg, similarity_groups), key=lambda x: x[0], reverse=True
            )
        )

    if unique_groups:
        result.append(f"Unique Files (similarity below threshold):")
        for file in unique_groups:
            result.append(file)

    if printable_output:
        return "\n".join(result)

    return similarity_groups, similarity_groups_avg, unique_groups, "\n".join(result)


def group_by_exhaustive_search(
    file_names, file_contents, lang, threshold, ted_algorithm, printable_output=True
):

    file_number = len(file_names)
    grouper = UnionFind(file_number)

    proccesed_files = [
        preprocess_code(file_names[idx], file_contents[idx], lang)
        for idx in range(file_number)
    ]

    similarity_indices = [0.00] * file_number

    for i in range(file_number - 1):
        file_a = proccesed_files[i]
        for j in range(i + 1, file_number):
            file_b = proccesed_files[j]
            similarity_index = get_similarity_coefficient(
                file_a, file_b, ted_algorithm
            )
            if similarity_index > threshold:
                grouper.union(i, j)
                similarity_indices[j] = similarity_index

    groups = {}

    for i in range(file_number):
        root = grouper.find(i)
        if root not in groups:
            groups[root] = []
        groups[root].append(i)

    groups = list(groups.values())

    return get_output_by_group(file_names, groups, similarity_indices, threshold, printable_output)
