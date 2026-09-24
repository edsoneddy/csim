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
    parser = argparse.ArgumentParser(
        description="A command-line tool to detect code similarity and plagiarism."
    )
    parser.add_argument(
        "action",
        choices=["report", "group", "tree", "view"],
        help="Action to perform: report, group, tree, or view.",
    )
    parser.add_argument(
        "--path",
        "-p",
        type=str,
        help="Path to a directory, or a single source file for tree/view.",
    )
    parser.add_argument(
        "--lang",
        "-l",
        choices=["python", "python_3_13", "java", "cpp"],
        default="python",
        help="The programming language of the source files (default: python).",
    )
    parser.add_argument(
        "--talg",
        "-ta",
        choices=["zss", "apted"],
        default="zss",
        help="The tree edit distance algorithm to use (default: zss).",
    )
    parser.add_argument(
        "--threshold",
        "-t",
        type=float,
        default=None,
        help="Similarity threshold for grouping files.",
    )
    parser.add_argument(
        "--strategy",
        "-s",
        choices=["exhaustive"],
        default="exhaustive",
        help="Grouping strategy (default: exhaustive).",
    )
    parser.add_argument(
        "--show-raw",
        action="store_true",
        help="For tree/view, also print the raw ANTLR parse tree.",
    )

    args = parser.parse_args()
    if not args.path:
        parser.error("The --path argument is required for this action.")

    if args.action in ("tree", "view"):
        if not os.path.isfile(args.path):
            parser.error(f"The path '{args.path}' is not a valid file.")

        tree_lang = "python" if args.lang == "python_3_13" else args.lang
        with open(args.path, "r", encoding="utf-8") as file:
            file_content = file.read()

        raw_tree = ANTLR_parse(args.path, file_content, tree_lang)
        if args.show_raw:
            print("=== Raw ANTLR Parse Tree ===")
            print_antlr_tree(raw_tree, tree_lang)
            print()

        normalized_tree = Normalize(raw_tree, tree_lang)
        pruned_tree, node_count = PruneAndHash(normalized_tree, tree_lang)
        print("=== Normalized + Pruned Tree (input to Tree Edit Distance) ===")
        print_tree(pruned_tree, lang=tree_lang)
        print(f"\nTotal nodes after pruning: {node_count}")
        return

    if args.action == "group":
        if args.threshold is None:
            parser.error("The --threshold argument is required for 'group' action.")
        if not 0.0 <= args.threshold <= 1.0:
            parser.error("The --threshold must be a float between 0.0 and 1.0.")
    elif args.action == "report":
        if args.threshold is not None:
            parser.error("The --threshold argument is only valid for 'group' action.")
        if args.strategy != "exhaustive":
            parser.error("The --strategy argument is only valid for 'group' action.")

    try:
        file_names, file_contents = process_files(args.path, args.lang)
    except (FileNotFoundError, NotADirectoryError, ValueError) as exc:
        parser.error(str(exc))

    if len(file_names) < 2:
        parser.error("At least two files are required for comparison.")

    if args.action == "report":
        results = report_pairwise_similarity(file_names, file_contents, args.lang, args.talg)
    else:
        results = group_by_exhaustive_search(
            file_names, file_contents, args.lang, args.threshold, args.talg
        )
    print(results)


if __name__ == "__main__":
    main()
