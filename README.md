# Code Similarity

Code Similarity (csim) is a method designed to detect similarity between source codes, even when they have been obfuscated using various techniques. It is ideal for programming teachers and students who want to verify the similitude of the code.

## Key Features

- **Source Code Similarity:** Analyzes and compares source code files to determine their similarity.
- **Advanced Analysis:** Utilizes parse trees, and tree edit distance to perform the analysis.
- **Parse Trees:** Represents the syntactic structure of the source code for detailed analysis.
- **Tree Edit Distance:** To measure the similarity between different code fragments.

## Technologies Used

- **Python:** Main programming language.
- **ANTLR:** For generating parse trees from source code.
- **zss:** For calculating tree edit distance.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/EdsonEddy/csim.git
    ```
2. Navigate to the project directory:
    ```sh
    cd csim
    ```
3. Install the package:
    ```sh
    pip install .
    ```

## Usage

csim can be used from the command line. Here are some usage examples:

```sh
import csim

code_a = "a = 5"
code_b = "c = 50"
similarity = csim.compare(code_a, code_b)
print(f"Similarity: {similarity}")
```

## Parser Generation

This section only describe how to regenerate the parser files, you dont need to do this unless you want to modify the grammar.

The Python parser files (e.g., `PythonLexer.py`, `PythonParser.py`, `PythonParserVisitor.py`) located in the `csim/` directory were generated using the ANTLR 4 tool. The grammar files (`PythonLexer.g4` and `PythonParser.g4`) were sourced from the [antlr/grammars-v4/python3_13](https://github.com/antlr/grammars-v4/tree/master/python/python3_13) repository.

To regenerate these files, you can use the ANTLR JAR tool from within the `grammars/` directory with the following command:

```sh
antlr4 -Dlanguage=Python3 -visitor -o ../csim/ PythonLexer.g4 PythonParser.g4
```

This command instructs ANTLR to generate Python 3 code (`-Dlanguage=Python3`), create a visitor class (`-visitor`), and output the resulting files into the `../csim/` directory.

Additionally, we need download `PythonLexerBase.py` file from the ANTLR4 grammars GitHub repository and move them to the csim directory:
```sh
curl -O https://raw.githubusercontent.com/antlr/grammars-v4/master/python/python3_13/Python3/PythonLexerBase.py 
```

## Contributing

Contributions are welcome. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Links

- [Repository](https://github.com/EdsonEddy/csim)
- [Documentation](https://github.com/EdsonEddy/csim/wiki)
- [Report a Bug](https://github.com/EdsonEddy/csim/issues)

## Additional Documentation
For more information on the techniques used, you can refer to the following resources:

- [ANTLR](https://www.antlr.org/)
- [Parse Trees](https://en.wikipedia.org/wiki/Parse_tree)
- [Tree Edit Distance](https://en.wikipedia.org/wiki/Tree_edit_distance)
- [zss](https://pypi.org/project/zss/1.1.4/)

## Third-Party Licenses

This project uses the following third-party libraries:

### ANTLR (ANother Tool for Language Recognition)
- **Purpose:** Parser generator used to create parse trees from source code
- **License:** BSD 3-Clause License
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

