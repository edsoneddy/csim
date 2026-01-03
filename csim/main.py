import argparse
import sys
import time
import threading
from .utils import process_files, get_file
from .CodeSimilarity import Compare


# Spinner function
def spinner(message):
    stop_spinner = threading.Event()

    def spinning():
        while not stop_spinner.is_set():
            for char in "|/-\\":
                if stop_spinner.is_set():
                    break
                sys.stdout.write(f"\r{message} {char}")
                sys.stdout.flush()
                time.sleep(0.1)

    spinner_thread = threading.Thread(target=spinning, daemon=True)
    spinner_thread.start()
    return stop_spinner.set


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
        description="Code Similarity Checker"
    )

    # Create a mutually exclusive group
    group = parser.add_mutually_exclusive_group(required=True)

    # Add the 'files' argument to the group
    group.add_argument(
        "--files", "-f", type=get_file, nargs=2, help="The input two files to compare"
    )

    # Parse the arguments
    args = parser.parse_args()

    # Process the files
    file_names, file_contents = process_files(args)

    if len(file_names) == 2:
        stop_spinner = spinner("Calculating similarity...")
        try:
            results = Compare(file_contents[0], file_contents[1])
        finally:
            stop_spinner()
            print()
        print(results)
    else:
        print("Error: Please provide exactly two files for comparison.")


if __name__ == "__main__":
    main()
