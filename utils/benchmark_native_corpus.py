#!/usr/bin/env python
"""Benchmark `csim group` on a 50-file corpus: pure-Python vs native parsers.

Not a pytest test: this takes minutes on the Python baseline. Run directly.

The corpus mixes distinct algorithms with deliberate near-duplicates (renamed
identifiers, reordered members, compound-assignment rewrites), so the run
exercises the same mix of high- and low-similarity pairs a real plagiarism
sweep would, rather than 50 copies of one file.

Usage:
    python test/benchmark_native_corpus.py [--files N] [--lang java_20|cpp_14]
"""

import argparse
import hashlib
import importlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

# Run against the working tree, not whatever csim is pip-installed: running this
# file directly puts test/ on sys.path, not the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from csim.language.parser import ANTLR_parse
from csim.native import is_available, loader
from csim.processing.tree_processing import Normalize, PruneAndHash
from csim.utils import get_similarity_coefficient, group_by_exhaustive_search


# --- corpus -----------------------------------------------------------------

JAVA_ALGORITHMS = [
    # (name, body) -- each is a distinct algorithm, not a template instance.
    ("QuickSort", """
    public static void sort(int[] a, int lo, int hi) {
        if (lo < hi) {
            int p = partition(a, lo, hi);
            sort(a, lo, p - 1);
            sort(a, p + 1, hi);
        }
    }
    private static int partition(int[] a, int lo, int hi) {
        int pivot = a[hi];
        int i = lo - 1;
        for (int j = lo; j < hi; j++) {
            if (a[j] < pivot) { i++; int t = a[i]; a[i] = a[j]; a[j] = t; }
        }
        int t = a[i + 1]; a[i + 1] = a[hi]; a[hi] = t;
        return i + 1;
    }"""),
    ("MergeSort", """
    public static int[] sort(int[] a) {
        if (a.length <= 1) return a;
        int mid = a.length / 2;
        int[] left = java.util.Arrays.copyOfRange(a, 0, mid);
        int[] right = java.util.Arrays.copyOfRange(a, mid, a.length);
        return merge(sort(left), sort(right));
    }
    private static int[] merge(int[] l, int[] r) {
        int[] out = new int[l.length + r.length];
        int i = 0, j = 0, k = 0;
        while (i < l.length && j < r.length) {
            if (l[i] <= r[j]) { out[k++] = l[i++]; } else { out[k++] = r[j++]; }
        }
        while (i < l.length) out[k++] = l[i++];
        while (j < r.length) out[k++] = r[j++];
        return out;
    }"""),
    ("BinarySearch", """
    public static int find(int[] a, int target) {
        int lo = 0, hi = a.length - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid] == target) return mid;
            if (a[mid] < target) { lo = mid + 1; } else { hi = mid - 1; }
        }
        return -1;
    }"""),
    ("GraphBFS", """
    public static java.util.List<Integer> traverse(int[][] adj, int start) {
        java.util.List<Integer> order = new java.util.ArrayList<>();
        boolean[] seen = new boolean[adj.length];
        java.util.Deque<Integer> queue = new java.util.ArrayDeque<>();
        queue.add(start); seen[start] = true;
        while (!queue.isEmpty()) {
            int node = queue.poll();
            order.add(node);
            for (int next : adj[node]) {
                if (!seen[next]) { seen[next] = true; queue.add(next); }
            }
        }
        return order;
    }"""),
    ("MatrixOps", """
    public static int[][] multiply(int[][] x, int[][] y) {
        int n = x.length, m = y[0].length, k = y.length;
        int[][] out = new int[n][m];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                int acc = 0;
                for (int t = 0; t < k; t++) { acc += x[i][t] * y[t][j]; }
                out[i][j] = acc;
            }
        }
        return out;
    }"""),
    ("StringUtils", """
    public static boolean isPalindrome(String s) {
        int i = 0, j = s.length() - 1;
        while (i < j) {
            if (s.charAt(i) != s.charAt(j)) return false;
            i++; j--;
        }
        return true;
    }
    public static String reverse(String s) {
        StringBuilder sb = new StringBuilder();
        for (int i = s.length() - 1; i >= 0; i--) sb.append(s.charAt(i));
        return sb.toString();
    }"""),
    ("Fibonacci", """
    public static long compute(int n) {
        if (n <= 1) return n;
        long a = 0, b = 1;
        for (int i = 2; i <= n; i++) { long c = a + b; a = b; b = c; }
        return b;
    }"""),
    ("StackImpl", """
    private int[] data = new int[16];
    private int size = 0;
    public void push(int v) {
        if (size == data.length) data = java.util.Arrays.copyOf(data, size * 2);
        data[size++] = v;
    }
    public int pop() {
        if (size == 0) throw new IllegalStateException("empty");
        return data[--size];
    }"""),
]

CPP_ALGORITHMS = [
    ("QuickSort", """
#include <vector>
#include <utility>
class %(name)s {
public:
    static void sort(std::vector<int>& a, int lo, int hi) {
        if (lo < hi) {
            int p = partition(a, lo, hi);
            sort(a, lo, p - 1);
            sort(a, p + 1, hi);
        }
    }
private:
    static int partition(std::vector<int>& a, int lo, int hi) {
        int pivot = a[hi];
        int i = lo - 1;
        for (int j = lo; j < hi; j++) {
            if (a[j] < pivot) { i++; std::swap(a[i], a[j]); }
        }
        std::swap(a[i + 1], a[hi]);
        return i + 1;
    }
};"""),
    ("BinaryTree", """
#include <memory>
template<typename T>
class %(name)s {
    struct Node {
        T value;
        std::unique_ptr<Node> left, right;
        explicit Node(const T& v) : value(v) {}
    };
    std::unique_ptr<Node> root;
    std::unique_ptr<Node> insertAt(std::unique_ptr<Node> n, const T& v) {
        if (!n) return std::make_unique<Node>(v);
        if (v < n->value) n->left = insertAt(std::move(n->left), v);
        else n->right = insertAt(std::move(n->right), v);
        return n;
    }
public:
    void insert(const T& v) { root = insertAt(std::move(root), v); }
};"""),
    ("LinkedList", """
#include <memory>
template<typename T>
class %(name)s {
    struct Cell { T value; std::unique_ptr<Cell> next; };
    std::unique_ptr<Cell> head;
    int count = 0;
public:
    void prepend(const T& v) {
        auto cell = std::make_unique<Cell>();
        cell->value = v;
        cell->next = std::move(head);
        head = std::move(cell);
        count += 1;
    }
    int size() const { return count; }
};"""),
    ("MatrixOps", """
#include <vector>
class %(name)s {
public:
    static std::vector<std::vector<int>> multiply(
        const std::vector<std::vector<int>>& x,
        const std::vector<std::vector<int>>& y) {
        int n = x.size(), m = y[0].size(), k = y.size();
        std::vector<std::vector<int>> out(n, std::vector<int>(m, 0));
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                int acc = 0;
                for (int t = 0; t < k; t++) acc += x[i][t] * y[t][j];
                out[i][j] = acc;
            }
        }
        return out;
    }
};"""),
    ("GraphSearch", """
#include <vector>
#include <queue>
class %(name)s {
public:
    static std::vector<int> bfs(const std::vector<std::vector<int>>& adj, int start) {
        std::vector<int> order;
        std::vector<bool> seen(adj.size(), false);
        std::queue<int> q;
        q.push(start); seen[start] = true;
        while (!q.empty()) {
            int node = q.front(); q.pop();
            order.push_back(node);
            for (int next : adj[node]) {
                if (!seen[next]) { seen[next] = true; q.push(next); }
            }
        }
        return order;
    }
};"""),
    ("StringUtils", """
#include <string>
class %(name)s {
public:
    static bool isPalindrome(const std::string& s) {
        int i = 0, j = static_cast<int>(s.size()) - 1;
        while (i < j) {
            if (s[i] != s[j]) return false;
            i++; j--;
        }
        return true;
    }
    static std::string reverse(const std::string& s) {
        std::string out;
        for (int i = static_cast<int>(s.size()) - 1; i >= 0; i--) out += s[i];
        return out;
    }
};"""),
    ("Accumulator", """
#include <vector>
class %(name)s {
    long total = 0;
    int seen = 0;
public:
    void add(int v) { total += v; seen += 1; }
    void scale(int f) { total *= f; }
    void shift(int s) { total <<= s; }
    double mean() const { return seen ? static_cast<double>(total) / seen : 0.0; }
};"""),
    ("Fibonacci", """
#include <vector>
class %(name)s {
public:
    static long compute(int n) {
        if (n <= 1) return n;
        long a = 0, b = 1;
        for (int i = 2; i <= n; i++) { long c = a + b; a = b; b = c; }
        return b;
    }
};"""),
]


def _rename_identifiers(source, suffix):
    """Produce a near-duplicate: same structure, different local names."""
    for old, new in (
        (" a[", f" arr{suffix}["), ("(a,", f"(arr{suffix},"),
        (" i ", f" idx{suffix} "), (" j ", f" jdx{suffix} "),
        (" lo", f" low{suffix}"), (" hi", f" high{suffix}"),
    ):
        source = source.replace(old, new)
    return source


def build_java_corpus(count):
    """Build `count` Java files: rotating algorithms plus near-duplicate variants."""
    files = {}
    for i in range(count):
        name, body = JAVA_ALGORITHMS[i % len(JAVA_ALGORITHMS)]
        variant = i // len(JAVA_ALGORITHMS)
        class_name = f"{name}V{variant}"

        if variant % 3 == 1:
            body = _rename_identifiers(body, variant)
        elif variant % 3 == 2:
            # Same logic, compound assignment instead of explicit form.
            body = body.replace("acc = acc +", "acc +=").replace("i = i + 1", "i += 1")

        files[f"{class_name}.java"] = f"public class {class_name} {{{body}\n}}\n"
    return files


def build_cpp_corpus(count):
    """Build `count` C++ files: rotating algorithms plus near-duplicate variants."""
    files = {}
    for i in range(count):
        name, template = CPP_ALGORITHMS[i % len(CPP_ALGORITHMS)]
        variant = i // len(CPP_ALGORITHMS)
        class_name = f"{name}V{variant}"

        source = template % {"name": class_name}
        if variant % 3 == 1:
            source = _rename_identifiers(source, variant)

        files[f"{class_name}.cpp"] = source + "\n"
    return files


# --- measurement ------------------------------------------------------------

def _set_native(enabled):
    """Switch csim between the native and pure-Python parser paths."""
    if enabled:
        os.environ.pop("CSIM_DISABLE_NATIVE", None)
    else:
        os.environ["CSIM_DISABLE_NATIVE"] = "1"
    loader._handles.clear()
    importlib.reload(loader)


def measure_stages(names, contents, lang):
    """Time every pipeline stage, so the parts account for the whole."""
    parse_time = 0.0
    normalize_time = 0.0
    processed = []

    for name, content in zip(names, contents):
        start = time.perf_counter()
        tree = ANTLR_parse(name, content, lang)
        parse_time += time.perf_counter() - start

        start = time.perf_counter()
        processed.append(PruneAndHash(Normalize(tree, lang), lang))
        normalize_time += time.perf_counter() - start

    start = time.perf_counter()
    for i in range(len(processed)):
        for j in range(i + 1, len(processed)):
            get_similarity_coefficient(processed[i], processed[j], "zss")
    ted_time = time.perf_counter() - start

    return parse_time, normalize_time, ted_time


def run_one_config(lang, corpus, native):
    """Measure a single (language, parser) config in the current process.

    Both ANTLR runtimes build their prediction caches lazily, so the first parse
    in a process is markedly slower than later ones. `group` is therefore timed
    twice: cold (what a CLI invocation pays) and warm (what a long-running
    service sees). Mixing the two in one process would let whichever config ran
    first subsidise the other, which is why the driver runs each in a subprocess.
    """
    names = list(corpus)
    contents = list(corpus.values())

    _set_native(native)

    start = time.perf_counter()
    output = group_by_exhaustive_search(
        names, contents, lang=lang, threshold=0.6, ted_algorithm="zss"
    )
    cold = time.perf_counter() - start

    start = time.perf_counter()
    group_by_exhaustive_search(
        names, contents, lang=lang, threshold=0.6, ted_algorithm="zss"
    )
    warm = time.perf_counter() - start

    parse_time, normalize_time, ted_time = measure_stages(names, contents, lang)

    return {
        "cold": cold,
        "warm": warm,
        "parse": parse_time,
        "normalize": normalize_time,
        "ted": ted_time,
        "output_digest": hashlib.sha256(output.encode("utf-8")).hexdigest(),
    }


def report_language(lang, results, n, pairs, total_bytes):
    """Print the comparison table for one language."""
    print(f"\n{'=' * 74}")
    print(f"{lang}  --  {n} files, {pairs:,} pairwise comparisons")
    print(f"{'=' * 74}")
    print(f"corpus: {total_bytes:,} chars  ({total_bytes // n:,} chars/file avg)")

    py, nat = results["python"], results["native"]

    def ratio(a, b):
        return a / b if b > 0 else float("inf")

    print(f"\n  {'-' * 70}")
    print(f"  {'measurement':<22} {'python':>12} {'native':>12} {'speedup':>10}")
    print(f"  {'-' * 70}")
    print(f"  {'group (cold start)':<22} {py['cold']:>11.2f}s {nat['cold']:>11.2f}s "
          f"{ratio(py['cold'], nat['cold']):>9.1f}x")
    print(f"  {'group (warm)':<22} {py['warm']:>11.2f}s {nat['warm']:>11.2f}s "
          f"{ratio(py['warm'], nat['warm']):>9.1f}x")
    print(f"  {'-' * 70}")
    print("  steady-state breakdown:")
    for key, label in (
        ("parse", "parsing"),
        ("normalize", "normalize+prune"),
        ("ted", "TED"),
    ):
        print(f"  {'  ' + label:<22} {py[key]:>11.2f}s {nat[key]:>11.2f}s "
              f"{ratio(py[key], nat[key]):>9.1f}x")

    py_sum = py["parse"] + py["normalize"] + py["ted"]
    nat_sum = nat["parse"] + nat["normalize"] + nat["ted"]
    print(f"  {'  total':<22} {py_sum:>11.2f}s {nat_sum:>11.2f}s "
          f"{ratio(py_sum, nat_sum):>9.1f}x")
    print(f"  {'-' * 70}")

    identical = py["output_digest"] == nat["output_digest"]
    print(f"\n  output identical: {'yes' if identical else 'NO -- MISMATCH'}")
    if not identical:
        print("  *** results diverge; the speedup figures are meaningless ***")
        return None

    return {
        "lang": lang,
        "files": n,
        "pairs": pairs,
        "python_cold": py["cold"],
        "native_cold": nat["cold"],
        "python_warm": py["warm"],
        "native_warm": nat["warm"],
    }

    if verify:
        identical = py["output"] == nat["output"]
        print(f"\n  output identical: {'yes' if identical else 'NO -- MISMATCH'}")
        if not identical:
            print("  *** results diverge; speedup figures are meaningless ***")
            return None

    return {
        "lang": lang,
        "files": n,
        "pairs": pairs,
        "python_wall": py["wall"],
        "native_wall": nat["wall"],
        "python_parse": py["parse"],
        "native_parse": nat["parse"],
        "python_ted": py["ted"],
        "native_ted": nat["ted"],
    }


def load_corpus_dir(path, lang, limit=None):
    """Load a real corpus from disk (e.g. judge submissions).

    Files that cannot be read are skipped with a warning rather than aborting
    the run; a real corpus routinely contains a few unreadable submissions.
    """
    from csim.utils import get_extension_by_lang

    extension = get_extension_by_lang(lang)
    paths = sorted(p for p in Path(path).iterdir() if p.is_file() and p.suffix == extension)

    if limit:
        paths = paths[:limit]

    corpus = {}
    for file_path in paths:
        try:
            corpus[file_path.name] = file_path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print(f"  warning: skipping {file_path.name}: {exc}", file=sys.stderr)

    if not corpus:
        raise SystemExit(f"error: no {extension} files found in {path}")

    return corpus


def build_corpus(lang, count, corpus_dir=None):
    if corpus_dir:
        return load_corpus_dir(corpus_dir, lang, limit=count)
    return build_java_corpus(count) if lang == "java_20" else build_cpp_corpus(count)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--files", type=int, default=50, help="corpus size (default 50)")
    parser.add_argument(
        "--lang",
        choices=["java_20", "cpp_14", "both"],
        default="both",
        help="language to benchmark (default both)",
    )
    parser.add_argument(
        "--java-dir",
        help="directory of real .java files to use instead of the synthetic corpus",
    )
    parser.add_argument(
        "--cpp-dir",
        help="directory of real .cpp files to use instead of the synthetic corpus",
    )
    parser.add_argument(
        "--worker",
        metavar="LANG:MODE",
        help=argparse.SUPPRESS,  # internal: run one config, emit JSON
    )
    args = parser.parse_args()

    corpus_dirs = {"java_20": args.java_dir, "cpp_14": args.cpp_dir}

    # Worker mode: measure a single config in this (fresh) process and report.
    if args.worker:
        lang, mode = args.worker.split(":")
        corpus = build_corpus(lang, args.files, corpus_dirs.get(lang))
        result = run_one_config(lang, corpus, native=(mode == "native"))
        print(json.dumps(result))
        return 0

    print(f"csim native parser benchmark  --  {args.files} files per language")
    print("each configuration runs in a fresh process so cold-start timings are real")

    languages = ["java_20", "cpp_14"] if args.lang == "both" else [args.lang]
    summary = []

    for lang in languages:
        if not is_available(lang):
            print(f"\n{lang}: native parser unavailable -- skipping")
            continue

        corpus = build_corpus(lang, args.files, corpus_dirs.get(lang))
        n = len(corpus)
        total_bytes = sum(len(c) for c in corpus.values())

        worker_args = [sys.executable, __file__, "--files", str(args.files)]
        if corpus_dirs.get(lang):
            worker_args += [
                "--java-dir" if lang == "java_20" else "--cpp-dir",
                corpus_dirs[lang],
            ]

        results = {}
        for mode in ("python", "native"):
            completed = subprocess.run(
                worker_args + ["--worker", f"{lang}:{mode}"],
                capture_output=True,
                text=True,
            )
            if completed.returncode != 0:
                print(f"\n{lang}/{mode}: worker failed\n{completed.stderr}")
                return 1
            results[mode] = json.loads(completed.stdout.strip().splitlines()[-1])

        entry = report_language(
            lang, results, n, n * (n - 1) // 2, total_bytes
        )
        if entry:
            summary.append(entry)

    if len(summary) > 1:
        print(f"\n{'=' * 74}")
        print("SUMMARY")
        print(f"{'=' * 74}")
        print(f"{'language':<10} {'files':>6} {'pairs':>7} "
              f"{'cold py':>9} {'cold nat':>9} {'x':>6} "
              f"{'warm py':>9} {'warm nat':>9} {'x':>6}")
        print("-" * 74)
        for s in summary:
            print(f"{s['lang']:<10} {s['files']:>6} {s['pairs']:>7,} "
                  f"{s['python_cold']:>8.2f}s {s['native_cold']:>8.2f}s "
                  f"{s['python_cold'] / s['native_cold']:>5.1f}x "
                  f"{s['python_warm']:>8.2f}s {s['native_warm']:>8.2f}s "
                  f"{s['python_warm'] / s['native_warm']:>5.1f}x")

    return 0


if __name__ == "__main__":
    sys.exit(main())
