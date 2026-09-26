"""Locate, load and call the compiled native parsers.

Loading is lazy and failure-tolerant: if a library is missing or cannot be
loaded (wrong platform, missing antlr4 C++ runtime, ...), the language simply
reports as unavailable and callers fall back to the pure-Python parsers.
"""

import ctypes
import os
import re
import sys
from pathlib import Path

# Per-language native configuration: library basename and exported symbol.
_NATIVE_CONFIG = {
    "java_20": ("libjava20_fast", "parse_java_flat"),
    "java_24": ("libjava24_fast", "parse_java24_flat"),
    "cpp_14": ("libcpp14_fast", "parse_cpp_flat"),
    "python_3": ("libpython3_fast", "parse_python3_flat"),
    # python_3_13 is intentionally absent: the modern Python grammar csim uses
    # publishes no C++ target upstream. python_3 (grammars-v4/python/python,
    # the "universal Python 2/3" grammar) is a separate, additional language
    # with its own native parser -- python_3_13 is unaffected and unchanged.
    "kotlin": ("libkotlin_fast", "parse_kotlin_flat"),
    "c": ("libc_fast", "parse_c_flat"),
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


# lang -> (package dir name, Lexer .tokens basename).
_TOKENS_FILES = {
    "java_20": ("java_20", "Java20Lexer.tokens"),
    "java_24": ("java_24", "Java24Lexer.tokens"),
    "cpp_14": ("cpp_14", "CPP14Lexer.tokens"),
    "python_3_13": ("python_3_13", "PythonLexer.tokens"),
    "python_3": ("python_3", "Python3Lexer.tokens"),
    "kotlin": ("kotlin", "KotlinLexer.tokens"),
    "c": ("c", "CLexer.tokens"),
}

# `'<literal>'=<type>` or `NAME=<type>`; only the literal form is of interest
# here. The literal body may contain backslash-escaped characters (e.g.
# Kotlin's SINGLE_QUOTE token, `'\''=52`), hence the non-greedy alternation.
_TOKENS_LINE = re.compile(r"^'((?:[^'\\]|\\.)*)'=(-?\d+)$")

_literal_names_cache = {}


def _unescape_literal(text):
    """Undo ANTLR's `.tokens`-file backslash escaping (`\\'` -> `'`, `\\\\` -> `\\`, ...)."""
    out = []
    i = 0
    while i < len(text):
        if text[i] == "\\" and i + 1 < len(text):
            out.append(text[i + 1])
            i += 2
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def _literal_names(lang):
    """Map token type -> unquoted literal text for `lang`'s lexer, used to
    give fixed-spelling terminals (keywords, punctuation) their source text
    when rebuilding a tree from the native flat buffer.

    Deliberately does NOT read the generated Lexer class's own `literalNames`
    list: that list is populated in literal-declaration order, not indexed by
    token type, so `literalNames[token_type]` silently returns the WRONG
    literal for a real grammar (confirmed on both CPP14Lexer and KotlinLexer
    -- e.g. `CPP14Lexer.literalNames[CPP14Lexer.LeftParen]` is `"'/'"`, not
    `"'('"`). ANTLR's own runtime indexes it the same naive way (see
    antlr4/IntervalSet.py's elementName()), so this is an upstream
    code-generation quirk, not something introduced here.

    The generated `.tokens` file (`'<literal>'=<type>` / `NAME=<type>` lines,
    one per token) IS correctly keyed by the real token type -- confirmed
    against the same two lexers above -- so it's used as the source of truth
    instead. Parsed once per language and cached.
    """
    if lang in _literal_names_cache:
        return _literal_names_cache[lang]

    config = _TOKENS_FILES.get(lang)
    if config is None:
        _literal_names_cache[lang] = None
        return None

    package_dir, basename = config
    path = Path(__file__).parent.parent / package_dir / basename

    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        _literal_names_cache[lang] = None
        return None

    literals = {}
    for line in text.splitlines():
        match = _TOKENS_LINE.match(line)
        if match:
            literal, token_type = match.groups()
            literals[int(token_type)] = _unescape_literal(literal)

    _literal_names_cache[lang] = literals
    return literals
