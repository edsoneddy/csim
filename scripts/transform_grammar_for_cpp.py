"""Adapt a csim grammar to ANTLR's C++ target, in place.

csim's grammars are maintained for the Python target: semantic predicates call
helpers as ``self.foo()``. The C++ target needs ``this->foo()``, and it does not
auto-include the ``superClass`` header, so the grammar must carry an ``@header``
with that include.

This mirrors the ``transformGrammar.py`` that grammars-v4 ships next to its C++
targets; it exists separately here only because csim's grammars use ``self.``
where upstream uses ``this.``. Keeping it as a build step means the ``.g4`` files
stay a single source of truth shared by both targets.

Usage:
    python transform_grammar_for_cpp.py <grammar.g4> [...]
"""

import re
import sys
from pathlib import Path

# "// Insert here @header for C++ lexer."  ->  @header { #include "XBase.h" }
_HEADER_MARKER = re.compile(
    r"//\s*Insert here @header for C\+\+ (lexer|parser)\.", re.IGNORECASE
)
_SUPERCLASS = re.compile(r"superClass\s*=\s*(\w+)\s*;")


def transform(path):
    """Rewrite `path` in place for the C++ target. Returns a change summary."""
    source = Path(path).read_text(encoding="utf-8")
    original = source

    superclass = _SUPERCLASS.search(source)
    base_class = superclass.group(1) if superclass else None

    # Predicate/action receiver: Python's `self.` and upstream's `this.` both
    # become `this->`. Guarded so identifiers like `myself.x` are untouched.
    source, self_count = re.subn(r"(?<![\w.])self\.", "this->", source)
    source, this_count = re.subn(r"(?<![\w.>-])this\.", "this->", source)

    # The C++ target does not include the superClass header on its own.
    header_count = 0
    if base_class:
        replacement = f'@header {{#include "{base_class}.h"}}'
        source, header_count = _HEADER_MARKER.subn(replacement, source)

        if header_count == 0 and "@header" not in source:
            raise SystemExit(
                f"{path}: declares superClass '{base_class}' but has no @header "
                f"and no '// Insert here @header for C++ ...' marker to replace. "
                f"The generated C++ will not compile without that include."
            )

    if source != original:
        Path(path).write_text(source, encoding="utf-8")

    return {
        "self_to_this": self_count,
        "this_to_arrow": this_count,
        "header_inserted": header_count,
        "base_class": base_class,
    }


def main(argv):
    if len(argv) < 2:
        raise SystemExit(__doc__)

    for path in argv[1:]:
        if not Path(path).is_file():
            raise SystemExit(f"error: no such grammar: {path}")
        result = transform(path)
        changes = (
            f"self.->this-> {result['self_to_this']}, "
            f"this.->this-> {result['this_to_arrow']}, "
            f"@header {result['header_inserted']}"
        )
        print(f"  {Path(path).name}: {changes}")


if __name__ == "__main__":
    main(sys.argv)
