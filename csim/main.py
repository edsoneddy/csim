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
    parser = argparse.ArgumentParser(description="Code Similarity Checker")

    # Create a mutually exclusive group
    group = parser.add_mutually_exclusive_group(required=True)

    # Add the 'files' argument to the group
    group.add_argument(
        "--files", "-f", type=get_file, nargs=2, help="The input two files to compare"
    )

    # Add the 'lang' argument to the group
    group.add_argument(
        "--lang", "-l", type=str, help="The programming language to use for comparison (e.g., python, java)", default="python"
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
