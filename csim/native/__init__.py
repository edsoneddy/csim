"""Native (C++) ANTLR parsers for csim.

Parsing dominates csim's runtime (~99% for Java/C++), and the Python ANTLR
runtime spends nearly all of that inside adaptivePredict/execATN. This package
routes parsing through ANTLR's C++ runtime when a compiled library is present,
falling back to the pure-Python parsers otherwise.

The C++ side emits the parse tree as a flat preorder int32 buffer; `tree_builder`
rebuilds a node tree exposing the same interface the existing visitors already
use, so normalization/pruning/TED run unchanged.
"""

from .loader import is_available, parse_flat, native_parse

__all__ = ["is_available", "parse_flat", "native_parse"]
