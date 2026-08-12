"""Locate, load and call the compiled native parsers.

Loading is lazy and failure-tolerant: if a library is missing or cannot be
loaded (wrong platform, missing antlr4 C++ runtime, ...), the language simply
reports as unavailable and callers fall back to the pure-Python parsers.
"""

import ctypes
import os
import sys
from pathlib import Path

# Per-language native configuration: library basename and exported symbol.
_NATIVE_CONFIG = {
    "java_20": ("libjava20_fast", "parse_java_flat"),
    "java_24": ("libjava24_fast", "parse_java24_flat"),
    "cpp_14": ("libcpp14_fast", "parse_cpp_flat"),
    # python_3_13 is intentionally absent: the modern Python grammar csim uses
    # publishes no C++ target (no PythonLexerBase.cpp/.h upstream), and the
    # legacy python3 grammar is slower than the Python runtime on CLI due to
    # cold-start overhead (only viable for long-running services).
}

_LIB_DIR = Path(__file__).parent / "lib"

# Cache of loaded handles: lang -> (cdll, func) or None when unavailable.
_handles = {}


def _library_suffix():
    if sys.platform == "darwin":
        return ".dylib"
    if sys.platform == "win32":
        return ".dll"
    return ".so"


def _disabled():
    """Allow opting out of native parsing (useful for debugging/benchmarks)."""
    return os.environ.get("CSIM_DISABLE_NATIVE", "").strip().lower() in (
        "1",
        "true",
        "yes",
    )


def _load(lang):
    """Load and configure the native library for `lang`, or return None."""
    if lang in _handles:
        return _handles[lang]

    config = _NATIVE_CONFIG.get(lang)
    if config is None or _disabled():
        _handles[lang] = None
        return None

    basename, symbol = config
    lib_path = _LIB_DIR / (basename + _library_suffix())

    if not lib_path.is_file():
        _handles[lang] = None
        return None

    try:
        cdll = ctypes.CDLL(str(lib_path))
        func = getattr(cdll, symbol)
        func.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32)]
        func.restype = ctypes.POINTER(ctypes.c_int32)
    except (OSError, AttributeError):
        _handles[lang] = None
        return None

    _handles[lang] = (cdll, func)
    return _handles[lang]


def is_available(lang):
    """Report whether a working native parser exists for `lang`."""
    return _load(lang) is not None


def parse_flat(file_content, lang):
    """Parse source with the native parser and return the flat int32 buffer.

    Returns:
        list[int]: The flat preorder buffer, or None if the native parser is
            unavailable or failed (caller should fall back to Python).
    """
    handle = _load(lang)
    if handle is None:
        return None

    _, func = handle
    size = ctypes.c_int32()

    try:
        pointer = func(file_content.encode("utf-8"), ctypes.byref(size))
    except Exception:
        return None

    if not pointer or size.value <= 0:
        return None

    # Copy out of the library-owned buffer before the next call reuses it.
    return pointer[: size.value]


def native_parse(file_content, lang):
    """Parse source natively and rebuild an ANTLR-compatible tree.

    Returns:
        The root node, or None when native parsing is unavailable or failed.
    """
    buffer = parse_flat(file_content, lang)
    if buffer is None:
        return None

    from ..utils import get_rule_names, get_symbolic_names  # local: avoid cycles
    from .tree_builder import build_tree

    rule_names = get_rule_names(lang)
    if not rule_names:
        return None

    try:
        return build_tree(buffer, rule_names, _literal_names(lang))
    except ValueError:
        return None


def _literal_names(lang):
    """Lexer literal names for `lang`, used to give terminals their text."""
    if lang == "java_20":
        from ..java_20.Java20Lexer import Java20Lexer

        return Java20Lexer.literalNames
    if lang == "java_24":
        from ..java_24.Java24Lexer import Java24Lexer

        return Java24Lexer.literalNames
    if lang == "cpp_14":
        from ..cpp_14.CPP14Lexer import CPP14Lexer

        return CPP14Lexer.literalNames
    if lang == "python_3_13":
        from ..python_3_13.PythonLexer import PythonLexer

        return PythonLexer.literalNames
    return None
