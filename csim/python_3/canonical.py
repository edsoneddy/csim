"""Canonical forms for equivalent Python 3 constructs (python_3 only).

Runs on the normalized tree (dicts with "label" and "children"), after identifiers,
punctuation and the `and`/`or` tokens have been dropped and before pruning and
hashing, so two programs that write the same thing in an equivalent way end up with
the same tree and the same hashes. Every rule works on the shape of the tree and on
token types only: native terminals carry no text, so nothing here can compare two
identifiers, and sort keys are built from labels alone.

Rules (applied bottom-up):

* comparison orientation: ``a > b`` -> ``b < a`` and ``a >= b`` -> ``b <= a``;
  ``a == b`` / ``a != b`` get their operands in a fixed order (``<>`` is ``!=``);
* negation: ``not (a < b)`` -> ``a >= b`` (and the other comparison pairs,
  ``in``/``not in``, ``is``/``is not``), ``not not x`` -> ``x``, and De Morgan,
  ``not (a and b)`` -> ``(not a) or (not b)`` -- `and`/`or` are not in the tree,
  so only the shape changes;
* commutative operands: the two operands of ``and``/``or`` and of ``*``, ``+``,
  ``&``, ``|``, ``^`` are put in a fixed order;
* ``else: if ...`` -> ``elif ...``.

Chained comparisons (``a < b < c``) are left alone: their operators are not
interchangeable with a swap of operands.
"""
from .Python3Lexer import Python3Lexer as L
from .Python3Parser import Python3Parser as P
from ..utils import TOKEN_TYPE_OFFSET
from .utils import SYNTHETIC_IF_STMT

_T = TOKEN_TYPE_OFFSET
LESS, GREATER = L.LESS_THAN + _T, L.GREATER_THAN + _T
LESS_EQ, GREATER_EQ = L.LT_EQ + _T, L.GT_EQ + _T
EQ, NE1, NE2 = L.EQUALS + _T, L.NOT_EQ_1 + _T, L.NOT_EQ_2 + _T
NOT, IN, IS = L.NOT + _T, L.IN + _T, L.IS + _T
COMMUTATIVE_OPS = {L.STAR + _T, L.ADD + _T, L.AND_OP + _T, L.OR_OP + _T, L.XOR + _T}
IF_TOKEN, ELIF_TOKEN = L.IF + _T, L.ELIF + _T

# operator -> operator of the negated comparison (three-token comparisons)
NEGATED = {EQ: NE2, NE1: EQ, NE2: EQ, LESS: GREATER_EQ, GREATER_EQ: LESS, GREATER: LESS_EQ, LESS_EQ: GREATER}
ORIENTED = {GREATER: LESS, GREATER_EQ: LESS_EQ}


def _leaf(label):
    return {"label": label, "children": []}


def _is_comparison(node):
    return node["label"] == P.RULE_comparison and len(node["children"]) >= 3


def _is_not(node):
    """logical_test of the form [NOT, operand]."""
    kids = node["children"]
    return node["label"] == P.RULE_logical_test and len(kids) == 2 and kids[0]["label"] == NOT


def _is_binary_logic(node):
    """logical_test of the form [left, right] (`and`/`or`: the connective is not in the tree)."""
    kids = node["children"]
    return node["label"] == P.RULE_logical_test and len(kids) == 2 and kids[0]["label"] != NOT


class _Canonicalizer:
    def __init__(self):
        self._keys = {}

    def key(self, node):
        """Order key made of labels only (no identifiers exist in the tree)."""
        hit = self._keys.get(id(node))
        if hit is None:
            k = (str(node["label"]), tuple(self.key(c) for c in node["children"]))
            # keep the node itself in the cache so its id cannot be reused by a later node
            hit = self._keys[id(node)] = (node, k)
        return hit[1]

    def run(self, node):
        node["children"] = [self.run(c) for c in node["children"]]
        return self.rewrite(node)

    def rewrite(self, node):
        label, kids = node["label"], node["children"]
        if label == P.RULE_comparison:
            return self._comparison(node)
        if label == P.RULE_logical_test:
            return self._logical(node)
        if label == P.RULE_expr and len(kids) == 3 and kids[1]["label"] in COMMUTATIVE_OPS:
            if self.key(kids[0]) > self.key(kids[2]):
                node["children"] = [kids[2], kids[1], kids[0]]
        elif label == SYNTHETIC_IF_STMT:
            return self._elif(node)
        return node

    # -- comparisons ---------------------------------------------------------------------
    def _comparison(self, node):
        kids = node["children"]
        if len(kids) != 3 or _is_comparison(kids[0]) or _is_comparison(kids[2]):
            return node  # `a < b < c` chains and n-token operators are not touched here
        left, op, right = kids
        if op["label"] in ORIENTED:
            return {"label": node["label"], "children": [right, _leaf(ORIENTED[op["label"]]), left]}
        if op["label"] in (EQ, NE1, NE2):
            label = EQ if op["label"] == EQ else NE2
            if self.key(left) > self.key(right):
                left, right = right, left
            return {"label": node["label"], "children": [left, _leaf(label), right]}
        return node

    def _negate_comparison(self, cmp_node):
        """The comparison equivalent to `not cmp_node`, or None."""
        kids = cmp_node["children"]
        if len(kids) == 3 and kids[1]["label"] in NEGATED and not (_is_comparison(kids[0]) or _is_comparison(kids[2])):
            op = _leaf(NEGATED[kids[1]["label"]])
            return self._comparison({"label": P.RULE_comparison, "children": [kids[0], op, kids[2]]})
        if len(kids) == 3 and kids[1]["label"] == IN:  # x in y -> x not in y
            return {"label": P.RULE_comparison, "children": [kids[0], _leaf(NOT), _leaf(IN), kids[2]]}
        if len(kids) == 4 and kids[1]["label"] == NOT and kids[2]["label"] == IN:  # x not in y -> x in y
            return {"label": P.RULE_comparison, "children": [kids[0], _leaf(IN), kids[3]]}
        if len(kids) == 3 and kids[1]["label"] == IS:  # x is y -> x is not y
            return {"label": P.RULE_comparison, "children": [kids[0], _leaf(IS), _leaf(NOT), kids[2]]}
        if len(kids) == 4 and kids[1]["label"] == IS and kids[2]["label"] == NOT:  # x is not y -> x is y
            return {"label": P.RULE_comparison, "children": [kids[0], _leaf(IS), kids[3]]}
        return None

    # -- logical tests -------------------------------------------------------------------
    def _not(self, operand):
        return {"label": P.RULE_logical_test, "children": [_leaf(NOT), operand]}

    def _logical(self, node):
        kids = node["children"]
        if _is_not(node):
            operand = kids[1]
            if _is_not(operand):  # not not x -> x
                return operand["children"][1]
            if operand["label"] == P.RULE_comparison:
                negated = self._negate_comparison(operand)
                if negated is not None:
                    return negated
            if _is_binary_logic(operand):  # De Morgan: the connective is invisible, only the shape moves
                left, right = operand["children"]
                pushed = [self.rewrite(self._not(x)) for x in (left, right)]
                return self.rewrite({"label": P.RULE_logical_test, "children": pushed})
            return node
        if _is_binary_logic(node) and self.key(kids[0]) > self.key(kids[1]):
            node["children"] = [kids[1], kids[0]]
        return node

    # -- else: if -> elif ----------------------------------------------------------------
    def _elif(self, node):
        kids = node["children"]
        for i, clause in enumerate(kids):
            if clause["label"] != P.RULE_else_clause:
                continue
            parts = clause["children"]
            if len(parts) == 2 and parts[1]["label"] == SYNTHETIC_IF_STMT:
                inner = parts[1]["children"]  # [IF, condition, body..., elif_clause*, else_clause?]
                cut = next((j for j in range(1, len(inner))
                            if inner[j]["label"] in (P.RULE_elif_clause, P.RULE_else_clause)), len(inner))
                elif_clause = {"label": P.RULE_elif_clause, "children": [_leaf(ELIF_TOKEN)] + inner[1:cut]}
                node["children"] = kids[:i] + [elif_clause] + inner[cut:] + kids[i + 1:]
                return node
        return node


def canonicalize(tree):
    """Return `tree` (modified in place) with the equivalent forms above unified."""
    return _Canonicalizer().run(tree)
