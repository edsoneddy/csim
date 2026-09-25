"""
Builds RESULTS.md from the data the notebooks work with:

* nodes_reduction/results/nodes_<lang>.csv  (written by nodes_reduction/nodes_number.py)
* the homework dataset used by homeworks/main_all.ipynb and main_groups.ipynb

Run from the repository root or from this folder (csim must be importable):
    python build_results.py
"""

import csv
import statistics as st
from pathlib import Path

from csim.utils import (
    get_similarity_coefficient,
    group_by_exhaustive_search,
    preprocess_code,
    read_file,
)

HERE = Path(__file__).parent
RESULTS = HERE / "nodes_reduction" / "results"
HOMEWORK = HERE / "datasets" / "INF-111-JT-Tarea 1-6876"
LANGS = ("python_3_13", "python_3")
THRESHOLD = 0.6


def pct(values, q):
    values = sorted(values)
    return values[min(len(values) - 1, round(q / 100 * (len(values) - 1)))]


def nodes_section():
    selected = list(csv.DictReader(open(RESULTS / "selected_all_py.csv")))
    lines = [
        "## Node reduction (Python)",
        "",
        f"Sample: **{len(selected)} programs** from `all_py` ({len({r['problem'] for r in selected})} problems pooled), "
        "duplicate-free (same raw ANTLR tree shape counted once), without syntax errors in either grammar, "
        "trivial programs and size outliers removed. *Before* = nodes of the raw ANTLR tree; *after* = nodes of the "
        "normalized, pruned and hashed tree given to the tree edit distance.",
        "",
        "| Grammar | Programs | Before (mean / median / p90 / max) | After (mean / median / p90 / max) | Mean reduction | Median per-program ratio | Left with 1 node |",
        "|---|---|---|---|---|---|---|",
    ]
    for lang in LANGS:
        rows = list(csv.DictReader(open(RESULTS / f"nodes_{lang}.csv")))
        b = [int(r["before"]) for r in rows]
        a = [int(r["after"]) for r in rows]
        lines.append(
            f"| `{lang}` | {len(rows)} | {st.mean(b):.0f} / {st.median(b):.0f} / {pct(b, 90)} / {max(b)} "
            f"| {st.mean(a):.1f} / {st.median(a):.0f} / {pct(a, 90)} / {max(a)} "
            f"| {(1 - st.mean(a) / st.mean(b)) * 100:.1f}% (x{st.mean(b) / st.mean(a):.1f}) "
            f"| x{st.median([x / y for x, y in zip(b, a)]):.1f} | {sum(v <= 1 for v in a)} |"
        )
    lines += [
        "",
        "Figures (from `nodes_reduction/nodes_reduction.ipynb`): "
        "`nodes_reduction/results/nodes_reduction_python_3_13.png`, "
        "`nodes_reduction_python_3.png`, `nodes_survival_python.png`.",
        "",
        "![python_3_13](nodes_reduction/results/nodes_reduction_python_3_13.png)",
        "",
        "![python_3](nodes_reduction/results/nodes_reduction_python_3.png)",
        "",
        "![survival](nodes_reduction/results/nodes_survival_python.png)",
        "",
    ]
    return lines


def read_homework():
    """Every .py under the homework folder (one sub-folder per student), like the notebooks do."""
    names, contents = [], []
    for path in sorted(HOMEWORK.rglob("*.py")):
        name, content = read_file(str(path))
        if content is not None:
            names.append(name)
            contents.append(content)
    return names, contents


def homework_section():
    names, contents = read_homework()
    processed = [preprocess_code(n, c, "python_3_13") for n, c in zip(names, contents)]
    sims = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            sims.append(get_similarity_coefficient(processed[i], processed[j], "apted"))
    groups, avgs, uniques, _ = group_by_exhaustive_search(
        names, contents, "python_3_13", THRESHOLD, "apted", printable_output=False
    )
    lines = [
        "## Homework similarity (`homeworks/main_all.ipynb`, `main_groups.ipynb`)",
        "",
        f"Dataset `{HOMEWORK.name}` with `python_3_13` and APTED: **{len(names)} files**, **{len(sims)} pairs**.",
        "",
        "| Statistic | Value |",
        "|---|---|",
        f"| Mean similarity | {st.mean(sims):.3f} |",
        f"| Median similarity | {st.median(sims):.2f} |",
        f"| p90 / max | {pct(sims, 90):.2f} / {max(sims):.2f} |",
        f"| Pairs above {THRESHOLD} | {sum(s > THRESHOLD for s in sims)} ({sum(s > THRESHOLD for s in sims) / len(sims) * 100:.1f}%) |",
        f"| Pairs above 0.8 | {sum(s > 0.8 for s in sims)} |",
        "",
        f"Grouping at threshold {THRESHOLD} (union-find): **{len(groups)} group(s)** with more than one file, "
        f"{len(uniques)} unique files.",
        "",
    ]
    if groups:
        lines += ["| Group | Files | Average similarity |", "|---|---|---|"]
        for k, (g, avg) in enumerate(zip(groups, avgs), 1):
            lines.append(f"| {k} | {len(g)} | {avg:.2f} |")
        lines += [
            "",
            "Groups are built with union-find, so similarity can chain: a group's average (each member against its "
            "first file) may fall below the threshold.",
            "",
        ]
    return lines


if __name__ == "__main__":
    out = ["# Notebook results", "", "Generated by `build_results.py`; do not edit by hand.", ""]
    out += nodes_section() + homework_section()
    (HERE / "RESULTS.md").write_text("\n".join(out))
    print("RESULTS.md written")
