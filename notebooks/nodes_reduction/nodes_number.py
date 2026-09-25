"""
Generates prev_nodes_number.txt and post_nodes_number.txt for nodes_reduction.ipynb.

For every source file of a dataset directory it calls `csim.count_nodes`, which returns
(nodes_before, nodes_after):

* prev_nodes_number.txt -- nodes of the raw ANTLR parse tree (every rule and token node).
* post_nodes_number.txt -- nodes of the normalized, pruned and hashed tree that is handed to
  the tree edit distance (what `csim tree` prints as "Total nodes after pruning").

Usage:
    python nodes_number.py [dataset_dir] [lang]

Defaults: ../datasets/large, python_3_13. Files that fail to parse are skipped.
"""

from pathlib import Path
import sys

from csim import count_nodes
from csim.utils import get_extension_by_lang, read_file

path = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).parent / "../datasets/large")
lang = sys.argv[2] if len(sys.argv) > 2 else "python_3_13"
directory = Path(path)

if not directory.is_dir():
    raise ValueError(f"Error: {path} is not a directory")

extension = get_extension_by_lang(lang)
before, after = [], []
for p in sorted(directory.iterdir()):
    if not (p.is_file() and p.name.endswith(extension)):
        continue
    file_name, content = read_file(str(p))
    if content is None:
        continue
    try:
        b, a = count_nodes(file_name, content, lang)
    except Exception as e:
        print(f"Error {p.name}: {e}", file=sys.stderr)
        continue
    before.append(b)
    after.append(a)

out = Path(__file__).parent
(out / "prev_nodes_number.txt").write_text(str(before) + "\n")
(out / "post_nodes_number.txt").write_text(str(after) + "\n")
print(f"{len(after)} files ({lang}) -> prev_nodes_number.txt / post_nodes_number.txt")
