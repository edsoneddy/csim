from csim.utils import group_by_exhaustive_search

file_names = [
    "a.py",
    "b.py",
    "c.py",
    "d.py",
]
file_contents = [
    "def f(x):\n    if x:\n        return x\n    return 0\n",
    "def f(y):\n    if y:\n        return y\n    return 0\n",
    "a = 1\nb = 2\nc = 3\n",
    "x = 1\ny = 2\nz = 3\n",
]

result = group_by_exhaustive_search(
    file_names,
    file_contents,
    lang="python",
    threshold=0.67,
    ted_algorithm="zss",
    with_output=False,
)

print(result)
