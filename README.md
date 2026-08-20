# Code Similarity (csim)

Code Similarity (csim) provide a module designed to detect similarities between source code files, even when obfuscation techniques have been applied. It is particularly useful for programming instructors and students who need to verify code originality.

## Key Features

- **Source Code Similarity Analysis:** Compares source code files to determine their degree of similarity.
- **Pairwise Reporting:** Generate detailed similarity reports for all file pairs.
- **File Grouping:** Cluster similar files into groups based on a configurable threshold.
- **Flexible Search Strategies:** 
  - **Exhaustive Search:** All-pairs comparison for maximum precision
- **Advanced Analysis:** Utilizes parse trees and the tree edit distance algorithm for in-depth analysis.
- **Parse Trees:** Represents the syntactic structure of source code, enabling detailed comparisons.
- **Tree Edit Distance:** Measures the similarity between different code structures.
- **Hash-Based Pruning:** Optimizes the comparison process by reducing tree size while preserving essential structure.
- **Multi-Language Support:** Supports Python 3.13, Python 3 (universal grammar), Java 20, Java 24, and C++14 source code analysis.

## Technologies Used

- **Python:** The core programming language for the tool.
- **ANTLR:** A parser generator for creating parse trees from source code.
- **apted:** A library for computing the tree edit distance (default algorithm).
- **zss:** A library for calculating the tree edit distance, alternatively to apted.
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
- **numpy:** 1.26.4

## Quick Start

**New to csim?** Start here: [GETTING_STARTED.md](GETTING_STARTED.md)

For detailed information about search strategies, see: [docs/STRATEGIES.md](docs/STRATEGIES.md)

csim supports three main actions: **report** (for pairwise similarity analysis), **group** (for clustering similar files), and **tree**/**view** (for visualizing a file's normalized/pruned parse tree). The tool supports Python 3.13, Java 20, Java 24, and C++14 source code files.

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
- `--lang, -l`: Programming language (default: `python_3_13`). Options: `python_3_13`, `python_3`, `java_20`, `java_24`, `cpp_14`, `kotlin`, `c`
- `--talg, -ta`: Tree edit distance algorithm (default: `apted`). Options: `zss`, `apted`

**Example with options:**
```sh
csim report --path /path/to/directory --lang java_20 --talg zss
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

**When to use each:**
- **exhaustive**: Small datasets (< 100 files), when maximum precision is critical

#### Group Action Options

- `--threshold, -t`: Similarity threshold (0.0 to 1.0). **Required.**
- `--strategy, -s`: Grouping strategy (default: `exhaustive`). Options: `exhaustive`
- `--lang, -l`: Programming language (default: `python_3_13`). Options: `python_3_13`, `python_3`, `java_20`, `java_24`, `cpp_14`, `kotlin`, `c`
- `--talg, -ta`: Tree edit distance algorithm (default: `apted`). Options: `zss`, `apted`

**Complete example:**
```sh
csim group --path /path/to/directory --threshold 0.9 --strategy exhaustive --lang python_3_13 --talg zss
```

### Action 3: `tree` (alias: `view`) - Visualize Parse Trees

Prints the normalized/pruned tree for a single file — the exact tree that gets passed to the tree edit distance algorithm. Useful for debugging how the normalization, collapsing, and hashing rules affect a specific file before it's compared against others.

```sh
csim tree --path /path/to/file.py --lang python_3_13
```

**Example Output:**
```
=== Normalized + Pruned Tree (input to Tree Edit Distance) ===
statements
   function_def_raw
      param [hashed:e3b0c442]
      statements
         STRING
         if_stmt
            comparison [hashed:93e10dca]
            return_stmt [hashed:337adaa9]
   assignment [hashed:118045cc]
   primary [hashed:e1b0c7ab]

Total nodes after pruning: 24
```

Rule and token names are resolved for readability, `LOOP` marks nodes collapsed under control-flow equivalence (e.g. `for`/`while`), and `[hashed:xxxxxxxx]` marks subtrees that were hashed into a single node instead of compared structurally.

**Options:**
- `--path, -p`: Path to a single source code file (**required**).
- `--lang, -l`: Programming language (default: `python_3_13`). Options: `python_3_13`, `python_3`, `java_20`, `java_24`, `cpp_14`, `kotlin`, `c`
- `--show-raw`: Also print the raw ANTLR parse tree before normalization/pruning, for side-by-side comparison.

**Example with `--show-raw`:**
```sh
csim tree --path /path/to/file.py --lang python_3_13 --show-raw
```

### Language Support

The tool supports the following programming languages:

**Python 3.13:**
```sh
csim report --path /path/to/python/files --lang python_3_13
```

**Python 3 (universal grammar):**
```sh
csim report --path /path/to/python/files --lang python_3
```

Same `.py` files as `python_3_13`, parsed with grammars-v4's "universal Python 2/3"
grammar, which publishes a C++ target -- giving a large speedup once the native
parser is built (see [Native Parsers](#native-parsers) below). Grouping output is
byte-identical to `python_3_13` on most real-world code (verified against
hundreds of real judge submissions); a narrow, understood exception remains for
files with very few top-level statements, where tree-size differences can
slightly overstate similarity — see `csim/python_3/utils.py` for the full
writeup. Does not parse positional-only parameters (`/`, PEP 570), the walrus
operator (`:=`, PEP 572), or `match`/`case` (PEP 634); csim falls back to
`python_3_13` automatically for files using those, so results stay correct,
just slower for that subset.

**Java 20:**
```sh
csim report --path /path/to/java/files --lang java_20
```

**Java 24 (experimental):**
```sh
csim report --path /path/to/java/files --lang java_24
```

Java 24 uses an optimized grammar (grammars-v4/java/java) that parses much faster
than `java_20` when the native parser is available (see [Native Parsers](#native-parsers)
below), and supports the same modern Java syntax (records, sealed classes, pattern
matching, switch expressions, text blocks). **However, its similarity/grouping
output is not yet tuned to match `java_20` and can be significantly less accurate**
(verified on real submissions — see `CHANGELOG.md`). Use `java_20` for `group`/`report`
until this is resolved; `java_24` is available for parse-speed experimentation only.

**C++14:**
```sh
csim report --path /path/to/cpp/files --lang cpp_14
```

**Kotlin (experimental):**
```sh
csim report --path /path/to/kotlin/files --lang kotlin
```

First-cut integration (grammars-v4/kotlin/kotlin) with a working native parser
(no C++ base class needed at all -- this grammar declares no `superClass`).
Unlike `java_24`/`python_3`, there is no real-world Kotlin corpus in this
project's benchmark set to tune or validate grouping precision against yet, so
the normalization rules (`csim/kotlin/utils.py`) follow the same *categories*
already validated for other languages (structural punctuation, identifier
text, import/package plumbing, body-wrapping content) but haven't been
corpus-measured for false-positive/false-negative rates. Treat `group`/`report`
results as a reasonable starting point, not a tuned config, until a real
corpus drives the next pass.

**C (experimental):**
```sh
csim report --path /path/to/c/files --lang c
```

First-cut integration (grammars-v4/c, ISO C23 + GNU/MSVC extensions), with a
working native parser backed by a real symbol-table implementation for
typedef disambiguation. Like Kotlin, there's no real-world C corpus in this
project's benchmark set to tune grouping precision against yet -- same
caveats apply, see `csim/c/utils.py`.

Runs with preprocessing disabled (`--nopp`) always: a real preprocessor can't
be assumed present in a production container, and judge submissions have no
consistent include paths anyway. `#include`/`#define`/etc. lines are
swallowed as hidden tokens rather than expanded, which means macro-dependent
code (token-pasting tricks, macros used for control flow) can fail to parse
or parse differently than a real compiler would see it -- real submissions
essentially never rely on that, but it's a known, real limitation.

### Native Parsers

For `java_20`, `java_24`, `cpp_14`, `python_3`, `kotlin`, and `c`, csim can
use a compiled C++ ANTLR parser instead of the pure-Python one, giving a
large speedup with identical (or, for `java_24`, not-yet-identical -- see
above) output. `python_3_13` always uses the pure-Python parser (no C++
target is available for that grammar).

Check which backend is active for each language:

```sh
csim info
```

If a native library isn't present for a language, csim falls back to the
pure-Python parser automatically — results are unaffected, only speed. Build
the native parsers from source with:

```sh
scripts/build_native_parsers.sh
```

Set `CSIM_DISABLE_NATIVE=1` to force the pure-Python parsers for every
language, e.g. for debugging or benchmarking.

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
    lang="python_3_13",
    threshold=0.8,
    ted_algorithm="apted"
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
- [Search Strategies Guide](docs/STRATEGIES.md) - Detailed explanation of available search strategies
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

