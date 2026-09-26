# Pruning fidelity

Pruning (exclusions, collapsing, hashing) compresses the tree for TED, but it
should not change the similarity index much. This note records how that is
measured and what was found for `python_3` and `python_3_13`.

## Method

* **Data**: real judge submissions from `jv-umsa-dataset/all_py`. Three
  disjoint sets of 12 problems (seeds 7, 11, 23), 16 files each (files with
  5-260 nodes so APTED stays tractable), all within-problem pairs: 1440 pairs
  per set.
* **Reference (R0)**: near-raw tree -- only whitespace, comments, NEWLINE/
  INDENT/DEDENT, EOF and identifier tokens dropped; no rule exclusion,
  no collapsing, no hashing. R1 is the current exclusions with no hashing.
* **Metric**: mean absolute error (MAE) of the similarity index of the pruned
  trees vs. R0, plus p90/max error, signed bias, and median node-count ratio
  (unpruned / pruned).
* Seeds 7 and 11 were used to choose the config; seed 23 was only run after.

## Finding

Hashing whole compound statements (`if`/`while`/`for`/`with`/`def`/`class`)
was the cause of the aggressive compression: a program that is one loop
became 1 node, and the median program went from ~100 nodes to 4-6.

| Config | Compression | MAE vs R0 |
|---|---|---|
| Exclusions only, no hash (R1) | 1.8x | 0.05-0.07 |
| Old: hash compound statements | 25-37x | 0.14-0.18 (max 0.87) |
| New: hash leaves only (expressions, simple statements) | ~5-6x | 0.08-0.09 (max ~0.5) |

Per-set results of the new config (cost 0.5): `python_3` 0.082 / 0.089 /
0.093; `python_3_13` 0.077 / 0.081 / 0.082 (sets 7 / 11 / 23; bias ~0).

Also tried and rejected: hashing a compound statement only when its subtree is
small (K = 6..48 nodes): error grows with K and compression gains are not
worth it; and size-weighting hashed nodes in the TED (better MAE by ~0.015
but changes SimilarityIndex/APTED costs -- not worth the complexity).

`try/except/finally`, `elif`/`else`, and (python_3_13) `raise`/`assert`/
`with_item` were previously excluded entirely; keeping them lowers the error
on both sets and stops dropping semantics.

## Edit cost 0.5 vs 1.0

`label_distance` gives 0.5 to two hashed nodes matching on rule or on hash.
Unit cost (1.0 everywhere) was measured on the same pairs: MAE is equal or
slightly worse (e.g. 0.093 -> 0.102) and the index becomes biased low
(-0.04..-0.06) because a slightly different statement costs as much as a
totally different one. 0.5 has bias ~0. Sweeping 0.25..1.0 showed a flat MAE
optimum around 0.4-0.6. Cost was left at 0.5.

## Known limitations

* Literal *values* are invisible (`x == 0` vs `x == 1` hash identically) since
  the hash covers token/rule labels, not text.
* ~4-7% of pairs still cross the 0.8 grouping threshold differently than R0
  (R1, exclusions alone, already flips ~4%).

## Interaction with the other normalizations (3.4.0)

Three normalizations sit next to the hashing change and were re-measured
together (same three problem sets, `python_3`/`python_3_13` MAE 0.075-0.098,
compression ~7x):

* **Augmented assignment** is rewritten to the tree of its expanded form, so
  it is neutral for fidelity by construction (see CHANGELOG).
* **`for` == `while`**: `test/controlled` (hand-made clones, incl. a `for` ->
  `while` rewrite and a `+=` rewrite) needs it to reach >= 0.7 on 34-35 of 36
  pairs. This is deliberate normalization, so it is a *designed* deviation from
  the near-raw reference, which keeps loop kinds distinct.
* **Loop variable and `def`/`class` keywords** are dropped: identifier-like
  or redundant with the rule label.

## All languages (3.4.0)

The same policy (hash expression/declaration *islands*, never the control-flow
skeleton; `STRUCTURAL_RULE_INDICES` guards nesting) was applied to Java 20/24,
C++14, C and Kotlin. Method as above, on `jv-umsa-dataset/all_java`, `all_cpp`,
`all_c` (two or three disjoint 12-problem sets each). The reference for
"unpruned" keeps the language's `for`/`while` equivalence, since that is a
deliberate normalization. Kotlin has no real corpus: `all_kotlin` is a
synthetic judge-style set (see its README), so its numbers are indicative.

| Language | Mean error before | Mean error now | Compression now |
|---|---|---|---|
| python_3 | 0.14-0.16 (~30x) | 0.083-0.092 | ~6x |
| python_3_13 | 0.14-0.18 (~30x) | 0.071-0.091 | ~6x |
| java_20 | 0.146 (93% of files = 1 node) | 0.063-0.075 | ~7.5x |
| java_24 | 0.297 (median 8 nodes) | 0.086-0.100 | ~9.5x |
| cpp_14 | 0.302, bias +0.26 (median 3 nodes) | 0.094-0.095 | ~7x |
| c | 0.033 (hashing was a near no-op, 1.6x) | 0.110-0.118 | ~5.5x |
| kotlin (synthetic) | 0.101 (3x on tiny programs) | 0.084-0.088 | ~6x |

**False similarity between different problems** (500 random cross-problem
pairs, fraction scoring >= 0.7; unpruned tree: 0% everywhere except the tiny
synthetic Kotlin programs). The old configs inflated it badly: java_24 40.4%,
cpp_14 34.4% (java_20 stayed at 0% but its mean similarity rose 0.31 -> 0.50).
Now: 0% for python_3, python_3_13, java_24, cpp_14 and c, 0-0.2% for java_20;
Kotlin goes from 1.6-4.2% (unpruned) to 6.8-9.4% because its synthetic programs
are ~20 nodes after pruning.

### Controlled clone sets

`jv-umsa-dataset/controlled` (Python) and `controlled/{java,cpp,c,kotlin}`: one
program and 8 rewrites (reformatting, comments, renaming, reordering, an extra
statement, wrapping in a function, `for` -> `while`, `+=`), 36 all-vs-all pairs,
all clones. Pairs scoring >= 0.7: python_3 35, python_3_13 34, java_20 34,
java_24 34, cpp_14 34, kotlin 35, **c 28** (all 8 misses involve the
function-wrapped rewrite, ~0.65; the extra `main` adds ~7 nodes to a ~20-node
tree). Two per-language tweaks were needed and cost fidelity: java_24 excludes
modifier rules (+~0.01 error) and cpp_14/c exclude built-in type keywords and,
for C, statement keywords (neutral).

### Language-specific notes

* **C++**: the grammar parses a type-less `x = e;` as a *declaration*; it is
  rebuilt into the same assignment-expression shape as `x += e;` / `p->n = e;`.
  `for`/`while`/`do` are one rule (`iterationStatement`), so all three share
  `LOOP`.
* **java_24**: `expression`/`statement` are unified rules; control statements get
  synthetic ids in `relabel_node()` (Python side only) so they can be marked
  structural. Assignments are no longer excluded.
* **java_20 / C++**: doubly-indexed targets (`a[i][j] op= ...`) do not yet
  match their expansion exactly.
* **C**: no assignment-operator rule exists; the operator is a bare terminal.

## Faidhi ladder (dataset F) and weighted hashes (3.4.2, `python_3`)

`scsc/notebooks/datasets/F` has 9 small problems, each a ladder r0..r4 where
every step adds one Faidhi change (rename, reorder, swap a control structure,
swap a technique): 90 related pairs with a known level plus 60 unrelated
pairs. It covers L4-L6, which random pairs from `all_py` almost never reach.

**Where the L5/L6 recall gap comes from.** With the 3.4.1 config, recall at
0.70 is 14/18 (L4), 16/27 (L5), 9/36 (L6). The near-raw tree (no hashing, no
rule exclusion) gets 14/16/11: pruning explains ~2 pairs, not the gap. The
rest is the scale of the index: these pairs really do share only 55-70% of
their tree, and a fixed 0.70 cuts through them. Ranking quality is fine:

| Method (F, python_3) | L5 AUC | L6 AUC | L5 / L6 recall at 0.70 |
|---|---|---|---|
| csim 3.4.1 | 0.978 | 0.916 | 16/27, 9/36 |
| csim near-raw tree | 1.00 | 0.99 | 16/27, 11/36 |
| csim 3.4.2 | 0.975 | 0.950 | 15/27, 9/36 |
| `pycode_similar` TreeDiff (scsc adapter) | 0.97 | 0.77 | 18/27, 13/36 |

(AUC = related vs. the 60 unrelated pairs. The TED row scores unrelated pairs
at 0.53 on average, csim at 0.23, so 0.70 is a much more lenient cut for it.
Its metric is also directional and per-function, not `1 - d / max(n1, n2)`.)

**What changed.** The remaining pruning loss was that a hashed node counted 1
however large it was, and different-but-similar hashes were all-or-nothing.
Hashed nodes now carry weight and a label multiset (see CHANGELOG 3.4.2).
Sweep of the weight exponent alpha (MAE, seeds 7/11): none 0.087/0.098; 0.25
0.073/0.083; 0.4 0.063/0.073; **0.6 0.052/0.061**; 0.75 0.060/0.063; 1.0
0.104/0.094 (bias turns positive). Weights alone (flat 0.5 substitution) gave
no gain (0.087-0.100), so the overlap-based substitution is what matters. Seed
23 (not used to choose): 0.098 -> 0.054. Time on the 2 x 1440 pairs is
unchanged (~6-7 s).

**What did not change.** Raising recall at 0.70 on L5/L6 would need a
calibrated (higher) index, not less pruning; that was not done, since it would
also raise the score of unrelated pairs.
