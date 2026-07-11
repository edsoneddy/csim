# Search Strategies in csim

This document explains the search strategy used in csim for grouping similar files: **exhaustive search**.

## Overview

When grouping files by similarity, csim needs to:
1. Find candidate pairs of files that might be similar
2. Calculate the precise structural similarity for each candidate pair
3. Group files based on a similarity threshold

The tool uses an exhaustive all-pairs approach for candidate selection and performs precise structural comparisons to ensure high accuracy.

## Strategy: Exhaustive Search (Default)

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
| **Best For** | Small to medium datasets |
| **Pros** | Finds all similar files without missing any |
| **Cons** | Slow for very large datasets |

### When to Use

Use exhaustive search when:
- Your dataset is small to medium-sized
- Accuracy is critical and missing a copy is unacceptable
- You can afford the computational cost for full comparison

### Command

```bash
csim group --path /path/to/files --threshold 0.8
```

---

## Troubleshooting

### "My copies weren't detected!"

1. **Try adjusting the threshold:** Try a lower `--threshold` (e.g., 0.7)
2. **Check the code:** Verify the submissions are structurally similar
3. **Run an exhaustive report:** Use `csim report` to inspect pairwise similarity values

---

## See Also

- [Parse Tree (Wikipedia)](https://en.wikipedia.org/wiki/Parse_tree)
- [Tree Edit Distance (Wikipedia)](https://en.wikipedia.org/wiki/Tree_edit_distance)
