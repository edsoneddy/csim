# Changelog

Notable releases. Earlier entries were reconstructed from the commit history,
so they summarise each line rather than list every change.

## [4.0.0]

### Selectable similarity index, with a new default (**breaking**)

`SimilarityIndex` was `1 - d / max(n1, n2)`, with a fallback to
`1 - d / (n1 + n2)` whenever `d` passed the bound `max(n1, n2)` does not
actually impose. The formula is now selectable with `--index` / `-ix` on the
CLI and `index_formula=` on `Compare`, `report_pairwise_similarity`,
`group_by_exhaustive_search` and `SimilarityIndex`:

| Value | Formula |
|---|---|
| `ratio` (new default) | `max / (max + d)` |
| `metric` | `(n1 + n2 - d) / (n1 + n2 + d)` |
| `legacy` | `1 - d / max`, the index of csim <= 3.4.2 |

This is language-independent: it changes only the normalization step, not any
grammar, normalization or pruning configuration.

**Every score changes.** Consumers that do not pass `index_formula` get the
new scale, so pinned thresholds must be re-derived. `ratio` is a *monotone
rescaling* of `legacy` -- both rank pairs identically, and their ROC/AUC are
the same to the last digit on all six scsc datasets -- so a `legacy` threshold
translates exactly as `t_ratio = 1 / (2 - t_legacy)`: 0.70 -> 0.769,
0.80 -> 0.833, 0.90 -> 0.909. Note also that `ratio` does not reach 0 in
practice: a pair with nothing in common sits near 0.5.

**Why change the default.** `legacy`'s denominator does not bound `d`, so its
scale has a discontinuity where it swaps denominators (measured: that branch
fires once in 6642 real pairs). `ratio` removes it, stays in (0, 1] by
construction, and places a fixed cut of 0.70 at a usable operating point: on
the scsc datasets, macro F1 at 0.70 goes 0.847 -> 0.867, dataset F goes 0.686
-> 0.824, and the controlled clone set goes from 34/36 to 36/36 above 0.70,
with cross-problem false similarity still 0/750.

To be explicit about what this is: since `ratio` and `legacy` rank pairs
identically, those gains are **recalibration, not better discrimination**. The
threshold-free AUC is unchanged. `metric` is the one option that ranks
differently (it normalizes by total size); it is included because it is a
published metric normalization of tree edit distance and makes the ablation
citable.

## [3.4.2]

### Weighted hashes for `python_3` (partial credit inside hashed subtrees)

A hashed node used to cost 1 whatever it replaced, and two hashed nodes of the
same rule with different content cost a flat 0.5. Now, for `python_3` only, a
hashed node keeps the *mass* of the subtree it replaced (`(size + 1) ** 0.6`,
`HASH_MASS_ALPHA` in `python_3/utils.py`) and the multiset of labels it
covered. Insert/delete cost the weight, and a substitution between two hashed
nodes of the same rule costs `weight * (1 - overlap)` (never below 0.5), so a
statement that changed by one call is charged a fraction of a statement that
was replaced entirely. Tree size, and so edit-distance time, is unchanged.

* Fidelity (mean |error| of the index vs. the near-raw tree, 3 sets of 12
  `all_py` problems, seeds 7/11 used to choose, 23 held out): 0.087 / 0.098 /
  0.098 -> 0.052 / 0.061 / 0.054, bias ~0.
* No new false similarity: 0/250 cross-problem pairs >= 0.7 per set (as before).
* Dataset F (Faidhi ladder, 90 related + 60 unrelated pairs): AUC at L6 goes
  0.916 -> 0.950; recall at threshold 0.70 is essentially unchanged
  (L4 14/18, L5 16 -> 15/27, L6 9/36). See `docs/pruning_fidelity.md`.
* `jv-umsa-dataset/controlled`: 35 -> 34 of 36 pairs >= 0.7 (one pair moved
  0.70 -> 0.67).
* `PruneAndHash` now returns the tree *mass* as its second value for weighted
  languages (what `SimilarityIndex` needs); `count_nodes` and `csim tree` still
  report real node counts. `--talg zss` supports the weights too.
* Other languages, `python_3_13` included, are unchanged.

## [3.4.1]

### New: `csim.count_nodes`

`count_nodes(file_name, file_content, lang)` returns `(nodes_before, nodes_after)`: the size
of the raw ANTLR parse tree and of the normalized, pruned and hashed tree that is given to
the tree edit distance (the number `csim tree` prints as "Total nodes after pruning"). It
works for every language, with the native and the pure-Python parsers. No other change since
3.4.0.

## [3.4.0]

### Less aggressive pruning for `python_3` and `python_3_13`

Compound statements (`if`/`while`/`for`/`with`/`def`/`class`) are no longer
hashed, and `try/except/finally`, `elif`/`else` (and `raise`/`assert`/
`with_item` in `python_3_13`) are no longer excluded. Previously a program
that was a single loop became one node (median compression ~30x). Measured on
3 disjoint sets of 12 real `all_py` problems, the mean error of the similarity
index vs. the unpruned tree drops from ~0.14-0.18 to ~0.08-0.09 at ~6-7x
compression. Method and numbers: `docs/pruning_fidelity.md`.

### Same policy for Java 20/24, C++14, C and Kotlin

Only expression/declaration "islands" are hashed now (new optional
`STRUCTURAL_RULE_INDICES` in each language's `utils.py`: a hashed rule that
contains control flow, e.g. a lambda with a block body, is not collapsed).
Previously Java 20 collapsed 93% of real files to a single node, java_24 and
cpp_14 to a median of 8 and 3 nodes, and those configs scored 34-40% of
*unrelated* submission pairs as >= 0.7 similar (0% on the unpruned tree). Now:
mean index error vs. the unpruned tree 0.06-0.12 at 5.5-9.5x compression and
0-0.2% false similarity. Assignments, `if`/`for`/`switch`/`throw`/`catch`,
declarations and types are no longer dropped wholesale. New: `for`/`while`
equivalence (`LOOP`) in every language; `x op= y` == `x = x op y` in every
language (also on the native path); modifier rules excluded in java_24;
built-in type keywords excluded in C/C++. Full table: `docs/pruning_fidelity.md`.
`csim tree` now prints readable names for synthetic ids (`if_stmt`, ...).

### Fixed: augmented assignment normalization (`x += y` vs `x = x + y`)

The rewrite in `python_3_13` built a tree of a different shape than the
naturally-parsed `x = x + y` (one child instead of two, and the reused target
kept the target rule instead of the expression rule), so the two never hashed
equal. It now re-emits the target as its right-hand-side twin (`atom`, or the
`primary` chain for `a[i]` / `self.x`) and adds the `star_targets` child.
`python_3` had no rewrite at all; it now gets the same one (done in `visit()`,
so the native parser path sees it too). Covered for all 13 operators plus
subscript/attribute targets in regression tests.

### Fixed: `python_3` lexer crash on trailing whitespace at EOF

`Python3LexerBase.HandleSpaces` called `chr(-1)` when a file ended in spaces
(`ValueError: chr() arg not in range`), making `Compare` return `None`. Fixed in
the Python lexer base and in `grammars/Python3LexerBase.cpp` (the C++ change
needs a native rebuild to take effect).

### Restored: `for` / `while` equivalence (as in 2.0.0)

Both loop kinds share the `LOOP` label again (`CONTROL_EQUIVALENCE_RULE_INDICES`),
and the loop variable / `for`/`while`/`in` keywords no longer add a node. On
the hand-made clone set (`jv-umsa-dataset/controlled`, 36 all-vs-all pairs, all clones)
36 -> 35 (`python_3`) and 34 (`python_3_13`) pairs score >= 0.7, 2.0.0: 34.
`python_3` also drops the `def`/`class` keywords and hashes `def_parameters`,
as `python_3_13` already did. Trade-off: `for` vs `while` no longer costs a
full mismatch.

## [3.3.0]

### New language: C (experimental, grammars-v4/c)

Added C as a fully new language to csim (ISO C23 grammar + GNU/MSVC
extensions), the same shape of addition as Kotlin above: a pure-Python
parser (`csim/c/`), a native C++ parser backed by a real symbol-table
implementation for typedef disambiguation, and the full
Normalize/PruneAndHash pipeline (`csim/c/utils.py`).

**Performance** (single cold pass, one process, 70-file synthetic
judge-style corpus, plus a 25-file adversarial real-world sample from
grammars-v4's own c-testsuite -- no C corpus in `jv_dataset` to use directly):

| Corpus | Pure Python | Native C++ | Speedup |
|---|---|---|---|
| Synthetic (70 files) | 3.958 ms/file | 0.539 ms/file | ~7.3x |
| c-testsuite sample (25 files) | 9.565 ms/file | 1.650 ms/file | ~5.8x |

**Correctness**: 32/32 grammars-v4 example files and 70/70 synthetic corpus
files parse clean; 22/25 on the adversarial c-testsuite sample (the 3
failures are macro-token-pasting tricks and a GNU array-range initializer
outside this grammar's coverage -- see below). Native and pure-Python
parsers verified byte-identical at every pipeline stage via
`test/test_native_parsers.py`.

**Two upstream issues patched before shipping** (found during the earlier
spike, see project history):
1. The vendored `CLexerBase`/`CParserBase` (both C++ and Python target)
   defaulted to shelling out to a real `gcc`/invoking `subprocess` on every
   parse, and the **Python** target read `sys.argv` directly to decide this
   -- inside csim, `sys.argv` holds csim's own CLI arguments, not anything
   related to C preprocessing. Patched to default to `--nopp` (skip
   preprocessing) and to read an explicit, csim-controlled args list
   instead of `sys.argv`. A production container can't assume gcc/clang is
   on PATH, and judge submissions have no consistent include paths anyway.
2. Both targets unconditionally wrote the source text to a `<name>.p` file
   on disk on every single parse call, even in the (now-default) pass-through
   case. Removed -- wasted I/O per file and a race condition under
   concurrent use, for a debug artifact csim has no use for.

**Known limitations**: with preprocessing disabled, `#include`/`#define`/
etc. lines are swallowed as hidden tokens rather than expanded (the grammar
has a generic `Directive` rule for this), which means macro-dependent code
(token-pasting tricks, macros used for control flow) can fail to parse or
parse differently than a real compiler would see it. Real judge submissions
essentially never rely on that. Like Kotlin, there is no real-world C corpus
in this project's benchmark set to tune `csim/c/utils.py`'s normalization
rules against yet -- treat `group`/`report` results as a reasonable starting
point, not a tuned config.

**Usage**:
- `--lang c` for `report`/`group`/`tree`
- `csim info` reports native parser availability
- `CSIM_DISABLE_NATIVE=1` forces the pure-Python parser

---

### Fix: wrong terminal text in `csim tree --show-raw` for all native languages

`csim/native/loader.py`'s `_literal_names()` read the generated Lexer class's
own `literalNames` list to give native-parsed terminals their source text.
That list turned out to be populated in literal-declaration order, not
indexed by token type -- e.g. `CPP14Lexer.literalNames[CPP14Lexer.LeftParen]`
was `"'/'"`, not `"'('"` (ANTLR's own runtime indexes it the same naive way,
so this is an upstream code-generation quirk affecting every native language
already shipped: `java_20`, `java_24`, `cpp_14`, `python_3`). Discovered while
adding Kotlin, whose keywords showed up as unrelated words (`FUN` displayed
as `'super'`) under `--show-raw`.

**Did not affect correctness of `report`/`group`/similarity scoring** --
those never read terminal text, only `token.type` (see
`csim/processing/tree_processing.py`) -- only the cosmetic `--show-raw` tree
dump was wrong, which nothing in the test suite previously exercised.

Fixed by sourcing literal text from the generated `.tokens` file instead
(`'<literal>'=<type>` lines), which is correctly keyed by token type. Added
`test_native_terminal_text_matches_python_when_present` to
`test/test_native_parsers.py`, parametrized across all native languages, to
catch a regression here in the future.

### New language: Kotlin (experimental, grammars-v4/kotlin/kotlin)

Added Kotlin as a fully new language to csim -- a pure-Python parser
(`csim/kotlin/`), a native C++ parser, and the full Normalize/PruneAndHash
pipeline (`csim/kotlin/utils.py`), unlike the `java_24`/`python_3` additions
in 3.2.0 which only added a native accelerator next to an *already-existing*
pure-Python parser. No custom lexer/parser base class was needed for either
target: this grammar declares no `superClass` at all -- Kotlin's string
template interpolation is handled entirely through native ANTLR lexer modes.

**Performance** (single cold pass, one process, 70-file synthetic
judge-style corpus -- see below for why synthetic):

| Parser | Avg/file |
|---|---|
| Pure Python (ANTLR Python3 target) | 148.14 ms |
| Native C++ (ANTLR Cpp target) | 16.69 ms |

**~8.9x speedup.**

**Correctness**: native and pure-Python parsers verified byte-identical at
every pipeline stage (raw tree, `Normalize`, `PruneAndHash`, similarity
scores, `group`/`report` CLI output) via `test/test_native_parsers.py`.

**Known limitation -- untuned grouping precision:** unlike every other
language in csim, there is no real-world Kotlin corpus in this project's
benchmark set (`jv_dataset` has Java/C++/Python submissions only) to tune or
validate `csim/kotlin/utils.py`'s normalization rules against. The rules
follow the same *categories* already validated for other languages
(structural punctuation excluded, identifier text excluded, import/package
plumbing collapsed, function/class/property bodies hashed for tree-edit-
distance tractability) but have not been corpus-measured for false-positive/
false-negative rates the way `java_24`'s `SYNTHETIC_ASSIGNMENT_EXPR` fix or
`python_3`'s `relabel_node()` fixes were. Treat `group`/`report` results on
Kotlin as a reasonable starting point, not a tuned config, until a real
corpus is available to drive the next pass.

**Usage**:
- `--lang kotlin` for `report`/`group`/`tree`
- `csim info` reports native parser availability
- `CSIM_DISABLE_NATIVE=1` forces the pure-Python parser

---

## [3.2.0]

### New: Python 3 native parser (grammars-v4/python/python)

Added a native C++ parser for Python using grammars-v4's "universal Python
2/3" grammar, available alongside the existing `python_3_13` parser (nothing
about `python_3_13` was removed or changed). Unlike `java_24` below, grouping
output has been tuned to match the pure-Python parser closely, not just
parsing speed.

**Performance** (`csim group` end-to-end, real files, `jv_dataset/all_py`):

| Corpus | `python_3_13` | Native `python_3` | Speedup |
|--------|---------------|--------------------|---------|
| 67 files | 0.92s | 0.25s | 3.7x |
| 296 files | 4.10s | 2.15s | 1.9x |

Underlying parse-only speedup is 18.65x; the smaller end-to-end numbers
reflect tree-edit-distance cost, which now dominates once parsing is fast
(profiled: parsing is 91.6% of `python_3_13`'s runtime, 18% of `python_3`'s).

**Grouping correctness:** validated by comparing `csim group`'s output against
`python_3_13` pairwise, threshold 0.8, on multiple real corpora:

| Corpus | Threshold-crossing pairs | Result |
|--------|--------------------------|--------|
| `all_py/1050` (67 files, 2211 pairs) | 0 | `csim group` output byte-identical |
| `all_py/1006` (296 files) | 0 | `csim group` output byte-identical |
| `all_py/1039` (91 files) | 26 | known limitation, see below |

Three root causes were found and fixed via `csim/python_3/utils.py`'s
`relabel_node()` hook (same engine-level technique introduced for `java_24`):
import statements collapsed to a content-free marker (matching
`python_3_13`), `try`/`except`/`finally` excluded entirely (matching
`python_3_13`), and each `compound_stmt` alternative (`if`/`while`/`for`/
`with`/`class`/`def`) given its own synthetic rule id so a control-flow-kind
change costs full similarity distance instead of the partial credit a shared
rule index would give.

**Known limitation:** on files with very few top-level statements,
`python_3`'s tree can end up smaller/coarser than `python_3_13`'s for the
same source, which can slightly overstate similarity (a boilerplate match
counts for proportionally more of a smaller tree). Root cause identified but
not yet fixed — see `csim/python_3/utils.py`'s module docstring.

**Coverage:** this grammar does not parse positional-only parameters (`/`,
PEP 570), the walrus operator (`:=`, PEP 572), or `match`/`case` (PEP 634).
`csim/native/loader.py` falls back to `python_3_13` automatically for files
using those constructs, so results stay correct, just slower for that subset
(measured: ~4.2% of a large real corpus).

---

### Experimental: Java 24 native parser (grammars-v4/java/java)

Added a native C++ parser for Java using the optimized Java 24 grammar from
grammars-v4, available alongside the existing `java_20` parser (nothing about
`java_20` was removed or changed).

**Performance** (`csim group` end-to-end, 50 real files):

| Configuration | Time |
|----------------|------|
| Pure Python | 68.93s |
| Native `java_20` | 10.93s avg |
| Native `java_24` | 0.38s avg |

`java_24` is **~29x faster** than native `java_20`, and **~181x faster** than
pure Python, on this corpus.

**Known limitation — grouping correctness:** `csim/java_24/utils.py`'s
rule-normalization tables are a partial port of `java_20`'s, extended with a
`relabel_node()` engine hook (isolating assignment expressions from
`java_24`'s unified `expression` rule) that fixed *recall* -- known
near-duplicate pairs now correctly score 0.94-1.0 (were 0.5, undetected)
across all 38 verified true-positive pairs in a 50-file corpus. *Precision*
remains unfixed: on the same corpus, 532 of 570 pairs scoring above the 0.8
threshold are false positives (unrelated files sharing enough boilerplate to
look similar), because the shared-boilerplate-heavy submissions used to
verify this haven't had the broader rule-table tuning `java_20` has (~65
tuned exclusion entries, built via a dedicated corpus-tuner sweep referenced
in `java_20/utils.py`'s comments). **Do not use `java_24` for `group`/`report`
until this is fixed.**

**Usage**:
- `java_20` (existing, unchanged): use for `group`/`report` — correctness verified
- `java_24` (new, experimental): parsing/raw-tree correctness verified; grouping
  precision (false-positive rate) pending further rule-table tuning
- `python_3` (new): both parsing speed and grouping correctness verified — see above
- `csim info` reports native parser availability for all four languages
- `CSIM_DISABLE_NATIVE=1` forces pure-Python parsers for all

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
