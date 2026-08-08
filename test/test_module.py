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
    Tests that two completely different Python 3.13 code snippets have a low similarity.
    """
    code_a = "x = 1\nprint(x)"
    code_b = "def my_func():\n    return 'hello'"
    similarity = Compare(content_a=code_a, content_b=code_b, lang="python_3_13")
    assert similarity is not None
    assert similarity < 0.5


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
