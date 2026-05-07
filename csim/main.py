import argparse
from .utils import group_by_similarity, process_files, compare_all, get_file


def main():
    """
    Main function to parse command-line arguments and execute the similarity checker.
    Arguments:
        --files, -f (str, nargs=2): The input two files to compare.
        --path, -p (str): Path to the directory containing the source code files.
        --lang, -l (str): The programming language of the source files. Defaults to 'python'.
        --threshold, -t (float): Similarity threshold between 0.0 and 1.0. Only valid when used with --path/-p option.
        --talg, -ta (string): The tree edit distance algorithm to use. Defaults to 'zss'.
        --help, -h: Show this help message and exit.
    Returns:
        None
    """
    parser = argparse.ArgumentParser(
        description="A command-line tool to compare source code files for similarity."
    )

    # A mutually exclusive group for specifying the source of files
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        "--path",
        "-p",
        type=str,
        help="Path to a directory containing source code files. Cannot be used with --files.",
    )
    source_group.add_argument(
        "--files",
        "-f",
        nargs=2,
        metavar=("FILE1", "FILE2"),
        help="Two specific source code files to compare. Cannot be used with --path.",
    )

    # Language of the source files
    parser.add_argument(
        "--lang",
        "-l",
        choices=["python", "java", "cpp"],
        default="python",
        help="The programming language of the source files (default: python).",
    )

    # Optional threshold, only valid when --path is used
    parser.add_argument(
        "--threshold",
        "-t",
        type=float,
        default=None,
        help="Similarity threshold (0.0 to 1.0) for grouping files. Only valid with --path.",
    )

    # Algorithm for tree edit distance
    parser.add_argument(
        "--talg",
        "-ta",
        choices=["zss", "apted"],
        default="zss",
        help="The tree edit distance algorithm to use (default: zss).",
    )

    args = parser.parse_args()

    # Validate that --threshold is only used with --path
    if args.threshold is not None:
        if not args.path:
            parser.error("The --threshold argument can only be used with --path.")
        if not (0.0 <= args.threshold <= 1.0):
            parser.error("The --threshold must be a float between 0.0 and 1.0.")

    # Process files based on the provided arguments
    try:
        file_names, file_contents = process_files(args.path, args.files, args.lang)

        if len(file_names) < 2:
            print("Error: At least two files are required for comparison.")
            return

        if args.path:
            # When a path is provided, compare all files and group by similarity if a threshold is set
            if args.threshold is not None:
                results = group_by_similarity(
                    file_names, file_contents, args.lang, args.threshold, args.talg
                )
            else:
                results = compare_all(file_names, file_contents, args.lang, args.talg)
        else:
            # When two files are provided directly
            results = compare_all(file_names, file_contents, args.lang, args.talg)

        print(results)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
