# Changelog

Notable releases. Earlier entries were reconstructed from the commit history,
so they summarise each line rather than list every change.

## [Unreleased]

### Experimental: Java 24 native parser (grammars-v4/java/java)

Added a native C++ parser for Java using the optimized Java 24 grammar from
grammars-v4, available alongside the existing `java_20` parser (nothing about
`java_20` was removed or changed). Parsing itself is dramatically faster and
verified correct; **grouping/similarity output is not yet usable** — see below.

**Performance** (`csim group` end-to-end, 50 real files, 3 trials each):

| Configuration | Time |
|----------------|------|
| Pure Python | 68.17s |
| Native `java_20` | 11.43s avg |
| Native `java_24` | 0.26s avg |

`java_24` is **~44x faster** than native `java_20`, and **~262x faster** than
pure Python, on this corpus.

**Known limitation — grouping correctness:** `csim/java_24/utils.py` (the
rule-normalization tables that drive `Normalize`/`PruneAndHash`) is a rough,
untuned port of `java_20`'s tables. On real submissions it produces
significantly different — and less accurate — similarity scores than
`java_20`: on a 50-file corpus where `java_20` correctly finds 3 groups of
near-duplicate files, `java_24` finds 0. Pairwise similarity for structurally
identical files (renamed variables only) can drop from 1.0 to 0.5. **Do not
use `java_24` for `group`/`report` until this is fixed** — proper tuning
requires the same kind of dedicated sweep that produced `java_20`'s tables
(referenced in its comments as the "csim-batch-tuner sweep").

**Usage**:
- `java_20` (existing, unchanged): use for `group`/`report` — correctness verified
- `java_24` (new, experimental): parsing/raw-tree correctness verified; grouping
  correctness pending rule-table tuning
- `csim info` reports native parser availability for both
- `CSIM_DISABLE_NATIVE=1` forces pure-Python parser for both

---

## [3.1.1]

Packaging fix. No changes to csim itself.

The 3.1.0 macOS wheel went out tagged `universal2`, claiming support for both
Intel and Apple Silicon, while carrying arm64-only libraries. On an Intel Mac
pip would install it, the libraries would fail to load, and csim would fall
back to the Python parser: correct results, no speedup. The wheel is now
tagged `arm64`, and the build checks each library's architecture against the
tag before packaging.

Linux and Apple Silicon users are unaffected by the bug and by the fix.

---

## [3.1.0]

Native C++ parsers for Java and C++, giving a **6-8x speedup** on `csim group`
and `csim report`. Results are unchanged: same trees, same similarity scores,
same output.

### Why

Profiling `csim group` showed parsing accounted for 96-100% of total runtime,
almost all of it inside `adaptivePredict`/`execATN` in the Python ANTLR runtime.
Tree edit distance and normalization were negligible next to it. Parsing now
runs through ANTLR's C++ runtime, which is what that bottleneck required.

### Performance

Measured on real judge submissions (50 Java files, 49 C++ files):

| Language | Before | After | Speedup |
|----------|--------|-------|---------|
| `java_20` | 68.75s | 11.41s | 6.0x |
| `cpp_14`  | 21.83s |  2.85s | 7.7x |

Those are cold-start numbers, what a CLI run pays. A long-running process
(a web service, for example) reuses the parser's prediction cache and sees
**7.4x** for Java and **7.8x** for C++ after the first request.

Stage breakdown in steady state:

| Stage | Java before | Java after | C++ before | C++ after |
|-------|-------------|------------|------------|-----------|
| parsing | 18.77s | 2.55s | 16.85s | 1.69s |
| normalize + prune | 0.01s | 0.01s | 0.03s | 0.02s |
| tree edit distance | 0.01s | 0.02s | 0.47s | 0.47s |

Parsing is the only stage that changed, which is what the profiling predicted.

### Correctness

The native and Python parsers were compared at every stage of the pipeline:
raw parse tree, `Normalize`, `PruneAndHash`, similarity score (both `zss` and
`apted`), and the final `group`/`report` output. Output is identical.

This was also verified file by file against 99 real judge submissions,
including ones containing syntax errors: every tree matched.

### Added

- **`csim info`** — reports which parser backend is active per language.
  When a compiled parser is missing or fails to load, csim falls back to the
  Python parser silently: results stay correct but run several times slower.
  This command makes that state visible.

  ```
  $ csim info
  csim parser backends

    python_3_13    python   (no native parser for this grammar)
    java_20        native   (C++, several times faster)
    cpp_14         native   (C++, several times faster)
  ```

- **`CSIM_DISABLE_NATIVE=1`** — forces the pure-Python parsers, for debugging
  or benchmarking.

- **`scripts/build_native_parsers.sh`** — builds the native parsers from the
  grammars. Requires the ANTLR generator, the ANTLR C++ runtime, and a C++17
  compiler.

### Notes

**Python is unchanged.** `python_3_13` keeps using the Python parser. The
modern Python grammar csim uses publishes no C++ target upstream, and the
legacy `python3` grammar that does parses *slower* than the Python runtime
(78ms vs 20ms on the same input). Python was also the cheapest language to
begin with — Java and C++ were where the time went.

**Nothing breaks without the native libraries.** If no compiled parser is
present for the platform, csim uses the Python parsers and behaves exactly as
before. Install from a platform wheel to get the speedup; `csim info` confirms
which path is active.

### Packaging

- Wheels are now platform-specific (`py3-none-<platform>`). The parsers are
  loaded through `ctypes` and use no CPython API, so one wheel per platform is
  correct and works on any Python 3.
- The source distribution carries the grammars and build scripts needed to
  rebuild the parsers, and no binaries.
- GitHub Actions builds and publishes wheels for manylinux and macOS.

### Internals

For anyone building on this:

- The C++ side emits the parse tree as a flat preorder `int32` buffer. JSON was
  tried first and turned out to cost ~90x the parse itself, erasing the gain.
- The rebuilt nodes expose the interface the existing visitors already use, so
  `Normalize`, `PruneAndHash` and the tree edit distance run unchanged.
- The ANTLR C++ runtime is linked statically, so the shipped libraries depend
  only on base system libraries.
- The `.g4` grammars remain a single source of truth for both targets;
  `scripts/transform_grammar_for_cpp.py` adapts them to C++ at build time.

---

## [3.0.0] — 2026-08-10

Explicit language versions, and normalization good enough to see through
common rewrites.

### Changed

- **Language identifiers now carry a version**: `python` → `python_3_13`,
  `java` → `java_20`, `cpp` → `cpp_14`. This is the breaking change: any call
  passing the old identifiers has to be updated. Pinning the version makes it
  clear which grammar a result came from, and leaves room for other versions
  later.
- **`apted` is now the default tree edit distance algorithm**, replacing `zss`.
  `zss` is still available via `--talg zss`.

### Added

- **`csim tree` / `csim view`** — prints the normalized and pruned tree for a
  single file: the exact tree the comparison actually runs on. `--show-raw`
  also prints the raw ANTLR parse tree, which is what you want when a
  similarity score looks wrong and you need to see why.
- **Assignment operator normalization** — `x += 1` and `x = x + 1` now compare
  as equivalent, so rewriting compound assignments no longer hides a copy.
- Per-language exclusion and hashing rules for all three languages, tuning
  which tokens and rules carry weight in the comparison.

### Fixed

- C++14 parser predicates used `this.` (valid for other ANTLR targets) instead
  of `self.`, which broke on the Python target.

---

## [2.0.0] — 2026-07-11

Multi-language support. csim went from a Python-only tool to handling three
languages.

### Added

- **Java 20 and C++14 support**, alongside Python. Grammars, generated
  parsers, and per-language normalization rules for each.
- **Test suite** — CLI and module tests, plus sample files per language.
- **Continuous integration** via GitHub Actions.
- `GETTING_STARTED.md` and strategy documentation.

### Changed

- Restructured into modules: `csim/language/` for parsing, `csim/processing/`
  for tree processing and distance metrics, and one package per language. The
  language-agnostic pipeline dates from here.

---

## 1.x — 2025-12-24 to 2026-03-11

The Python-only line, where the core comparison method took shape. First
release was **1.1.0**; there was no 1.0.0.

Notable steps:

- **1.1.0** — initial release: parse trees and tree edit distance over Python
  source.
- **1.3.0** — structural hashing to collapse equivalent subtrees.
- **1.4.0 / 1.4.1** — `PruneAndHash`: pruning the tree before comparison,
  which is what made larger files practical.
- **1.5.2** — control-flow equivalence, so a `for` and an equivalent `while`
  no longer count as unrelated.
- **1.6.0** — file grouping, built on Union-Find, together with the
  `--threshold` option. Before this, csim only reported pairwise similarity.
- **1.7.0** — APTED as an alternative tree edit distance algorithm.
