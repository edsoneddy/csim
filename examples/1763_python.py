file_names = [
    "a.py",
    "b.py",
]
file_contents = [
    "def f(x):\n    if x:\n        return x\n    return 0\n",
    "def f(x):\n    if x:\n        return x\n    return 0\n",
]

from csim import Compare

similarity_index = Compare(file_names[0], file_contents[0], file_names[1], file_contents[1])
print(similarity_index)
