import argparse
from .utils import process_files, get_file
from .CodeSimilarity import Compare


def main():
    """
    Main function to parse command-line arguments and execute the similarity checker.
    Arguments:
        --files, -f (str, nargs=2): The input two files to compare.
    Returns:
        None
    """
    # Create the argument parser
    parser = argparse.ArgumentParser(
        description="Compare two source code files for similarity."
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
        choices=["python", "java"],
        default="python",
        help="The programming language of the source files. Defaults to 'python'.",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Process the files
    file_names, file_contents = process_files(args)

    if len(file_names) == 2:
        try:
            results = Compare(file_contents[0], file_contents[1], args.lang)
            print(results)
        except Exception as e:
            print(f"An error occurred during comparison: {e}")
    else:
        print("Please provide exactly two files for comparison.")


if __name__ == "__main__":
    main()
