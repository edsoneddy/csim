import subprocess
import sys
import os

CSIM_EXECUTABLE = os.path.join(os.path.dirname(sys.executable), 'csim')

def test_cli_report_action():
    """
    Testing the execution of the CLI with the 'report' action.
    This generates a pairwise similarity report for all files.
    """
    test_dir = "test/files/"

    command = [CSIM_EXECUTABLE, "report", "-p", test_dir, "-l", "python"]

    result = subprocess.run(command, capture_output=True, text=True, check=False)

    assert result.returncode == 0, f"CLI failed with return code {result.returncode}. Error: {result.stderr}"

    assert result.stdout, "The output of the report command is empty."
    assert "similarity index" in result.stdout, f"The output does not contain the expected text. Output: {result.stdout}"
    print(f"\nOutput of report action:\n{result.stdout}")


def test_cli_group_action_exhaustive():
    """
    Testing the execution of the CLI with the 'group' action using exhaustive strategy.
    This groups files by similarity using all-pairs comparison.
    """
    test_dir = "test/files/"

    command = [CSIM_EXECUTABLE, "group", "-p", test_dir, "-t", "0.8", "-l", "python", "-s", "exhaustive"]

    result = subprocess.run(command, capture_output=True, text=True, check=False)

    assert result.returncode == 0, f"CLI failed with return code {result.returncode}. Error: {result.stderr}"

    assert result.stdout, "The output of the group command is empty."
    assert "Threshold" in result.stdout, f"The output does not contain the expected text. Output: {result.stdout}"
    assert "Total files processed" in result.stdout, f"The output does not contain the expected text. Output: {result.stdout}"
    print(f"\nOutput of group action (exhaustive):\n{result.stdout}")


def test_cli_group_action_lsh():
    """
    Testing the execution of the CLI with the 'group' action using LSH strategy.
    This groups files using Locality Sensitive Hashing for faster performance.
    """
    test_dir = "test/files/"

    command = [CSIM_EXECUTABLE, "group", "-p", test_dir, "-t", "0.8", "-l", "python", "-s", "lsh"]

    result = subprocess.run(command, capture_output=True, text=True, check=False)

    assert result.returncode == 0, f"CLI failed with return code {result.returncode}. Error: {result.stderr}"

    assert result.stdout, "The output of the group command is empty."
    assert "Threshold" in result.stdout, f"The output does not contain the expected text. Output: {result.stdout}"
    assert "Total files processed" in result.stdout, f"The output does not contain the expected text. Output: {result.stdout}"
    print(f"\nOutput of group action (lsh):\n{result.stdout}")


def test_cli_group_action_default_strategy():
    """
    Testing the execution of the CLI with the 'group' action using default strategy (exhaustive).
    If no strategy is specified, exhaustive should be used by default.
    """
    test_dir = "test/files/"

    command = [CSIM_EXECUTABLE, "group", "-p", test_dir, "-t", "0.8", "-l", "python"]

    result = subprocess.run(command, capture_output=True, text=True, check=False)

    assert result.returncode == 0, f"CLI failed with return code {result.returncode}. Error: {result.stderr}"

    assert result.stdout, "The output of the group command is empty."
    assert "Threshold" in result.stdout, f"The output does not contain the expected text. Output: {result.stdout}"
    print(f"\nOutput of group action (default strategy):\n{result.stdout}")


def test_cli_group_missing_threshold():
    """
    Testing that the CLI properly validates that --threshold is required for the 'group' action.
    """
    test_dir = "test/files/"

    command = [CSIM_EXECUTABLE, "group", "-p", test_dir, "-l", "python"]

    result = subprocess.run(command, capture_output=True, text=True, check=False)

    # This should fail because threshold is required for group action
    assert result.returncode != 0, f"CLI should have failed without --threshold. Output: {result.stderr}"
    assert "--threshold" in result.stderr or "required" in result.stderr.lower(), f"Error message should mention --threshold requirement. Error: {result.stderr}"
    print(f"\nCorrectly rejected missing threshold:\n{result.stderr}")
