# C++ Parser Fix: `this` vs `self` in `IsPureSpecifierAllowed`

This document describes a correctness bug found in the C++14 parser (`grammars/CPP14Parser.g4` and the generated `csim/cpp_14/CPP14Parser.py`) while running the csim-batch-tuner compression sweep, and the fix applied.

## The bug

`memberDeclarator`'s grammar rule embeds a semantic predicate to disambiguate a pure-virtual specifier (`= 0`) from an ordinary default member initializer (`= <value>`):

```antlr
memberDeclarator
    : declarator (
        virtualSpecifierSeq
        | { this.IsPureSpecifierAllowed() }? pureSpecifier
        | { this.IsPureSpecifierAllowed() }? virtualSpecifierSeq pureSpecifier
        | braceOrEqualInitializer
    )
    | declarator
    ...
```

`this` is the correct keyword for this kind of embedded action in ANTLR's Java, C#, or JavaScript targets. It is **not** valid Python — the generated recognizer methods take `self`, not `this`. The grammar was evidently adapted from a non-Python target grammar without updating this one reference, and ANTLR faithfully carried the bug into the generated `CPP14Parser.py` in four places (two semantic-predicate calls in `memberDeclarator`, mirrored in the corresponding `_sempred` dispatch method).

The method itself is implemented correctly, as `self.IsPureSpecifierAllowed()`, in `csim/cpp_14/CPP14ParserBase.py:17` — it was simply unreachable.

## Impact

Because Python has no bare `this` name, every attempt to evaluate the predicate raised an uncaught `NameError`, not a graceful parse error. Any C++ source file containing either of these extremely common constructs would crash csim outright, without a syntax-error message and without any recovery:

- A **default member initializer** inside a class/struct body:
  ```cpp
  class Base {
      int value = 0;   // crashes
  };
  ```
- A **pure virtual function**:
  ```cpp
  class Shape {
      virtual double area() = 0;   // crashes
  };
  ```

Both are foundational, everyday C++ idioms, so this bug meant csim's C++ support was broken for a large fraction of realistic source files, not an edge case.

## The fix

Replaced `this` with `self` in both locations:

1. **`grammars/CPP14Parser.g4`** (lines 820–821) — the grammar source, so the bug is not reintroduced if the parser is ever regenerated from the grammar.
2. **`csim/cpp_14/CPP14Parser.py`** — the generated parser actually shipped and imported at runtime, patched directly in place (not regenerated) to keep the change to an auditable, minimal diff rather than risk unrelated churn from a full ANTLR regeneration:
   - `memberDeclarator` (two `if not self.IsPureSpecifierAllowed():` checks, including the predicate text in the `FailedPredicateException` message)
   - `memberDeclarator_sempred` (two `return self.IsPureSpecifierAllowed()` branches)

No other `this.` reference exists anywhere in the generated file.

## Verification

```python
# Before the fix, all three raised NameError: name 'this' is not defined
class Base { int value = 0; };            # default member initializer
class Base { int value = 5; };             # non-zero initializer (rules out an "= 0" special case)
class Base { virtual void f() = 0; };      # pure virtual function
```

After the fix, all three parse cleanly via `python scripts/harness.py --lang cpp --file <snippet>`, and the existing `test/` suite (`pytest test/`) continues to pass.
