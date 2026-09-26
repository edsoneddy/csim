from pathlib import Path

from csim import Compare
from csim.utils import group_by_exhaustive_search, report_pairwise_similarity


def test_identical_python_3_13_code():
    """
    Tests that two identical Python 3.13 code snippets have a similarity of 1.0.
    """
    code = "x = 1\nprint(x)"
    similarity = Compare(content_a=code, content_b=code, lang="python_3_13")
    assert similarity == 1.0


def test_different_python_3_13_code():
    """
    Tests that two completely different Python 3.13 code snippets have a low
    similarity. The bound is scale-dependent: 'ratio' is max/(max+d), so a pair
    with no structure in common sits near 0.5, not near 0.
    """
    code_a = "x = 1\nprint(x)"
    code_b = "def my_func():\n    return 'hello'"
    similarity = Compare(content_a=code_a, content_b=code_b, lang="python_3_13")
    assert similarity is not None
    assert similarity <= 0.5

    legacy = Compare(
        content_a=code_a, content_b=code_b, lang="python_3_13", index_formula="legacy"
    )
    assert legacy < 0.5


def test_structurally_similar_python_3_13_code():
    """
    Tests that two structurally identical Python 3.13 snippets (with different variable names)
    have a high similarity.
    """
    code_a = "for i in range(10):\n    print(i)"
    code_b = "for item in range(10):\n    print(item)"
    similarity = Compare(content_a=code_a, content_b=code_b, lang="python_3_13")
    assert similarity is not None
    assert similarity > 0.9


def test_java_20_identical_code():
    """
    Tests that two identical Java 20 code snippets have a similarity of 1.0.
    """
    code = 'public class Main { public static void main(String[] args) { System.out.println("Hello"); } }'
    similarity = Compare(content_a=code, content_b=code, lang="java_20")
    assert similarity == 1.0


def test_cpp_14_identical_code():
    """
    Tests that two identical C++14 code snippets have a similarity of 1.0.
    """
    code = '#include <iostream>\nint main() { std::cout << "Hello"; return 0; }'
    similarity = Compare(content_a=code, content_b=code, lang="cpp_14")
    assert similarity == 1.0


def test_apted_algorithm():
    """
    Tests that the comparison runs successfully with the 'apted' algorithm.
    """
    code_a = "a = 1"
    code_b = "b = 2"
    similarity = Compare(
        content_a=code_a, content_b=code_b, lang="python_3_13", ted_algorithm="apted"
    )
    assert similarity is not None


def test_index_formulas():
    """
    Tests the three similarity index formulas against their definitions, and
    that an unknown one is rejected.
    """
    import pytest

    from csim import INDEX_FORMULAS, SimilarityIndex

    assert INDEX_FORMULAS == ("ratio", "metric", "legacy")

    # d = 0 means identical trees on every scale.
    for formula in INDEX_FORMULAS:
        assert SimilarityIndex(0, 10, 10, index_formula=formula) == 1.0

    # max = 20, total = 30, d = 5
    assert SimilarityIndex(5, 10, 20, index_formula="ratio") == round(20 / 25, 2)
    assert SimilarityIndex(5, 10, 20, index_formula="metric") == round(25 / 35, 2)
    assert SimilarityIndex(5, 10, 20, index_formula="legacy") == round(1 - 5 / 20, 2)

    # 'legacy' is the default of csim <= 3.4.2; 'ratio' is the default now.
    assert SimilarityIndex(5, 10, 20) == SimilarityIndex(
        5, 10, 20, index_formula="ratio"
    )

    # Threshold translation between the two scales of the max family.
    assert SimilarityIndex(6, 10, 20, index_formula="legacy") == 0.70
    assert SimilarityIndex(6, 10, 20, index_formula="ratio") == round(1 / (2 - 0.70), 2)

    # 'legacy' needs a fallback denominator once d passes max, 'ratio' does not.
    assert SimilarityIndex(25, 10, 20, index_formula="legacy") == round(1 - 25 / 30, 2)
    assert 0.0 < SimilarityIndex(25, 10, 20, index_formula="ratio") < 0.5

    with pytest.raises(ValueError):
        SimilarityIndex(1, 10, 10, index_formula="nope")


def test_report_pairwise_similarity(tmp_path: Path):
    """
    Tests that the reusable report helper generates pairwise output for a language.
    """
    file_a = tmp_path / "sample_a.java"
    file_b = tmp_path / "sample_b.java"

    code = 'public class Main { public static void main(String[] args) { System.out.println("Hello"); } }'
    file_a.write_text(code)
    file_b.write_text(code)

    result = report_pairwise_similarity(
        [str(file_a), str(file_b)],
        [file_a.read_text(), file_b.read_text()],
        lang="java_20",
        ted_algorithm="zss",
    )

    assert result
    assert "similarity index" in result
    assert str(file_a) in result
    assert str(file_b) in result


def test_group_by_exhaustive_search(tmp_path: Path):
    """
    Tests that exhaustive grouping builds a transitive cluster.
    """
    samples = {
        "a.py": "def f(x):\n    if x:\n        return x\n    return 0\n",
        "b.py": "def f(y):\n    if y:\n        return y\n    return 0\n",
        "c.py": "def f(x):\n    while x:\n        return x\n    return 0\n",
        "d.py": "def f(x):\n    for _ in range(1):\n        return x\n    return 0\n",
    }

    file_names = []
    file_contents = []
    for file_name, content in samples.items():
        file_path = tmp_path / file_name
        file_path.write_text(content)
        file_names.append(str(file_path))
        file_contents.append(content)

    result = group_by_exhaustive_search(
        file_names,
        file_contents,
        lang="python_3_13",
        threshold=0.67,
        ted_algorithm="zss",
    )

    assert "Group 1" in result
    assert "a.py" in result
    assert "b.py" in result
    assert "c.py" in result
    assert "d.py" in result
