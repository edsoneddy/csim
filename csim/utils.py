import argparse
from pathlib import Path
import os
from .DataStructures import UFDS as UnionFind


def get_file(file_path):
    if not Path(file_path).is_file():
        raise argparse.ArgumentTypeError(f"File '{file_path}' does not exist.")
    return file_path


def get_rule_names(lang):
    if lang == "python":
        from .python.PythonParser import PythonParser
        return PythonParser.ruleNames
    if lang == "java":
        from .java.Java20Parser import Java20Parser
        return Java20Parser.ruleNames
    if lang == "cpp":
        from .cpp.CPP14Parser import CPP14Parser
        return CPP14Parser.ruleNames
    return None


def get_symbolic_names(lang):
    if lang == "python":
        from .python.PythonLexer import PythonLexer
        return PythonLexer.symbolicNames
    if lang == "java":
        from .java.Java20Lexer import Java20Lexer
        return Java20Lexer.symbolicNames
    if lang == "cpp":
        from .cpp.CPP14Lexer import CPP14Lexer
        return CPP14Lexer.symbolicNames
    return None


def format_label(label, rule_names=None, symbolic_names=None):
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
    if node is None:
        return

    rule_names = get_rule_names(lang) if lang else None
    symbolic_names = get_symbolic_names(lang) if lang else None

    def _print(current_node, depth):
        print("   " * depth + format_label(current_node["label"], rule_names, symbolic_names))
        for child in current_node["children"]:
            _print(child, depth + 1)

    _print(node, indent)


def print_antlr_tree(node, lang, indent=0):
    from antlr4 import TerminalNode

    rule_names = get_rule_names(lang)

    def _print(current_node, depth):
        if isinstance(current_node, TerminalNode):
            print("   " * depth + repr(current_node.getText()))
            return
        rule_index = current_node.getRuleIndex()
        label = (
            rule_names[rule_index]
            if rule_names and 0 <= rule_index < len(rule_names)
            else str(rule_index)
        )
        print("   " * depth + label)
        for child in current_node.getChildren():
            _print(child, depth + 1)

    _print(node, indent)


def count_antlr_tree_nodes(node):
    """Return the number of rule and terminal nodes in an ANTLR tree."""
    if node is None:
        return 0
    from antlr4 import TerminalNode

    if isinstance(node, TerminalNode):
        return 1

    return 1 + sum(count_antlr_tree_nodes(child) for child in node.getChildren())


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
    if lang == "python":
        return ".py"
    elif lang == "java":
        return ".java"
    elif lang == "cpp":
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
    if lang == "python":
        from .python.utils import EXCLUDED_TOKEN_TYPES as python_excluded

        return python_excluded
    elif lang == "java":
        from .java.utils import EXCLUDED_TOKEN_TYPES as java_excluded

        return java_excluded
    elif lang == "cpp":
        from .cpp.utils import EXCLUDED_TOKEN_TYPES as cpp_excluded

        return cpp_excluded
    else:
        return set()  # Default to empty set for unsupported languages


def get_hash_rule_indices(lang):
    """Retrieve hashed rule indices based on the programming language.
    Args:
        lang (str): Programming language identifier.
    Returns:
        set: Set of hashed rule indices.
    """
    if lang == "python":
        from .python.utils import HASHED_RULE_INDICES as python_hashed_rules

        return python_hashed_rules
    else:
        return set()  # Default to empty set for unsupported languages


def get_exclude_childrens_from_rule(lang):
    """Retrieve rule indices whose children should be excluded from similarity comparison based on the programming language.

    Args:
        lang (str): Programming language identifier.

    Returns:
        dict: Dictionary mapping rule indices to lists of child indices to exclude.
    """
    if lang == "python":
        from .python.utils import (
            EXCLUDE_CHILDRENS_FROM_RULE as python_exclude_childrens_from_rule,
        )

        return python_exclude_childrens_from_rule
    else:
        return dict()  # Default to empty dict for unsupported languages


def get_control_equivalence_rule_indices(lang):
    """Retrieve control equivalence rule indices based on the programming language.

    Args:
        lang (str): Programming language identifier.

    Returns:
        dict: Dictionary mapping rule indices to their equivalence classes for control flow analysis.
    """
    if lang == "python":
        from .python.utils import (
            CONTROL_EQUIVALENCE_RULE_INDICES as python_control_equivalence_rules,
        )

        return python_control_equivalence_rules
    else:
        return dict()  # Default to empty dict for unsupported languages


def preprocess_code(file_name, file_content, lang="python"):
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


def get_output_by_group(file_names, groups, similarity_indices, threshold):
    result = []
    unique_files = []

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
        else:
            unique_files.append(file_names[file_group[0]])

    if unique_files:
        result.append(f"Unique Files (similarity below threshold):")
        for file in unique_files:
            result.append(file)

    return "\n".join(result)


def group_by_exhaustive_search(
    file_names, file_contents, lang, threshold, ted_algorithm
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

    return get_output_by_group(file_names, groups, similarity_indices, threshold)
