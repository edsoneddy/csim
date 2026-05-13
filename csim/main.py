import argparse
from .utils import (
    group_by_exhaustive_search,
    group_by_lsh_search,
    process_files,
    report_pairwise_similarity,
)


def main():
    """
    Main function to parse command-line arguments and execute the similarity checker.
    
    Actions:
        report: Generate a pairwise similarity report for all files.
        group: Group files by similarity using a specified strategy.
    
    Arguments for 'report' action:
        --path, -p (str): Path to a directory containing source code files (required).
        --lang, -l (str): The programming language of the source files (default: 'python').
        --talg, -ta (str): The tree edit distance algorithm to use (default: 'zss').
    
    Arguments for 'group' action:
        --path, -p (str): Path to a directory containing source code files (required).
        --threshold, -t (float): Similarity threshold between 0.0 and 1.0 (required).
        --strategy, -s (str): Grouping strategy: 'exhaustive' (default) or 'lsh'.
        --lang, -l (str): The programming language of the source files (default: 'python').
        --talg, -ta (str): The tree edit distance algorithm to use (default: 'zss').
    
    Returns:
        None
    """
    parser = argparse.ArgumentParser(
        description="A command-line tool to detect code similarity and plagiarism."
    )

    # Action argument (positional)
    parser.add_argument(
        "action",
        choices=["report", "group"],
        help="Action to perform: 'report' for pairwise similarity report, 'group' for grouping files by similarity.",
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
        choices=["exhaustive", "lsh"],
        default="exhaustive",
        help="Grouping strategy: 'exhaustive' (all-pairs comparison) or 'lsh' (optimized search). Default: exhaustive.",
    )

    args = parser.parse_args()

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
            parser.error("The --strategy argument is only valid for 'group' action.")

    # Process files
    try:
        file_names, file_contents = process_files(args.path, None, args.lang)

        if len(file_names) < 2:
            print("Error: At least two files are required for comparison.")
            return

        # Execute the appropriate action
        if args.action == "report":
            results = report_pairwise_similarity(
                file_names, file_contents, args.lang, args.talg
            )
        elif args.action == "group":
            if args.strategy == "exhaustive":
                results = group_by_exhaustive_search(
                    file_names, file_contents, args.lang, args.threshold, args.talg
                )
            else:  # lsh
                results = group_by_lsh_search(
                    file_names, file_contents, args.lang, args.threshold, args.talg
                )

        print(results)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
