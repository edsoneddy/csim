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
