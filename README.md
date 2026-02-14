# Code Similarity (csim)

Code Similarity (csim) provide a module designed to detect similarities between source code files, even when obfuscation techniques have been applied. It is particularly useful for programming instructors and students who need to verify code originality.

## Key Features

- **Source Code Similarity Analysis:** Compares source code files to determine their degree of similarity.
- **Advanced Analysis:** Utilizes parse trees and the tree edit distance algorithm for in-depth analysis.
- **Parse Trees:** Represents the syntactic structure of source code, enabling detailed comparisons.
- **Tree Edit Distance:** Measures the similarity between different code structures.
- **Hash-Based Pruning:** Optimizes the comparison process by reducing tree size while preserving essential structure.

## Technologies Used

- **Python:** The core programming language for the tool.
- **ANTLR:** A parser generator for creating parse trees from source code.
- **zss:** A library for calculating the tree edit distance.

## Installation

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

### Version Compatibility
- **Python:** 3.9–3.12 (recommended 3.11)
- **ANTLR4 Python Runtime:** 4.13.2
- **zss:** 1.2.0

## Usage
csim can be used from the command line. For now, only Python files are supported; more languages will be added in future versions. For example, to compare two Python files, run:

### Option -f (Specify Files)
This option will compare two specified files and output the similarity index.
```sh
csim -f file1.py file2.py
```
### Output
```
file1.py is similar to file2.py with similarity index: X.XX
```

### Option -p (Specify Directory)
This option will compare all the files in the specified directory and output the similarity index for each pair of files.
```sh
csim --path /path/to/directory  
```
### Output
```
file1.py is similar to file2.py with similarity index: X.XX
file1.py is similar to file3.py with similarity index: X.XX
...
fileN.py is similar to fileM.py with similarity index: X.XX
```

Notes:
- Only `.py` files within the directory are considered.
- The output uses full file paths when reporting similarities.

### Option -l (Specify Language)
You can specify the input language. Currently, only `python` is supported and it is the default.
```sh
csim -f file1.py file2.py --lang python
```

Alternatively, you can use csim as a Python module:
```python
from csim import Compare
code_a = "a = 5"
code_b = "c = 50"
similarity = Compare(name_a = 'example A', content_a = code_a, name_b = 'example B', content_b = code_b)
print(f"Similarity: {similarity}") # Output: Similarity: X.XX
```

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

## Links

- [Repository](https://github.com/EdsonEddy/csim)
- [Documentation](https://github.com/EdsonEddy/csim/wiki)
- [Report a Bug](https://github.com/EdsonEddy/csim/issues)

## Additional Resources

For more information on the techniques and tools used in this project, refer to the following resources:

- [ANTLR](https://www.antlr.org/)
- [Parse Tree (Wikipedia)](https://en.wikipedia.org/wiki/Parse_tree)
- [Tree Edit Distance (Wikipedia)](https://en.wikipedia.org/wiki/Tree_edit_distance)
- [zss (PyPI)](https://pypi.org/project/zss/)
- [Hashing](https://docs.python.org/es/3/library/hashlib.html)

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

