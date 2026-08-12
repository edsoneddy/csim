"""Rebuild an ANTLR-compatible parse tree from the native flat buffer.

The C++ bridge emits the tree as a flat preorder int32 sequence:

    [(label, num_children), (label, num_children), ...]

with labels encoded so that terminals can never collide with rule indices:

    label <  TERMINAL_BASE  ->  rule node,     rule_index = label
    label >= TERMINAL_BASE  ->  terminal node, token_type = label - TERMINAL_BASE - 1

The +1 shift exists because EOF carries token type -1; without it EOF would land
back inside the rule-index space and be rebuilt as a bogus rule node.

The nodes built here expose only what the existing visitors touch
(``getRuleIndex``, ``getChildren``, ``getChild``, ``getChildCount``, ``accept``,
and ``symbol.type`` on terminals), so ``Normalize`` runs against them unchanged.
"""

from antlr4.tree.Tree import TerminalNode

# Must match TERMINAL_BASE in the C++ bridges (grammars/cpp_build/*/bridge_fast.cpp).
TERMINAL_BASE = 1000000


class _Symbol:
    """Minimal stand-in for an ANTLR token, carrying just the type."""

    __slots__ = ("type", "text")

    def __init__(self, token_type, text=""):
        self.type = token_type
        self.text = text


class NativeTerminalNode(TerminalNode):
    """Terminal node backed by the flat buffer.

    Subclasses ANTLR's ``TerminalNode`` so the ``isinstance(child, TerminalNode)``
    checks in the visitors keep working.
    """

    __slots__ = ("symbol", "parentCtx")

    def __init__(self, token_type, text=""):
        self.symbol = _Symbol(token_type, text)
        self.parentCtx = None

    def getText(self):
        return self.symbol.text

    def getChildCount(self):
        return 0

    def getChildren(self):
        return []

    def accept(self, visitor):
        return visitor.visitTerminal(self)

    def __repr__(self):
        return f"<NativeTerminal type={self.symbol.type}>"


class NativeRuleNode:
    """Rule node backed by the flat buffer.

    ``accept`` reproduces ANTLR's generated dispatch: a rule named ``foo`` is
    routed to ``visitFoo`` when the visitor defines it, else to ``visitChildren``.
    """

    __slots__ = ("_rule_index", "children", "_visit_method")

    def __init__(self, rule_index, visit_method):
        self._rule_index = rule_index
        self.children = []
        self._visit_method = visit_method

    def getRuleIndex(self):
        return self._rule_index

    def getChildren(self):
        return self.children

    def getChild(self, i):
        return self.children[i]

    def getChildCount(self):
        return len(self.children)

    def getText(self):
        return "".join(child.getText() for child in self.children)

    def accept(self, visitor):
        method = getattr(visitor, self._visit_method, None)
        if method is not None:
            return method(self)
        return visitor.visitChildren(self)

    def __repr__(self):
        return f"<NativeRule index={self._rule_index} children={len(self.children)}>"


def _visit_method_names(rule_names):
    """Precompute the ANTLR visitor method name for every rule index."""
    return [
        "visit" + name[:1].upper() + name[1:] if name else "visitChildren"
        for name in rule_names
    ]


def build_tree(buffer, rule_names, literal_names=None):
    """Rebuild the parse tree from a flat preorder buffer.

    Built iteratively rather than recursively so that deeply nested sources
    cannot blow the Python stack during construction.

    Args:
        buffer: Flat int32 sequence of (label, num_children) pairs, preorder.
        rule_names: Parser rule names indexed by rule index.
        literal_names: Lexer literal names indexed by token type; used to give
            terminals their source text. Optional.

    Returns:
        The root node, or None when the buffer is empty.

    Raises:
        ValueError: If the buffer is malformed (odd length or truncated).
    """
    if not buffer:
        return None
    if len(buffer) % 2 != 0:
        raise ValueError(f"Malformed native buffer: odd length {len(buffer)}")

    visit_methods = _visit_method_names(rule_names)
    total = len(literal_names) if literal_names else 0

    def _terminal_text(token_type):
        if literal_names and 0 <= token_type < total:
            literal = literal_names[token_type]
            # ANTLR stores literals quoted ("'+='"); bare names mean no literal.
            if len(literal) >= 2 and literal[0] == "'" and literal[-1] == "'":
                return literal[1:-1]
        return ""

    root = None
    # Stack of [node, remaining_children] for the open ancestors.
    stack = []
    index = 0
    size = len(buffer)

    while index < size:
        label = buffer[index]
        num_children = buffer[index + 1]
        index += 2

        if label >= TERMINAL_BASE:
            token_type = label - TERMINAL_BASE - 1
            node = NativeTerminalNode(token_type, _terminal_text(token_type))
            is_leaf = True
        else:
            method = (
                visit_methods[label] if 0 <= label < len(visit_methods) else "visitChildren"
            )
            node = NativeRuleNode(label, method)
            is_leaf = num_children == 0

        if stack:
            stack[-1][0].children.append(node)
            stack[-1][1] -= 1
        elif root is None:
            root = node
        else:
            raise ValueError("Malformed native buffer: multiple root nodes")

        if not is_leaf:
            stack.append([node, num_children])

        # Close any ancestors that have received all their children.
        while stack and stack[-1][1] == 0:
            stack.pop()

    if stack:
        raise ValueError("Malformed native buffer: truncated before tree was complete")

    return root
