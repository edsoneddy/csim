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
    # Create the argument parser
    parser = argparse.ArgumentParser(
        description="Compare two source code files for similarity."
    )

    # Create a mutually exclusive group
    group = parser.add_mutually_exclusive_group(required=True)

    # Add the 'path' argument to the group
    group.add_argument(
        "--path",
        "-p",
        type=str,
        help="Path to the directory containing the source code files to compare.",
    )

    # Add the 'files' argument to the group
    parser.add_argument(
        "--files",
        "-f",
        nargs=2,
        metavar=("FILE1", "FILE2"),
        help="The two source code files to compare.",
        required=True,
    )

    # Add the 'lang' argument to the group
    parser.add_argument(
        "--lang",
        "-l",
        choices=["python", "java", "cpp"],
        default="python",
        help="The programming language of the source files. Defaults to 'python'.",
    )

    # Add the 'lang' argument to the group
    parser.add_argument(
        "--lang",
        "-l",
        choices=["python"],
        default="python",
        help="The programming language of the source files. Defaults to 'python'.",
    )

    # Optional threshold used only when --path is selected
    parser.add_argument(
        "--threshold",
        "-t",
        type=float,
        help="Similarity threshold between 0.0 and 1.0. Only valid when used with --path/-p option.",
    )

    # Optional argument for tree edit distance algorithm
    parser.add_argument(
        "--talg",
        "-ta",
        choices=["zss", "apted"],
        default="zss",
        help="The tree edit distance algorithm to use. Defaults to 'zss'.",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Validate conditional use of --threshold: only allowed with --path
    if args.threshold is not None:
        if not args.path:
            parser.error("argument --threshold: can only be used with --path/-p")
        if not (0.0 <= args.threshold <= 1.0):
            parser.error("argument --threshold: must be between 0.0 and 1.0")

    # Process the files
    file_names, file_contents = process_files(args.path, args.files)

    try:
        if len(file_names) >= 2:
            if args.threshold is not None:
                results = group_by_similarity(
                    file_names, file_contents, args.lang, args.threshold, args.talg
                )
            else:
                results = compare_all(file_names, file_contents, args.lang, args.talg)
        else:
            results = "Please provide at least two files for comparison."
        print(results)
    except Exception as e:
        print(f"An error occurred during comparison: {e}")


if __name__ == "__main__":
    main()
