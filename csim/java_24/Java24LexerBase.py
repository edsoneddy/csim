from antlr4 import Lexer

class Java24LexerBase(Lexer):
    def __init__(self, input):
        super().__init__(input)
