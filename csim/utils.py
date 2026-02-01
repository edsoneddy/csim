import argparse
from pathlib import Path


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
    if args.files is not None:
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
        from .python.utils import EXCLUDED_TOKEN_TYPES as python_excluded

        return python_excluded
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
