import argparse
from pathlib import Path
import os
from .DataStructures import UFDS as UnionFind


def get_file(file_path):
    if not Path(file_path).is_file():
        raise argparse.ArgumentTypeError(f"File '{file_path}' does not exist.")
    return file_path


def print_tree(node, indent=0):
    if node is None:
        return
    print("   " * indent + str(node["label"]))
    for child in node["children"]:
        print_tree(child, indent + 1)


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
