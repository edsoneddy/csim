# Changelog

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
