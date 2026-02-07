import argparse
from .utils import process_files, compare_all, get_file
from .CodeSimilarity import Compare


def main():
    """
    Main function to parse command-line arguments and execute the similarity checker.
    Arguments:
        --files, -f (str, nargs=2): The input two files to compare.
        --path, -p (str): Path to the directory containing the source code files.
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
        help="Path to the directory containing the source code files. All files in the directory will be compared against each other.",
    )

    # Add the 'files' argument to the group
    group.add_argument(
        "--files", "-f", type=get_file, nargs=2, help="The input two files to compare"
    )

    # Add the 'lang' argument to the group
    parser.add_argument(
        "--lang",
        "-l",
        choices=["python"],
        default="python",
        help="The programming language of the source files. Defaults to 'python'.",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Process the files
    file_names, file_contents = process_files(args)

    try:
        if len(file_names) == 2:
            results = Compare(file_contents[0], file_contents[1], args.lang)
        elif len(file_names) > 2:
            results = compare_all(file_names, file_contents, args)
        else:
            results = "Please provide exactly two files for comparison."
        print(results)
    except Exception as e:
        print(f"An error occurred during comparison: {e}")


if __name__ == "__main__":
    main()
