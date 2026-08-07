# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`csim` (Code Similarity) is a Python CLI/library that detects structural similarity between source code files (Python, Java, C++) to support plagiarism detection. It parses source into ANTLR parse trees, normalizes/prunes them, and computes a similarity index via tree edit distance (zss or apted).

## Commands

Install in editable mode with dependencies:
```sh
pip install -e .
pip install -r requirements.txt
```

Run the test suite (from repo root, since tests reference `test/files/` by relative path):
```sh
pytest
```

Run a single test file or test:
```sh
pytest test/test_module.py
pytest test/test_module.py::test_identical_python_code
```

Run the CLI locally:
```sh
csim report --path <dir> --lang python --talg zss
csim group --path <dir> --threshold 0.8 --lang python
csim tree --path <file> --lang python [--show-raw]   # debug: print the normalized/pruned tree for one file
python -m csim report --path <dir>   # equivalent, if not installed as a script
```

Build distributables (version is hardcoded in `setup.py`, bump it manually):
```sh
python setup.py sdist bdist_wheel
```

## Architecture

### Pipeline (the core flow, used by both `Compare()` and the CLI/`utils.py` batch functions)

1. **Parse** — `csim/language/parser.py: ANTLR_parse(file_name, content, lang)` builds an ANTLR parse tree using the generated lexer/parser for the language (`csim/python`, `csim/java`, `csim/cpp` — these are ANTLR-generated files, do not hand-edit; regenerate per `grammars/parser_gen_guide.md` from the `.g4` grammars in `grammars/`).
2. **Normalize** — `csim/processing/tree_processing.py: Normalize(tree, lang)` walks the ANTLR tree with a language-specific visitor (`csim/Visitors.py`) and converts it into a simple `{"label": ..., "children": [...]}` dict tree, dropping tokens/rules that don't affect semantics (whitespace, punctuation, variable names) and collapsing single-child chains.
3. **Prune and hash** — `csim/processing/tree_processing.py: PruneAndHash(tree, lang)` further trims subtrees (e.g. excluded children per rule) and hashes certain subtrees (e.g. `assignment`, `primary`, `args`) into single leaf nodes so structurally-equivalent-but-differently-shaped code collapses to the same node. Returns `(pruned_tree, node_count)`.
4. **Tree edit distance** — `csim/processing/distance_metrics.py: TreeEditDistance(N1, N2, ted_algorithm)` computes edit distance between two normalized/hashed trees using either `zss` or `apted`, each wired up via a small adapter `Config` class since both libraries expect a `get_children`/`get_label` interface over arbitrary node objects.
5. **Similarity index** — `SimilarityIndex(d, T1, T2)` normalizes edit distance into a `[0, 1]` score (`1 - d / max(T1, T2)`, with a fallback normalization by `T1 + T2` when `d` exceeds `max(T1, T2)`).

`csim/CodeSimilarity.py: Compare(...)` runs this whole pipeline for a single pair of snippets and is the main library entrypoint (also re-exported from `csim/__init__.py`).

### Per-language configuration (`csim/<lang>/utils.py`)

Each supported language (`python`, `java`, `cpp`) has its own `utils.py` defining the sets/dicts that drive normalization — this is where language-specific tuning happens, not in the shared pipeline code:
- `EXCLUDED_TOKEN_TYPES` — lexer tokens dropped entirely (punctuation, keywords already implied by grammar structure, identifiers like `NAME`).
- `EXCLUDED_RULE_TYPES` — parser rules skipped during traversal.
- `EXCLUDE_CHILDRENS_FROM_RULE` — per-rule list of child labels to drop during pruning (e.g. drop the loop variable name in a `for` statement so `for i in ...` and `for x in ...` compare equal).
- `COLLAPSED_RULE_INDICES` — rules collapsed to a bare leaf node with no children (used in `Visitors.py`'s overridden `visit`), e.g. import statements, list/tuple/dict/set literals — their exact contents don't matter for structural comparison.
- `HASHED_RULE_INDICES` — rules whose entire subtree gets hashed to one opaque node in `PruneAndHash` rather than compared structurally.
- `CONTROL_EQUIVALENCE_RULE_INDICES` — rules treated as interchangeable for control flow (e.g. Python's `for` and `while` both map to `"LOOP"`), so a `for`-based and `while`-based solution to the same problem score as similar.
- Python additionally has `ASIGN_OP_NORMALIZED` / `RULE_ASSIGNMENT`, used by `PythonParserVisitorExtended.visitAssignment` in `csim/Visitors.py` to rewrite augmented assignment (`x += 1`) into the equivalent expanded form (`x = x + 1`) before comparison.

Dispatch to the right language's config lives in `csim/utils.py` (`get_excluded_token_types`, `get_hash_rule_indices`, etc.) — each is an if/elif over `lang` that lazily imports from the matching `csim/<lang>/utils.py` to avoid circular imports at module load time.

When adding/adjusting normalization behavior for a language, edit the corresponding `csim/<lang>/utils.py` set/dict — the shared pipeline in `tree_processing.py` and `Visitors.py` should not need language-specific branches beyond what already exists.

### Batch operations (`csim/utils.py`)

- `process_files(path, lang)` — reads all files in a directory matching the language's extension.
- `report_pairwise_similarity(...)` — computes an all-pairs similarity matrix, returns a printable report.
- `group_by_exhaustive_search(...)` — all-pairs comparison (O(n²)) that unions files above `threshold` using `UFDS` (union-find, `csim/DataStructures.py`) into transitive similarity clusters, then formats output via `get_output_by_group`. This is currently the only grouping strategy (`--strategy` accepts only `exhaustive`, kept as a CLI option for forward compatibility).

### CLI (`csim/main.py`)

`argparse`-based entrypoint (`csim=csim.main:main` console script) with three actions:
- `report` / `group` — share `--path/-p` (a directory), `--lang/-l` (`python`/`java`/`cpp`), `--talg/-ta` (`zss`/`apted`); `group` additionally requires `--threshold/-t` and accepts `--strategy/-s`.
- `tree` (alias `view`) — debugging command that prints the exact tree passed to the tree edit distance algorithm for a single file. Takes `--path/-p` (a *file*, not a directory) and `--lang/-l`; runs `ANTLR_parse` → `Normalize` → `PruneAndHash` and prints the result via `print_tree(..., lang=...)` (in `csim/utils.py`), which resolves rule indices/token types back to readable names via `get_rule_names`/`get_symbolic_names`/`format_label`. Pass `--show-raw` to also print the untouched ANTLR parse tree first (via `print_antlr_tree`), for comparing pre/post normalization side by side. Useful when tuning the per-language `EXCLUDE_CHILDRENS_FROM_RULE`/`COLLAPSED_RULE_INDICES`/`HASHED_RULE_INDICES` config described above.

### Generated parser/lexer code

`csim/python`, `csim/java`, `csim/cpp` contain ANTLR-generated lexer/parser/visitor files (from the grammars in `grammars/*.g4`) plus a hand-written `utils.py` per language for normalization config. Do not hand-edit the generated `*Lexer.py`/`*Parser.py`/`*ParserVisitor.py`/`.interp`/`.tokens` files — regenerate them from the grammar per `grammars/parser_gen_guide.md` (requires ANTLR 4.13.2 locally; not needed for normal development since generated files are checked in).
