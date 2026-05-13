# Code Similarity (csim)

Code Similarity (csim) provide a module designed to detect similarities between source code files, even when obfuscation techniques have been applied. It is particularly useful for programming instructors and students who need to verify code originality.

## Key Features

- **Source Code Similarity Analysis:** Compares source code files to determine their degree of similarity.
- **Pairwise Reporting:** Generate detailed similarity reports for all file pairs.
- **File Grouping:** Cluster similar files into groups based on a configurable threshold.
- **Flexible Search Strategies:** 
  - **Exhaustive Search:** All-pairs comparison for maximum precision
  - **LSH Optimization:** Fast candidate selection using Locality Sensitive Hashing for large codebases
- **Advanced Analysis:** Utilizes parse trees and the tree edit distance algorithm for in-depth analysis.
- **Parse Trees:** Represents the syntactic structure of source code, enabling detailed comparisons.
- **Tree Edit Distance:** Measures the similarity between different code structures.
- **Hash-Based Pruning:** Optimizes the comparison process by reducing tree size while preserving essential structure.
- **Multi-Language Support:** Supports Python, Java, and C++ source code analysis.

## Technologies Used

- **Python:** The core programming language for the tool.
- **ANTLR:** A parser generator for creating parse trees from source code.
- **zss:** A library for calculating the tree edit distance.
- **apted:** A library for computing the tree edit distance, alternatively to zss.
- **datasketch:** Provides implementations of probabilistic data structures like MinHash for fast similarity estimation.
- **NumPy:** Used for efficient numerical operations.

## Installation
For the installation `pip` is required, you can either clone the repository and install it locally or install it directly from PyPI.

1.  Clone the repository:
    ```sh
    git clone https://github.com/EdsonEddy/csim.git
    ```
2.  Navigate to the project directory:
    ```sh
    cd csim
    ```
3.  Install the package:
    ```sh
    pip install .
    ```

Alternatively, you can install it directly from PyPI:

```sh
pip install csim
```


### Version Compatibility
- **Python:** 3.10–3.12 (recommended 3.11)
- **ANTLR4 Python Runtime:** 4.13.2
- **zss:** 1.2.0
- **apted:** 1.0.3
- **datasketch:** 1.10.0
- **numpy:** 1.26.4

## Quick Start

**New to csim?** Start here: [GETTING_STARTED.md](GETTING_STARTED.md)

For detailed information about search strategies, see: [docs/STRATEGIES.md](docs/STRATEGIES.md)

csim supports two main actions: **report** (for pairwise similarity analysis) and **group** (for clustering similar files). The tool supports Python, Java, and C++ source code files.

### General Command Structure
```sh
csim <action> --path <directory> [options]
```

### Action 1: `report` - Generate Similarity Report

Generates a pairwise similarity report comparing all files in a directory.

```sh
csim report --path /path/to/directory
```

**Example Output:**
```
file1.py is similar to file2.py with similarity index: 0.95
file1.py is similar to file3.py with similarity index: 0.45
file2.py is similar to file3.py with similarity index: 0.50
```

**Options:**
- `--lang, -l`: Programming language (default: `python`). Options: `python`, `java`, `cpp`
- `--talg, -ta`: Tree edit distance algorithm (default: `zss`). Options: `zss`, `apted`

**Example with options:**
```sh
csim report --path /path/to/directory --lang java --talg apted
```

### Action 2: `group` - Group Files by Similarity

Groups files by similarity using a specified threshold and strategy.

```sh
csim group --path /path/to/directory --threshold 0.8
```

**Example Output:**
```
Threshold: 0.8
Total files processed: 4
Group 1 (Average Similarity: 0.98):
./file1.py
./file2.py
Group 2 (Average Similarity: 0.95):
./file3.py
./file4.py
```

#### Strategy Options

The `group` action supports two strategies for finding similar files:

##### 1. **exhaustive** (Default)
Compares every file against every other file (O(n²)). This is the most thorough approach but slower for large datasets.

```sh
csim group --path /path/to/directory --threshold 0.8 --strategy exhaustive
```

##### 2. **lsh** (Optimized)
Uses Locality Sensitive Hashing (LSH) to quickly identify candidate pairs before detailed structural comparison. This is significantly faster for large codebases while maintaining high accuracy.

```sh
csim group --path /path/to/directory --threshold 0.8 --strategy lsh
```

**When to use each:**
- **exhaustive**: Small datasets (< 100 files), when maximum precision is critical
- **lsh**: Large datasets (> 100 files), when speed is important

#### Group Action Options

- `--threshold, -t`: Similarity threshold (0.0 to 1.0). **Required.**
- `--strategy, -s`: Grouping strategy (default: `exhaustive`). Options: `exhaustive`, `lsh`
- `--lang, -l`: Programming language (default: `python`). Options: `python`, `java`, `cpp`
- `--talg, -ta`: Tree edit distance algorithm (default: `zss`). Options: `zss`, `apted`

**Complete example:**
```sh
csim group --path /path/to/directory --threshold 0.9 --strategy lsh --lang python --talg apted
```

### Language Support

The tool supports the following programming languages:

**Python:**
```sh
csim report --path /path/to/python/files --lang python
```

**Java:**
```sh
csim report --path /path/to/java/files --lang java
```

**C++:**
```sh
csim report --path /path/to/cpp/files --lang cpp
```

### Threshold Guidance

The similarity threshold represents the structural similarity of the code (based on the Abstract Syntax Tree). Choose appropriate thresholds based on your use case:

- **0.95+**: Nearly identical code (likely plagiarism)
- **0.85-0.95**: Very similar code (probable plagiarism)
- **0.70-0.85**: Moderately similar code (review recommended)
- **<0.70**: Low similarity (likely independent work)

### Using csim as a Python Module

You can also use csim programmatically within your Python code. The library provides low-level functions for advanced use cases:

```python
from csim.utils import group_by_exhaustive_search, report_pairwise_similarity

# Example: Group files by similarity
file_names = ["file1.py", "file2.py", "file3.py"]
file_contents = [code1, code2, code3]

results = group_by_exhaustive_search(
    file_names=file_names,
    file_contents=file_contents,
    lang="python",
    threshold=0.8,
    ted_algorithm="zss"
)

print(results)
```

Or use the legacy Compare class for simple pairwise comparisons:

```python
from csim import Compare

code_a = "a = 5"
code_b = "c = 50"
similarity = Compare(name_a='example A', content_a=code_a, name_b='example B', content_b=code_b)
print(f"Similarity: {similarity}") # Output: Similarity: X.XX
```

## Documentation

- [Getting Started Guide](GETTING_STARTED.md) - Quick tutorial for new users
- [Search Strategies Guide](docs/STRATEGIES.md) - Detailed comparison of exhaustive vs. LSH approaches
- [Changelog](CHANGELOG.md) - Version history and recent changes
- [ANTLR Parser Generation](grammars/parser_gen_guide.md) - For grammar customization

## ANTLR4 Installation and Parser/Lexer Generation

This installation is not required—the generated files are already included in the project. If you'd like to review the steps to generate them yourself, see [grammars/parser_gen_guide.md](grammars/parser_gen_guide.md).

Note: The included generated files were produced by **ANTLR 4.13.2** and are compatible with the pinned runtime listed above.

## Contributing

Contributions are welcome! To contribute, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/new-feature`).
3.  Make your changes and commit them (`git commit -am 'Add new feature'`).
4.  Push to the branch (`git push origin feature/new-feature`).
5.  Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

- **Questions?** Open a [GitHub Discussion](https://github.com/EdsonEddy/csim/discussions)
- **Found a bug?** File a [GitHub Issue](https://github.com/EdsonEddy/csim/issues)
- **Want to contribute?** See [Contributing](#contributing) section

## References

For more information on the techniques and tools used in this project, refer to the following resources:

- [ANTLR](https://www.antlr.org/)
- [Parse Tree (Wikipedia)](https://en.wikipedia.org/wiki/Parse_tree)
- [Tree Edit Distance (Wikipedia)](https://en.wikipedia.org/wiki/Tree_edit_distance)
- [Locality Sensitive Hashing (Wikipedia)](https://en.wikipedia.org/wiki/Locality-sensitive_hashing)
- [MinHash (Wikipedia)](https://en.wikipedia.org/wiki/MinHash)
- [zss (PyPI)](https://pypi.org/project/zss/)
- [Hashing (Python Docs)](https://docs.python.org/3/library/hashlib.html)
- [apted (GitHub)](https://github.com/JoaoFelipe/apted)
- [datasketch (PyPI)](https://pypi.org/project/datasketch/)

## Third-Party Licenses

This project utilizes the following third-party libraries:

### ANTLR (ANother Tool for Language Recognition)
- **Purpose:** A parser generator used to create parse trees from source code.
- **License:** BSD 3-Clause
- **Website:** [https://www.antlr.org/](https://www.antlr.org/)
- **Repository:** [https://github.com/antlr/antlr4](https://github.com/antlr/antlr4)

### ANTLR4-parser-for-Python-3.14 by RobEin
- **Purpose:** Python 3.14 grammar for ANTLR4
- **License:** MIT License
- **Repository:** [https://github.com/RobEin/ANTLR4-parser-for-Python-3.14](https://github.com/RobEin/ANTLR4-parser-for-Python-3.14)

### zss (Zhang-Shasha)
- **Purpose:** Tree edit distance algorithm implementation for comparing tree structures
- **License:** MIT License
- **Repository:** [https://github.com/timtadh/zhang-shasha](https://github.com/timtadh/zhang-shasha)

### apted (All Path Tree Edit Distance)
- **Purpose:** Python APTED algorithm for the Tree Edit Distance, an alternative to zss
- **License:** MIT License
- **Repository:** [https://github.com/JoaoFelipe/apted](https://github.com/JoaoFelipe/apted)

### datasketch
- **Purpose:** Provides probabilistic data structures including MinHash for fast similarity estimation
- **License:** MIT License
- **Repository:** [https://github.com/ekzhu/datasketch](https://github.com/ekzhu/datasketch)