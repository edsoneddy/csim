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
- **apted:** A library for computing the tree edit distance, alternatively to zss.

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
- **Python:** 3.9–3.12 (recommended 3.11)
- **ANTLR4 Python Runtime:** 4.13.2
- **zss:** 1.2.0
- **apted:** 1.0.3

## Usage
csim can be used from the command line. For now, only Python files are supported; more languages will be added in future versions. 

For example, to compare two Python files, run:

### Option --files (Specify Files)
This option will compare two specified files and output the similarity index.
```sh
csim --files file1.py file2.py
```
### Output
```sh
file1.py is similar to file2.py with similarity index: X.XX
```

### Option --path (Specify Directory)
This option will compare all the files in the specified directory and output the similarity index for each pair of files. This option is expensive in terms of time complexity, so it is recommended to use it with a small number of files.
```sh
csim --path /path/to/directory  
```
### Output
```sh
file1.py is similar to file2.py with similarity index: X.XX
file1.py is similar to file3.py with similarity index: X.XX
...
fileN.py is similar to fileM.py with similarity index: X.XX
```

Notes:
- Only `.py` files within the directory are considered.
- The output uses full file paths when reporting similarities.

### Option --lang (Specify Language)
csim can be used from the command line, supports Python, Java and Cpp source code files. You can specify the language using the `-lang` option. By default `python` is assumed.

For Python files, use:
```sh
csim -f file1.py file2.py -lang python
```

For Java files, use:
```sh
csim -f file1.java file2.java -lang java
```

For Cpp files, use:
```sh
csim -f file1.cpp file2.cpp -lang cpp
```

### Option --threshold (Specify Similarity Threshold)
You can specify a similarity threshold to group files based on their similarity.
Only available when using the `--files` option. If the similarity index is above the threshold, it will be reported in the output.
```sh
csim --path /path/to/directory --threshold 0.7
```
### Output
```sh
Threshold: 0.7
Total files processed: N
Group 1 (Average similarity: X.XX):
  file1.py
  file2.py
Group 2 (Average similarity: X.XX):
  file3.py
  file4.py
...
Unique files (similarity below threshold):
  fileN.py
```

### Option --talg (Specify Tree Edit Distance Algorithm)
You can specify the tree edit distance algorithm to use for comparisons. The available options are `zss` (default) and `apted`.
```sh
csim --files file1.py file2.py --talg apted
```

### Alternatively, you can use csim as a Python module:
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