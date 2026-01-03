from .PythonParser import PythonParser
from .PythonLexer import PythonLexer
from .PythonParserVisitor import PythonParserVisitor
from antlr4 import InputStream, CommonTokenStream, TerminalNode
from antlr4 import CommonTokenStream
from .utils import EXCLUDED_RULES, EXCLUDED_TOKENS
from zss import simple_distance, Node


class Visitor(PythonParserVisitor):

    def __init__(self):
        super().__init__()
        self.node_count = 0

    def visitChildren(self, node):
        rule_name = type(node).__name__.replace("Context", "")
        children_nodes = []

        for child in node.getChildren():
            if isinstance(child, TerminalNode):
                text = child.getText()
                if text not in EXCLUDED_TOKENS and text.strip():
                    self.node_count += 1
                    children_nodes.append(Node(f"TOKEN:{text}"))
            else:
                result = self.visit(child)
                if result is not None:
                    children_nodes.append(result)

        # 1. Rules to collapse completely
        if rule_name in EXCLUDED_RULES:
            if len(children_nodes) == 1:
                return children_nodes[0]
            elif len(children_nodes) > 1:
                self.node_count += 1
                group = Node("GROUP")
                for c in children_nodes:
                    group.addkid(c)
                return group
            else:
                return None

        # 2. Valid rule, create node
        self.node_count += 1
        zss_node = Node(rule_name)
        for c in children_nodes:
            zss_node.addkid(c)

        return zss_node


def Normalize(tree):

    visitor = Visitor()
    normalized_tree = visitor.visit(tree)

    return normalized_tree, visitor.node_count


def ANTLR_parse(code):
    input_stream = InputStream(code)
    lexer = PythonLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = PythonParser(token_stream)
    tree = parser.file_input()
    return tree


def SimilarityIndex(d, T1, T2):
    m = max(T1, T2)
    s = 1 - (d / m)
    return s


def Compare(code_a, code_b):
    T1 = ANTLR_parse(code_a)
    T2 = ANTLR_parse(code_b)

    N1, len_N1 = Normalize(T1)
    N2, len_N2 = Normalize(T2)

    d = simple_distance(N1, N2)
    s = SimilarityIndex(d, len_N1, len_N2)
    return s
