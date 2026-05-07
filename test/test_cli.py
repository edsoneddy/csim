import subprocess
import sys
import os

CSIM_EXECUTABLE = os.path.join(os.path.dirname(sys.executable), 'csim')

def test_cli_files_option():
    """
        Testing the execution of the CLI with the --files (-f) option.
    """
    file1 = "test/files/prob101.py"
    file2 = "test/files/prob100.py"

    command = [CSIM_EXECUTABLE, "-f", file1, file2, "-l", "python"]

    result = subprocess.run(command, capture_output=True, text=True, check=False)

    assert result.returncode == 0, f"CLI failed with return code {result.returncode}. Error: {result.stderr}"

    assert result.stdout, "The output of the -f command is empty."
    assert "similarity index" in result.stdout, f"The output does not contain the expected text. Output: {result.stdout}"
    print(f"\nOutput of -f:\n{result.stdout}")


def test_cli_path_option():
    """
    Testing the execution of the CLI with the --path (-p) option.
    """
    test_dir = "test/files/"

    command = [CSIM_EXECUTABLE, "-p", test_dir, "-l", "python"]

    result = subprocess.run(command, capture_output=True, text=True, check=False)

    assert result.returncode == 0, f"CLI failed with return code {result.returncode}. Error: {result.stderr}"

    assert result.stdout, "The output of the -p command is empty."
    assert "similarity index" in result.stdout, f"The output does not contain the expected text. Output: {result.stdout}"
    print(f"\nOutput of -p:\n{result.stdout}")
