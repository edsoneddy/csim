"""Canonical forms of python_3 (csim/python_3/canonical.py): equivalent constructs get the same tree."""
import pytest

import csim.python_3.utils as py3_utils
from csim import Compare


def score(a, b):
    return Compare(content_a=a, content_b=b, lang="python_3")


def cond(test, body="    x = 1\n"):
    return f"if {test}:\n{body}"


EQUIVALENT = [
    (cond("a > b"), cond("b < a")),
    (cond("a >= b"), cond("b <= a")),
    (cond("a == b"), cond("b == a")),
    (cond("a != b"), cond("not (a == b)")),
    (cond("not a < b"), cond("a >= b")),
    (cond("x not in y"), cond("not x in y")),
    (cond("x is not None"), cond("not x is None")),
    (cond("not (a and b)"), cond("not a or not b")),
    (cond("a and b"), cond("b and a")),
    (cond("not not a"), cond("a")),
    ("x = f(a) * b\n", "x = b * f(a)\n"),
    (
        "if a:\n    x = 1\nelse:\n    if b:\n        x = 2\n    else:\n        x = 3\n",
        "if a:\n    x = 1\nelif b:\n    x = 2\nelse:\n    x = 3\n",
    ),
]

DIFFERENT = [
    (cond("a < b"), cond("a <= b")),
    (cond("not (a and b)"), cond("a and b")),
    (cond("a < b"), cond("not a < b")),
    ("x = f(a) - b\n", "x = b - f(a)\n"),
    # an else with more than the nested if is not an elif
    (
        "if a:\n    x = 1\nelse:\n    y = 0\n    if b:\n        x = 2\n",
        "if a:\n    x = 1\nelif b:\n    x = 2\n",
    ),
]


@pytest.mark.parametrize("a,b", EQUIVALENT)
def test_equivalent_forms_have_the_same_tree(a, b):
    assert score(a, b) == 1.0


@pytest.mark.parametrize("a,b", DIFFERENT)
def test_different_programs_stay_different(a, b):
    assert score(a, b) < 1.0


def test_chained_comparison_is_left_alone():
    # a < b < c is (a < b) and (b < c): swapping operands would not be an equivalence
    assert score(cond("a < b < c"), cond("a < b < c")) == 1.0


def test_canonical_forms_can_be_turned_off(monkeypatch):
    monkeypatch.setattr(py3_utils, "CANONICAL_FORMS", False)
    assert score(cond("a > b"), cond("b < a")) < 1.0
    monkeypatch.setattr(py3_utils, "CANONICAL_FORMS", True)
    assert score(cond("a > b"), cond("b < a")) == 1.0


def test_other_languages_are_unaffected():
    a = "int main() { if (a > b) { return 1; } return 0; }"
    b = "int main() { if (b < a) { return 1; } return 0; }"
    assert Compare(content_a=a, content_b=b, lang="cpp_14") < 1.0
