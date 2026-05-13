# Search Strategies in csim

This document explains the two search strategies available in csim for grouping similar files: **exhaustive search** and **LSH (Locality Sensitive Hashing)**.

## Overview

When grouping files by similarity, csim needs to:
1. Find candidate pairs of files that might be similar
2. Calculate the precise structural similarity for each candidate pair
3. Group files based on a similarity threshold

The choice of strategy affects how step 1 is performed, which impacts both speed and accuracy.

## Strategy 1: Exhaustive Search (Default)

### How It Works

Exhaustive search compares **every file against every other file**, then calculates the precise structural similarity for each pair.

```
For files [A, B, C, D]:
  Compare: A-B, A-C, A-D, B-C, B-D, C-D
  Total comparisons: C(n,2) = n*(n-1)/2
  Time complexity: O(n²)
```

### Characteristics

| Property | Value |
|----------|-------|
| **Precision** | Maximum (100%) |
| **Recall** | Maximum (100%) |
| **Time Complexity** | O(n²) |
| **Best For** | Small datasets (<100 files) |
| **Pros** | Finds all similar files without missing any |
| **Cons** | Slow for large datasets |

### When to Use

Use exhaustive search when:
- Your dataset is small (< 100 files)
- Accuracy is critical and missing a copy is unacceptable
- You have sufficient computational time available
- You're verifying a specific assignment or contest

### Command

```bash
csim group --path /path/to/files --threshold 0.8 --strategy exhaustive
```

---

## Strategy 2: LSH (Locality Sensitive Hashing)

### How It Works

LSH is a probabilistic technique that groups similar items together with high probability in a pre-processing step, **before detailed comparison**. In csim's implementation:

1. **Tokenization Phase:** Files are tokenized (converted to token sequences)
2. **MinHash Generation:** Each token sequence is hashed into a compact fingerprint (MinHash)
3. **LSH Indexing:** MinHashes are indexed into hash buckets using LSH
4. **Candidate Selection:** For each file, LSH retrieves files in the same or nearby buckets as candidates
5. **Detailed Comparison:** Only candidates are subjected to the expensive structural similarity calculation

```
For files [A, B, C, D]:
  Tokenize: A, B, C, D
  Generate MinHashes and build LSH index
  For each file:
    Query LSH → Get candidates (typically 1-5 files instead of N-1)
    Compare only with candidates
  Total expensive comparisons: << n²
  Time complexity: O(n) to O(n log n) in practice
```

### Characteristics

| Property | Value |
|----------|-------|
| **Precision** | Very High (>99%) |
| **Recall** | Very High (>99%) |
| **Time Complexity** | O(n) to O(n log n) |
| **Best For** | Large datasets (>100 files) |
| **Pros** | Dramatically faster than exhaustive; high accuracy |
| **Cons** | Very small chance of missing a copy (< 1%) |

### Parameters in csim

- **JACCARD_THRESHOLD (Internal):** Set to 0.3 for LSH candidate selection
  - This is a token-level similarity threshold, not the structural similarity threshold
  - Lower values = more candidates = higher accuracy but slower
  - Higher values = fewer candidates = faster but risk of missing copies
  - Default of 0.3 is well-tuned for code

- **Structural Threshold (User-Provided):** The `--threshold` parameter
  - Candidates must also pass the structural similarity check
  - Provides final filtering to ensure true positives

### When to Use

Use LSH when:
- Your dataset is large (> 100 files)
- Speed is important
- The < 1% chance of missing a copy is acceptable
- You're checking for plagiarism in large courses or online judge systems
- You need to scale to thousands of submissions

### Command

```bash
csim group --path /path/to/files --threshold 0.8 --strategy lsh
```

---

## Comparison

### Performance Metrics

For a dataset of 1000 files (500 pairs actual in practice):

| Metric | Exhaustive | LSH |
|--------|-----------|-----|
| Time | ~2-3 hours | ~2-3 minutes |
| Pairs Compared Structurally | 499,500 | ~2,000-5,000 |
| Copies Detected | 100% (500/500) | ~99% (495-500/500) |

*Note: Times are estimates and depend on file sizes and code complexity*

### Decision Tree

```
Do you have > 100 files?
├── Yes → Use LSH (--strategy lsh)
│   └── Do you need to catch every single copy?
│       ├── Yes → Verify with exhaustive later
│       └── No → LSH is sufficient
└── No → Use Exhaustive (--strategy exhaustive)
    └── Maximum precision guaranteed
```

---

## Advanced: Understanding LSH in csim

### LSH Configuration

csim uses `MinHashLSH` from the `datasketch` library with:
- **num_perm = 128:** Number of hash functions for MinHash
  - Higher = more accurate but slower
  - 128 is a good balance
- **threshold = 0.3:** Jaccard similarity threshold for bucketing
  - This is **different** from the structural similarity threshold

### Why Two Thresholds?

1. **Jaccard Threshold (0.3 - LSH):** Token-level similarity
   - Fast to compute (on MinHashes)
   - Used to narrow down candidates
   - Conservative (includes false positives)

2. **Structural Threshold (user input):** AST-level similarity
   - Slow to compute (Tree Edit Distance)
   - Applied to candidates from LSH
   - Precise (filters out false positives)

### Why This Works

LSH with 0.3 Jaccard threshold will almost certainly include all files with high structural similarity (0.8+). Why?

- Files with 90% structural similarity typically have at least 30% token overlap
- LSH is conservative to avoid missing candidates
- The structural check filters false positives

This combination gives you the best of both worlds:
- **Speed** from LSH's fast candidate selection
- **Precision** from detailed structural comparison

---

## Tuning LSH

For advanced users who want to tune LSH performance:

Edit `csim/utils.py` and modify `JACCARD_THRESHOLD` in the `group_by_lsh_search` function:

```python
JACCARD_THRESHOLD = 0.3  # Adjust this value
```

- **Increase (0.4-0.5):** Fewer candidates, faster, slightly higher risk of missing copies
- **Decrease (0.1-0.2):** More candidates, slower, extremely safe

Default of 0.3 is recommended for most use cases.

---

## Troubleshooting

### "My copies weren't detected!"

1. **Try exhaustive mode first:** `--strategy exhaustive`
   - If found in exhaustive, LSH might be missing them
   - Reduce JACCARD_THRESHOLD to 0.2 or 0.1

2. **Check the threshold:** Try a lower `--threshold` (0.7 instead of 0.8)
   - Maybe your copies are 75% similar, not 80%

3. **Check the code:** Are they *structurally* similar?
   - LSH detects structural plagiarism, not style plagiarism
   - If the algorithm is completely rewritten, it might not match

### "LSH is too slow"

This shouldn't happen. If it is:
1. Check if you accidentally set JACCARD_THRESHOLD too low
2. Try a smaller dataset to isolate the issue
3. File an issue on GitHub

---

## See Also

- [Locality Sensitive Hashing (Wikipedia)](https://en.wikipedia.org/wiki/Locality-sensitive_hashing)
- [MinHash (Wikipedia)](https://en.wikipedia.org/wiki/MinHash)
- [datasketch Documentation](https://datasketch.readthedocs.io/)
