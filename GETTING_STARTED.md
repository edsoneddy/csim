# Getting Started with csim

This guide will help you get started with csim in just a few minutes.

## Installation

### From PyPI (Recommended)

```bash
pip install csim
```

### From Source

```bash
git clone https://github.com/EdsonEddy/csim.git
cd csim
pip install .
```

## Quick Start

### 1. Generate a Similarity Report

The simplest way to get started is to generate a report comparing all files in a directory:

```bash
csim report --path ./my_assignments
```

**Output:**
```
file1.py is similar to file2.py with similarity index: 0.92
file1.py is similar to file3.py with similarity index: 0.45
file2.py is similar to file3.py with similarity index: 0.50
```

This tells you which files are most similar to each other.

### 2. Group Similar Files

To automatically cluster files into groups of similar submissions:

```bash
csim group --path ./my_assignments --threshold 0.8
```

**Output:**
```
Threshold: 0.8
Total files processed: 3
Group 1 (Average Similarity: 0.92):
./file1.py
./file2.py

Unique Files (similarity below threshold):
./file3.py
```

This groups `file1.py` and `file2.py` together (92% similar), and marks `file3.py` as unique.

### 3. Choose a Search Strategy

For small datasets (< 100 files), the default exhaustive search is fine and guarantees finding all copies:

```bash
csim group --path ./small_dataset --threshold 0.8
```

**Note:** Exhaustive search is O(n²) and may be slow on large datasets.

---

## Common Use Cases

### Use Case 1: Detect Plagiarism in Programming Assignments

You have 30 Python 3.13 submissions for a programming assignment:

```bash
# Generate a report to see all similarities
csim report --path ./submissions/assignment1

# Group them to identify suspicious pairs
csim group --path ./submissions/assignment1 --threshold 0.85
```

**Interpretation:**
- Threshold 0.85 means files need to be 85% structurally similar to be grouped together
- This is intentionally high to minimize false positives
- Review the grouped files manually

### Use Case 2: Quick Duplicate Detection

You have many code files and want to find exact or near-exact duplicates:

```bash
# Threshold 0.95 = nearly identical
csim group --path ./codebase --threshold 0.95
```

### Use Case 3: Code Quality Check

Find copy-pasted functions or redundant code in a codebase:

```bash
# Threshold 0.80 = significantly similar (possible refactoring opportunity)
csim group --path ./src --threshold 0.80 --lang java_20
```

---

## Understanding Thresholds

The `--threshold` parameter determines how similar files must be to be considered a match.

| Threshold | Meaning | Use Case |
|-----------|---------|----------|
| **0.95+** | Nearly identical | Finding exact duplicates |
| **0.85-0.95** | Very similar | Plagiarism detection |
| **0.70-0.85** | Moderately similar | Code review / refactoring suggestions |
| **<0.70** | Somewhat similar | Finding conceptually similar code |

**Recommendation:** Start with 0.85 for plagiarism detection and adjust based on results.

---

## Supported Languages

csim supports five programming language configurations:

### Python 3.13
```bash
csim report --path ./python_files --lang python_3_13
```

### Python 3 (universal grammar, faster)
```bash
csim report --path ./python_files --lang python_3
```
Same `.py` files as `python_3_13`, parsed with a grammar that has a native C++
target (see `csim info`). Grouping output matches `python_3_13` on real code;
does not parse positional-only params (`/`), walrus (`:=`), or `match`/`case` --
csim falls back to `python_3_13` automatically for those files.

### Java 20
```bash
csim report --path ./java_files --lang java_20
```

### Java 24 (experimental — parsing only)
```bash
csim report --path ./java_files --lang java_24
```
Same `.java` files as `java_20`, parsed with an optimized grammar that's much
faster when the native C++ parser is built (see `csim info`). **Not yet
recommended for `group`/`report`**: its similarity output hasn't been tuned to
match `java_20` and can under-report similarity on real code. Use `java_20`
for actual comparisons for now.

### C++14
```bash
csim report --path ./cpp_files --lang cpp_14
```

---

## Advanced Options

### Change Tree Edit Distance Algorithm

By default, csim uses the `apted` algorithm. You can switch to `zss`:

```bash
csim group --path ./files --threshold 0.8 --talg zss
```

Both algorithms compute the same tree edit distance; `apted` is the default.

### Combine Options

```bash
# Large Java 20 assignment dataset (exhaustive search with zss algorithm)
csim group --path ./java_submissions \
  --threshold 0.8 \
  --strategy exhaustive \
  --lang java_20 \
  --talg zss
```

---

## Using csim as a Python Library

For programmatic access, import csim functions directly:

```python
from csim.utils import report_pairwise_similarity

# Your file data
file_names = ["file1.py", "file2.py", "file3.py"]
file_contents = [
    "a = 5\nprint(a)",
    "b = 10\nprint(b)", 
    "import os\nprint('hello')"
]

# Get similarity report
results = report_pairwise_similarity(
    file_names=file_names,
    file_contents=file_contents,
    lang="python_3_13",
    ted_algorithm="apted"
)

print(results)
```

---

## Troubleshooting

### Issue: "No files found"

```bash
csim report --path ./my_directory
```

**Solution:** Make sure the directory contains files with the correct extension (`.py` for Python 3.13, `.java` for Java 20, `.cpp` for C++14).

### Issue: Command not found

```bash
csim: command not found
```

**Solution:** Make sure csim is installed:
```bash
pip install csim
```

Or if installed from source, use:
```bash
python -m csim report --path ./files
```

### Issue: Slow performance on large datasets

```bash
# If you ran this and it's slow:
csim group --path ./1000_files --threshold 0.8 --strategy exhaustive
```

---

## Next Steps

- **Read the full documentation:** See [README.md](README.md)
- **Understand strategies:** Read [docs/STRATEGIES.md](docs/STRATEGIES.md) for detailed comparison
- **Report issues:** Visit [GitHub Issues](https://github.com/EdsonEddy/csim/issues)

---

## Getting Help

- **Questions?** Open a GitHub Discussion
- **Found a bug?** Open a GitHub Issue
- **Want to contribute?** See [README.md](README.md#contributing) for guidelines

Happy plagiarism detection! 🔍
