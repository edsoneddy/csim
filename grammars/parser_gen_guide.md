## Parser and Lexer Generation Guide

### ANTLR 4 Installation and Setup on Unix-based Systems

1.  **Verify Java Installation**

    Ensure you have Java installed on your system, as ANTLR requires it to run. You can check your Java version with the following command:
    ```sh
    java -version
    ```

2.  **Download ANTLR**

    Download the ANTLR 4 tool from the [official website](https://www.antlr.org/download.html) or use the following command to download it directly:
    ```sh
    curl -O https://www.antlr.org/download/antlr-4.13.1-complete.jar
    ```

3.  **Configure Classpath**

    Configure the classpath to include the ANTLR JAR file. Add the following line to your shell profile file (e.g., `~/.bashrc`, `~/.zshrc`). Replace `/path/to/` with the actual path where you downloaded the ANTLR JAR file.
    ```sh
    export CLASSPATH=".:/path/to/antlr-4.13.1-complete.jar:$CLASSPATH"
    ```

4.  **Create an Alias**

    Create an alias for the ANTLR tool to simplify its usage. Add the following line to your shell profile file, replacing `/path/to/` with the correct path:
    ```sh
    alias antlr4='java -jar /path/to/antlr-4.13.1-complete.jar'
    ```

5.  **Reload Shell Profile**

    Reload your shell profile to apply the changes:
    ```sh
    source ~/.bashrc  # or source ~/.zshrc
    ```

6.  **Verify Installation**

    Verify the installation by running the following command. You should see the ANTLR usage information.
    ```sh
    antlr4
    ```

### Generating Python3 Parser and Lexer
1.  **Download Grammar Files**

    Download the `PythonLexer.g4` and `PythonParser.g4` grammar files from the [ANTLR grammars repository](https://github.com/antlr/grammars-v4/tree/master/python/python3). Depending on the grammar version you target, paths may vary (e.g., Python 3.13-specific assets live under `python/python3_13`).

2.  **Place Grammar Files**

    Place the downloaded grammar files into the `grammars` directory of this project.

3.  **Generate Parser and Lexer**

    Generate the parser and lexer files using the following commands from the `grammars` directory. This will output the generated files into the `csim/python` directory.
    ```sh
    antlr4 PythonLexer.g4 -Dlanguage=Python3 -visitor -no-listener -o ../csim/python
    antlr4 PythonParser.g4 -Dlanguage=Python3 -visitor -no-listener -o ../csim/python
    ```
    *   `-Dlanguage=Python3`: Specifies that the generated code should be for Python 3.
    *   `-visitor`: Generates a visitor class for traversing the parse tree.
    *   `-no-listener`: Disables the generation of listener classes.
    *   `-o csim/python`: Sets the output directory for the generated files.

4.  **Download Lexer Base Class**

    The Python grammar requires a base class for the lexer. Download the `PythonLexerBase.py` file from the repository and place it in the `csim/python` directory. Run the following command from the root of the project (example for Python 3.13):
    ```sh
    curl -o csim/python/PythonLexerBase.py https://raw.githubusercontent.com/antlr/grammars-v4/refs/heads/master/python/python3_13/Python3/PythonLexerBase.py
    ```

5.  **Verify Generated Files**

    Verify that the generated files (`PythonLexer.py`, `PythonParser.py`, etc.) and the `PythonLexerBase.py` file are present in the `csim/python` directory.

Note: In this project, generated parser/lexer files are already included; regenerating them is optional.


