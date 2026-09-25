"""
Counts nodes before and after pruning for the programs picked by select_files.py.

For every file listed in results/selected_<dataset>.csv it calls `csim.count_nodes`, which returns
(nodes_before, nodes_after):

* nodes_before -- every node of the raw ANTLR parse tree (rules and tokens).
* nodes_after  -- the normalized, pruned and hashed tree handed to the tree edit distance
                  (what `csim tree` prints as "Total nodes after pruning").

Writes results/nodes_<lang>.csv (dataset,problem,file,lines,before,after).

Usage:
    python nodes_number.py [dataset_root] [lang ...]

dataset_root defaults to ../../../jv-umsa-dataset (the folder holding all_py).
With no language, both Python grammars are processed.
"""

import csv
import sys
from pathlib import Path

from csim import count_nodes

HERE = Path(__file__).parent
LANGS = {  # lang -> dataset folder (the analysis is Python-only)
    "python_3_13": "all_py",
    "python_3": "all_py",
}

root = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "../../../jv-umsa-dataset"
wanted = sys.argv[2:] or list(LANGS)

for lang in wanted:
    dataset = LANGS[lang]
    selected = HERE / "results" / f"selected_{dataset}.csv"
    if not selected.exists():
        print(f"skip {lang}: {selected.name} not found (run select_files.py first)")
        continue
    rows, skipped = [], 0
    with open(selected, newline="") as fh:
        for r in csv.DictReader(fh):
            path = root / dataset / r["problem"] / r["file"]
            try:
                before, after = count_nodes(str(path), path.read_text(encoding="utf-8"), lang)
            except Exception as e:  # a grammar may reject what another accepted
                print(f"  {lang}: {path.name}: {e}", file=sys.stderr)
                skipped += 1
                continue
            rows.append((dataset, r["problem"], r["file"], r["lines"], before, after))
    out = HERE / "results" / f"nodes_{lang}.csv"
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["dataset", "problem", "file", "lines", "before", "after"])
        w.writerows(rows)
    print(f"{lang}: {len(rows)} files ({skipped} skipped) -> {out.name}")
