"""
Picks a representative, duplicate-free sample of programs from a dataset of judge
submissions, so the node-reduction analysis is not dominated by many copies of the
same solution.

Problems are pooled (e.g. 1005 and 1010 can both contribute): only node counts are
analysed, so nothing needs to be compared *within* a problem.

Selection, per problem:
  1. keep files that read as UTF-8 and parse without syntax errors (in every grammar under
     test: `lang` plus --also-check); files with syntax errors say nothing about pruning;
  2. drop duplicates -- two files are duplicates when their raw ANTLR trees have the same
     shape (same sequence of rule/token types), i.e. they differ only in identifier names,
     literals, comments or whitespace;
  3. drop trivial programs (--min-nodes) and size outliers (above Q3 + 3*IQR, e.g. an exercise
     that builds a huge array literal), then keep exactly --target files, spread over the
     problems and, inside each problem, across the size range.

Usage:
    python select_files.py <dataset_dir> <lang> <out.csv> [--target 1000] [--also-check lang ...]

`lang` only selects the parser used for the duplicate/syntax checks. Output columns:
dataset,problem,file,lines,raw_nodes
"""

import argparse
import contextlib
import csv
import hashlib
import io
import os
from pathlib import Path

# The native parser recovers from syntax errors silently; the pure-Python one reports them,
# which is what the "parses cleanly" check needs (and keeps the selection deterministic).
os.environ["CSIM_DISABLE_NATIVE"] = "1"

from antlr4.tree.Tree import TerminalNode
from csim.language.parser import ANTLR_parse


def raw_shape(tree):
    """(hash of the shape, node count) of a raw ANTLR tree; iterative (deep trees)."""
    labels = []
    stack = [tree]
    while stack:
        node = stack.pop()
        count = node.getChildCount()
        labels.append(-node.symbol.type - 2 if isinstance(node, TerminalNode) else node.getRuleIndex())
        labels.append(count)
        stack.extend(node.getChild(i) for i in range(count - 1, -1, -1))
    return hashlib.sha1(repr(labels).encode()).hexdigest(), len(labels) // 2


def analyse(path, lang, also=()):
    """(shape_hash, raw_nodes, lines) or None when the file is unusable.

    Unusable = unreadable, empty, or with a syntax error in `lang` or in any grammar of `also`.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None
    if not text.strip():
        return None
    errors = io.StringIO()
    try:
        with contextlib.redirect_stderr(errors):
            tree = ANTLR_parse(str(path), text, lang)
    except Exception:
        return None
    if errors.getvalue():
        return None
    for other in also:
        errors = io.StringIO()
        try:
            with contextlib.redirect_stderr(errors):
                ANTLR_parse(str(path), text, other)
        except Exception:
            return None
        if errors.getvalue():
            return None
    shape, nodes = raw_shape(tree)
    return shape, nodes, text.count("\n") + 1


def spread(items, k):
    """k items evenly spread over `items` (already sorted by size)."""
    if len(items) <= k:
        return items
    return [items[round(i * (len(items) - 1) / (k - 1))] for i in range(k)] if k > 1 else [items[len(items) // 2]]


def quotas(sizes, target):
    """Per-problem quota so that the total is exactly `target` (or everything, if fewer)."""
    if sum(sizes.values()) <= target:
        return dict(sizes)
    lo, hi = 0, max(sizes.values())
    while lo < hi:  # largest base such that sum(min(size, base)) <= target
        mid = (lo + hi + 1) // 2
        if sum(min(n, mid) for n in sizes.values()) <= target:
            lo = mid
        else:
            hi = mid - 1
    quota = {p: min(n, lo) for p, n in sizes.items()}
    extra = target - sum(quota.values())
    for p in sorted(sizes):  # hand the remainder to problems that still have spare files
        if extra == 0:
            break
        if sizes[p] > quota[p]:
            quota[p] += 1
            extra -= 1
    return quota


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dataset")
    ap.add_argument("lang")
    ap.add_argument("out")
    ap.add_argument("--also-check", nargs="*", default=[], help="extra grammars the file must also parse cleanly with")
    ap.add_argument("--target", type=int, default=1000, help="number of files to select (a round number)")
    ap.add_argument("--min-nodes", type=int, default=40, help="drop trivial programs below this many raw nodes")
    ap.add_argument("--fence", type=float, default=3.0, help="drop outliers above Q3 + fence * IQR of raw nodes")
    args = ap.parse_args()

    root = Path(args.dataset)
    ext = {"python_3_13": ".py", "python_3": ".py", "java_20": ".java", "java_24": ".java",
           "cpp_14": ".cpp", "c": ".c", "kotlin": ".kt"}[args.lang]

    # 1. unique, cleanly parsed programs per problem
    pool = {}
    seen_global = set()
    for problem in sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith(("_", "."))):
        unique = {}
        for f in sorted(problem.glob(f"*{ext}")):
            info = analyse(f, args.lang, args.also_check)
            if info is None:
                continue
            shape, nodes, lines = info
            if shape in unique or shape in seen_global:
                continue
            unique[shape] = (nodes, lines, f.name)
        seen_global.update(unique)
        pool[problem.name] = sorted(unique.values())
    total_unique = sum(len(v) for v in pool.values())

    # 2. drop trivial programs and size outliers (e.g. a hard-coded array of N literals)
    sizes_all = sorted(n for v in pool.values() for n, _, _ in v)
    q1, q3 = sizes_all[len(sizes_all) // 4], sizes_all[3 * len(sizes_all) // 4]
    upper = q3 + args.fence * (q3 - q1)
    pool = {p: [c for c in v if args.min_nodes <= c[0] <= upper] for p, v in pool.items()}
    pool = {p: v for p, v in pool.items() if v}
    kept = sum(len(v) for v in pool.values())

    # 3. exactly `target` files, spread over problems and over the size range
    quota = quotas({p: len(v) for p, v in pool.items()}, args.target)
    rows = []
    for problem, cands in pool.items():
        for nodes, lines, name in spread(cands, quota[problem]):
            rows.append((root.name, problem, name, lines, nodes))

    with open(args.out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["dataset", "problem", "file", "lines", "raw_nodes"])
        w.writerows(rows)
    print(f"{args.out}: {len(rows)} files from {len({r[1] for r in rows})} problems "
          f"(unique {total_unique}, after outlier filter {kept}, raw nodes {args.min_nodes}..{upper:.0f})")


if __name__ == "__main__":
    main()
