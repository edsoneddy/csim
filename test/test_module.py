"""
This module contains test cases for the CodeSimilarity module. 
It tests the functionality of comparing code snippets in different programming languages (Python, Java, C++) using both APTED and ZSS algorithms. 
The test cases cover various scenarios to ensure the correctness and robustness of the similarity comparison.
"""

# testing python code similarity
python_code_a = """a = 1
b = 2
print(a + b)"""
python_code_b = """x = 1
y = 2
print(x + y)"""

from csim import Compare

sim_py_apted = Compare(
    content_a=python_code_a,
    content_b=python_code_b,
    lang="python",
    ted_algorithm="apted",
)
print(f"Similarity (Python, APTED): {sim_py_apted}")

sim_py_zss = Compare(
    content_a=python_code_a, content_b=python_code_b, lang="python", ted_algorithm="zss"
)
print(f"Similarity (Python, ZSS): {sim_py_zss}")

# testing java code similarity
java_code_a = """public class Main {
    public static void main(String[] args) {
        int a = 1;
        int b = 2;
        System.out.println(a + b);
    }
}"""
java_code_b = """public class Main {
    public static void main(String[] args) {
        int x = 1;
        int y = 2;
        System.out.println(x + y);
    }
}"""
sim_java_apted = Compare(
    content_a=java_code_a, content_b=java_code_b, lang="java", ted_algorithm="apted"
)
print(f"Similarity (Java, APTED): {sim_java_apted}")
sim_java_zss = Compare(
    content_a=java_code_a, content_b=java_code_b, lang="java", ted_algorithm="zss"
)
print(f"Similarity (Java, ZSS): {sim_java_zss}")

# testing cpp code similarity
cpp_code_a = """#include <iostream>
int main() {
    int a = 1;
    int b = 2;
    std::cout << a + b;
    return 0;
}"""
cpp_code_b = """#include <iostream>
int main() {
    int x = 1;
    int y = 2;
    std::cout << x + y;
    return 0;
}"""
sim_cpp_apted = Compare(
    content_a=cpp_code_a, content_b=cpp_code_b, lang="cpp", ted_algorithm="apted"
)
print(f"Similarity (C++, APTED): {sim_cpp_apted}")
sim_cpp_zss = Compare(
    content_a=cpp_code_a, content_b=cpp_code_b, lang="cpp", ted_algorithm="zss"
)
