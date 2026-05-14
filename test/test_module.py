from csim import Compare


def test_identical_python_code():
    """
    Tests that two identical Python code snippets have a similarity of 1.0.
    """
    code = "x = 1\nprint(x)"
    similarity = Compare(content_a=code, content_b=code, lang="python")
    assert similarity == 1.0


def test_different_python_code():
    """
    Tests that two completely different Python code snippets have a low similarity.
    """
    code_a = "x = 1\nprint(x)"
    code_b = "def my_func():\n    return 'hello'"
    similarity = Compare(content_a=code_a, content_b=code_b, lang="python")
    assert similarity is not None
    assert similarity < 0.5


def test_structurally_similar_python_code():
    """
    Tests that two structurally identical Python snippets (with different variable names)
    have a high similarity.
    """
    code_a = "for i in range(10):\n    print(i)"
    code_b = "for item in range(10):\n    print(item)"
    similarity = Compare(content_a=code_a, content_b=code_b, lang="python")
    assert similarity is not None
    assert similarity > 0.9


def test_java_identical_code():
    """
    Tests that two identical Java code snippets have a similarity of 1.0.
    """
    code = 'public class Main { public static void main(String[] args) { System.out.println("Hello"); } }'
    similarity = Compare(content_a=code, content_b=code, lang="java")
    assert similarity == 1.0


def test_cpp_identical_code():
    """
    Tests that two identical C++ code snippets have a similarity of 1.0.
    """
    code = '#include <iostream>\nint main() { std::cout << "Hello"; return 0; }'
    similarity = Compare(content_a=code, content_b=code, lang="cpp")
    assert similarity == 1.0


def test_apted_algorithm():
    """
    Tests that the comparison runs successfully with the 'apted' algorithm.
    """
    code_a = "a = 1"
    code_b = "b = 2"
    similarity = Compare(
        content_a=code_a, content_b=code_b, lang="python", ted_algorithm="apted"
    )
    assert similarity is not None
