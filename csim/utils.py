import argparse
from pathlib import Path
import os


def get_file(file_path):
    if not Path(file_path).is_file():
        raise argparse.ArgumentTypeError(f"File '{file_path}' does not exist.")
    return file_path


def print_tree(node, indent=0):
    if node is None:
        return
    print("   " * indent + str(node.label))
    for child in node.children:
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


def process_files(args):
    # Storage for file names and contents
    file_names = []
    file_contents = []

    # Process the files based on the provided arguments
    if args.path:
        path = args.path
        # Check if the path is a valid directory
        if not os.path.isdir(path):
            print(f"Error: The path '{path}' is not a valid directory.")
            return file_names, file_contents
        # Process the files in the directory
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path) and file.endswith(".py"):
                file_name, content = read_file(file_path)
                # Store the file name and content
                file_names.append(file_name)
                file_contents.append(content)
    elif args.files:
        file1, file2 = args.files
        file_name1, content1 = read_file(file1)
        file_name2, content2 = read_file(file2)
        # Store the file name and content
        file_names.extend([file_name1, file_name2])
        file_contents.extend([content1, content2])

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
        from .python.utils import EXCLUDED_TOKEN_TYPES as python_excluded_tokens

        return python_excluded_tokens
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
        set: Set of rule indices whose children should be excluded from similarity comparison.
    """
    if lang == "python":
        from .python.utils import (
            EXCLUDE_CHILDRENS_FROM_RULE as python_exclude_childrens_from_rule,
        )

        return python_exclude_childrens_from_rule
    else:
        return set()  # Default to empty set for unsupported languages


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


from zss import simple_distance


def get_similarity_coefficient(proccesed_code1, proccesed_code2):
    N1, len_N1 = proccesed_code1
    N2, len_N2 = proccesed_code2
    d = simple_distance(N1, N2)
    # Local import to avoid circular dependency at module import time
    from .CodeSimilarity import SimilarityIndex

    result = SimilarityIndex(d, len_N1, len_N2)
    return result


def compare_all(file_names, file_contents, args):

    file_number = len(file_names)
    proccesed_files = [
        preprocess_code(file_names[idx], file_contents[idx], args.lang)
        for idx in range(file_number)
    ]

    # Create a matrix to store similarity percentages
    similarity_matrix = [
        [None for _ in range(file_number + 1)] for _ in range(file_number + 1)
    ]

    # Fill the first row and first column with file names
    for i in range(file_number):
        similarity_matrix[0][i + 1] = file_names[i].split("/")[-1].replace(".py", "")
        similarity_matrix[i + 1][0] = file_names[i].split("/")[-1].replace(".py", "")

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
                similarity_percentage = get_similarity_coefficient(file_a, file_b)
                similarity_matrix[i + 1][j + 1] = round(similarity_percentage, 2)
                similarity_matrix[j + 1][i + 1] = round(similarity_percentage, 2)
                results.append(
                    f"{file_names[i]} is similar to {file_names[j]} with similarity index: {similarity_percentage}"
                )

    return "\n".join(results)
