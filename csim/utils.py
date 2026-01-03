EXCLUDED_RULES = {
    # wrappers
    "Statement",
    "Statements",
    "Simple_stmts",
    "Simple_stmt",
    "Star_expression",
    "Star_expressions",
    "Function_def_raw",
    # precedence / expressions
    "Disjunction",
    "Conjunction",
    "Inversion",
    "Comparison",
    "Bitwise_or",
    "Bitwise_xor",
    "Bitwise_and",
    "Shift_expr",
    "Sum",
    "Term",
    "Factor",
    "Power",
    "Await_primary",
    "Primary",
    "Atom",
    # names
    "Name",
    "Name_except_underscore",
    # other technicals
    "Target_with_star_atom",
    "Star_atom",
    # collapse rules
    "Import_name",
    "Dotted_as_names",
    "Dotted_as_name",
    "Dotted_name",
}

EXCLUDED_TOKENS = {"(", ")", ":", ",", "<INDENT>", "<DEDENT>", "<EOF>"}

import argparse
from pathlib import Path

# Utility functions for argument parsing


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
