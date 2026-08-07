import argparse
import os
from .language.parser import ANTLR_parse
from .processing.tree_processing import Normalize, PruneAndHash
from .utils import (
    group_by_exhaustive_search,
    print_antlr_tree,
    print_tree,
    process_files,
    report_pairwise_similarity,
)


def main():
    """
    Main function to parse command-line arguments and execute the similarity checker.
    
    Actions:
        report: Generate a pairwise similarity report for all files.
        group: Group files by similarity using a specified strategy.
        tree (alias: view): Print the normalized/pruned tree for a single file,
            i.e. the exact tree that gets passed to the tree edit distance algorithm.

    Arguments for 'report' action:
        --path, -p (str): Path to a directory containing source code files (required).
        --lang, -l (str): The programming language of the source files (default: 'python').
        --talg, -ta (str): The tree edit distance algorithm to use (default: 'zss').

    Arguments for 'group' action:
        --path, -p (str): Path to a directory containing source code files (required).
        --threshold, -t (float): Similarity threshold between 0.0 and 1.0 (required).
        --strategy, -s (str): Grouping strategy: 'exhaustive' (default).
        --lang, -l (str): The programming language of the source files (default: 'python').
        --talg, -ta (str): The tree edit distance algorithm to use (default: 'zss').

    Arguments for 'tree'/'view' action:
        --path, -p (str): Path to a single source code file (required).
        --lang, -l (str): The programming language of the source file (default: 'python').
        --show-raw: Also print the raw ANTLR parse tree before normalization/pruning.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(
        description="A command-line tool to detect code similarity and plagiarism."
    )

    # Action argument (positional)
    parser.add_argument(
        "action",
        choices=["report", "group", "tree", "view"],
        help="Action to perform: 'report' for pairwise similarity report, 'group' for grouping "
        "files by similarity, 'tree'/'view' to print a single file's normalized/pruned tree.",
    )

    # Required path argument
    parser.add_argument(
        "--path",
        "-p",
        type=str,
        required=True,
        help="Path to a directory containing source code files.",
    )

    # Language of the source files
    parser.add_argument(
        "--lang",
        "-l",
        choices=["python", "java", "cpp"],
        default="python",
        help="The programming language of the source files (default: python).",
    )

    # Algorithm for tree edit distance
    parser.add_argument(
        "--talg",
        "-ta",
        choices=["zss", "apted"],
        default="zss",
        help="The tree edit distance algorithm to use (default: zss).",
    )

    # Threshold (only for 'group' action)
    parser.add_argument(
        "--threshold",
        "-t",
        type=float,
        default=None,
        help="Similarity threshold (0.0 to 1.0) for grouping files. Required for 'group' action.",
    )

    # Strategy (only for 'group' action)
    parser.add_argument(
        "--strategy",
        "-s",
        choices=["exhaustive"],
        default="exhaustive",
        help="Grouping strategy: 'exhaustive' (all-pairs comparison). Default: exhaustive.",
    )

    # Raw tree flag (only for 'tree'/'view' action)
    parser.add_argument(
        "--show-raw",
        action="store_true",
        help="For the 'tree'/'view' action, also print the raw ANTLR parse tree "
        "before normalization/pruning.",
    )

    args = parser.parse_args()

    if args.action in ("tree", "view"):
        if not os.path.isfile(args.path):
            parser.error(f"The path '{args.path}' is not a valid file.")

        with open(args.path, "r", encoding="utf-8") as file:
            file_content = file.read()

        raw_tree = ANTLR_parse(args.path, file_content, args.lang)

        if args.show_raw:
            print("=== Raw ANTLR Parse Tree ===")
            print_antlr_tree(raw_tree, args.lang)
            print()

        normalized_tree = Normalize(raw_tree, args.lang)
        pruned_tree, node_count = PruneAndHash(normalized_tree, args.lang)

        print("=== Normalized + Pruned Tree (input to Tree Edit Distance) ===")
        print_tree(pruned_tree, lang=args.lang)
        print(f"\nTotal nodes after pruning: {node_count}")
        return

    # Validate arguments based on action
    if args.action == "group":
        if args.threshold is None:
            parser.error("The --threshold argument is required for 'group' action.")
        if not (0.0 <= args.threshold <= 1.0):
            parser.error("The --threshold must be a float between 0.0 and 1.0.")
    elif args.action == "report":
        if args.threshold is not None:
            parser.error("The --threshold argument is only valid for 'group' action.")
        if args.strategy != "exhaustive":
            parser.error("The --strategy argument is only valid for 'group' action and must be 'exhaustive'.")

    try:
        file_names, file_contents = process_files(args.path, args.lang)
    except (FileNotFoundError, NotADirectoryError, ValueError) as exc:
        parser.error(str(exc))

    if len(file_names) < 2:
        parser.error("At least two files are required for comparison.")

    if args.action == "report":
        results = report_pairwise_similarity(
            file_names, file_contents, args.lang, args.talg
        )
    elif args.action == "group":
        results = group_by_exhaustive_search(
            file_names, file_contents, args.lang, args.threshold, args.talg
        )

    print(results)


if __name__ == "__main__":
    main()
