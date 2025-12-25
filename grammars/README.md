# ANTLR4 Grammars for Python
1. Generate visitors and parsers using ANTLR4 in the visitors directory:
    ```sh
    antlr4 ./PythonLexer.g4 -visitor -no-listener -Dlanguage=Python3 -o ../csim/
    antlr4 ./PythonParser.g4 -visitor -no-listener -Dlanguage=Python3 -o ../csim/
    ```
2. Download PythonLexerBase from the ANTLR4 grammars GitHub repository and move them to the csim directory:
    ```sh
    curl -O https://raw.githubusercontent.com/antlr/grammars-v4/master/python/python3_13/Python3/PythonLexerBase.py 
    ```