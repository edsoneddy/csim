#!/usr/bin/env bash
#
# Build csim's native (C++) ANTLR parsers.
#
# Regenerates the ANTLR C++ lexer/parser for each supported language, compiles
# them together with csim's bridge, and installs the resulting shared library
# into csim/native/lib/ where the loader looks for it.
#
# Supported languages: java_20, java_24 (grammars-v4/java/java), cpp_14,
# python_3 (grammars-v4/python/python, the "universal Python 2/3" grammar),
# kotlin (grammars-v4/kotlin/kotlin -- no custom base class needed, this
# grammar declares no superClass at all), c (grammars-v4/c -- ships a real
# symbol-table implementation for typedef disambiguation; the vendored
# CLexerBase/CParserBase default to --nopp and never shell out to a real
# preprocessor, see grammars/CLexerBase.h for why).
# python_3_13 (the modern grammar) has no C++ target upstream and keeps using
# the pure-Python parser; python_3 is a separate, additional language key.
#
# Requirements:
#   - antlr4 (the generator) on PATH
#   - the ANTLR C++ runtime (brew install antlr4-cpp-runtime, or apt/vcpkg)
#   - a C++17 compiler
#
# Usage:
#   scripts/build_native_parsers.sh [language ...]

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GRAMMARS_DIR="$REPO_ROOT/grammars"
BRIDGE_DIR="$REPO_ROOT/csim/native/src"
LIB_DIR="$REPO_ROOT/csim/native/lib"
BUILD_DIR="$REPO_ROOT/build/native"

LANGUAGES=("${@:-java_20 java_24 cpp_14 python_3 kotlin c}")
read -r -a LANGUAGES <<< "${LANGUAGES[*]}"

# --- toolchain discovery ----------------------------------------------------

# `antlr4` is commonly set up as a shell alias, which is not visible to scripts,
# so fall back to locating the jar. Override with ANTLR_JAR=/path/to/antlr.jar.
if command -v antlr4 >/dev/null 2>&1; then
    ANTLR="antlr4"
else
    if [ -z "${ANTLR_JAR:-}" ]; then
        # Several jars may be installed side by side; take the highest version,
        # since the C++ target only exists from 4.5 onwards.
        # `|| true`: unmatched globs make ls exit non-zero, which would trip
        # `set -e`/`pipefail` even though finding nothing is a valid outcome here.
        ANTLR_JAR="$(
            { ls -1 \
                "$HOME"/Bin/antlr-*-complete.jar \
                /usr/local/lib/antlr-*-complete.jar \
                /opt/homebrew/share/antlr*/antlr-*-complete.jar \
                2>/dev/null || true; } \
            | sort -V | tail -n 1
        )"
    fi

    if [ -z "${ANTLR_JAR:-}" ] || [ ! -f "$ANTLR_JAR" ]; then
        echo "error: antlr4 not found." >&2
        echo "  Put antlr4 on PATH, or set ANTLR_JAR=/path/to/antlr-4.x-complete.jar" >&2
        echo "  See grammars/parser_gen_guide.md" >&2
        exit 1
    fi
    ANTLR="java -jar $ANTLR_JAR"
fi

if [ -n "${ANTLR_CPP_INCLUDE:-}" ] && [ -n "${ANTLR_CPP_LIB:-}" ]; then
    # Explicit paths, used by CI where the runtime is built from source to match
    # the generator version exactly.
    ANTLR_INCLUDE="$ANTLR_CPP_INCLUDE"
    ANTLR_LIB="$ANTLR_CPP_LIB"
elif command -v brew >/dev/null 2>&1 && brew --prefix antlr4-cpp-runtime >/dev/null 2>&1; then
    ANTLR_PREFIX="$(brew --prefix antlr4-cpp-runtime)"
    ANTLR_INCLUDE="$ANTLR_PREFIX/include/antlr4-runtime"
    ANTLR_LIB="$ANTLR_PREFIX/lib"
elif [ -d /usr/include/antlr4-runtime ]; then
    ANTLR_INCLUDE=/usr/include/antlr4-runtime
    ANTLR_LIB=/usr/lib
elif [ -d /usr/local/include/antlr4-runtime ]; then
    ANTLR_INCLUDE=/usr/local/include/antlr4-runtime
    ANTLR_LIB=/usr/local/lib
else
    echo "error: ANTLR C++ runtime headers not found." >&2
    echo "  macOS: brew install antlr4-cpp-runtime" >&2
    echo "  Debian/Ubuntu: apt-get install libantlr4-runtime-dev" >&2
    exit 1
fi

case "$(uname -s)" in
    Darwin)
        LIB_SUFFIX=".dylib"
        # macOS always provides libc++; nothing extra to bundle.
        PORTABILITY_FLAGS=()
        ;;
    *)
        LIB_SUFFIX=".so"
        # Link the C++ runtime in statically: distros ship widely differing
        # libstdc++ versions, and a wheel built on one would fail to load on
        # an older one -- silently, since csim just falls back to Python.
        PORTABILITY_FLAGS=(-static-libstdc++ -static-libgcc)
        ;;
esac

CXX="${CXX:-c++}"

echo "antlr4 runtime includes : $ANTLR_INCLUDE"
echo "antlr4 runtime libs     : $ANTLR_LIB"
echo "antlr4 generator        : $ANTLR"
echo "compiler                : $CXX"
echo

# --- per-language build -----------------------------------------------------

# lang | lexer grammar | parser grammar | extra sources | output library
build_language() {
    local lang="$1" lexer_g4="$2" parser_g4="$3" extra_srcs="$4" out_lib="$5"
    local work="$BUILD_DIR/$lang"

    echo "=== $lang ==="
    rm -rf "$work"
    mkdir -p "$work"

    cp "$GRAMMARS_DIR/$lexer_g4" "$GRAMMARS_DIR/$parser_g4" "$work/"

    # Some grammars ship C++ helper base classes plus an official transform that
    # adapts the grammar to the C++ target ("this." -> "this->" and the @header
    # include). Run it when present; it is the upstream-supported step.
    for extra in $extra_srcs; do
        if [ -f "$GRAMMARS_DIR/$extra" ]; then
            cp "$GRAMMARS_DIR/$extra" "$work/"
        else
            echo "error: missing required C++ helper source: grammars/$extra" >&2
            exit 1
        fi
    done

    # csim's grammars target Python (`self.` receivers, no @header for the
    # superClass). Adapt the working copies to the C++ target; the .g4 files in
    # grammars/ stay the single source of truth for both targets.
    echo "  adapting grammar to the C++ target:"
    python "$REPO_ROOT/scripts/transform_grammar_for_cpp.py" \
        "$work/$lexer_g4" "$work/$parser_g4"

    (cd "$work" && $ANTLR "$lexer_g4" -Dlanguage=Cpp -no-visitor -no-listener -o .)
    (cd "$work" && $ANTLR "$parser_g4" -Dlanguage=Cpp -Xexact-output-dir -no-visitor -no-listener -o .)
    echo "  generated C++ lexer/parser"

    # Ensure ParserBase.h/LexerBase.h are included in the generated .h files
    # (ANTLR doesn't do this automatically for every grammar). Done via
    # Python, not sed -i: BSD sed (macOS) and GNU sed (Linux CI) take -i's
    # backup-suffix argument differently -- `sed -i ''` only works on BSD,
    # and silently treats the script as a filename on GNU sed, failing with
    # "No such file or directory". Python's file handling doesn't have that
    # split, and the script already depends on Python being present (see the
    # transform_grammar_for_cpp.py call above).
    local parser_base_name="${parser_g4%.g4}Base"  # e.g. Java24ParserBase from Java24Parser.g4
    if [ -f "$work/${parser_base_name}.h" ]; then
        local parser_h="${parser_g4%.g4}.h"
        if ! grep -q "#include \"${parser_base_name}.h\"" "$work/$parser_h"; then
            python3 -c "
import pathlib
p = pathlib.Path('$work/$parser_h')
text = p.read_text()
p.write_text(text.replace(
    '#include \"antlr4-runtime.h\"',
    '#include \"antlr4-runtime.h\"\n#include \"${parser_base_name}.h\"',
    1,
))
"
        fi
    fi
    local lexer_base_name="${lexer_g4%.g4}Base"
    if [ -f "$work/${lexer_base_name}.h" ]; then
        local lexer_h="${lexer_g4%.g4}.h"
        if ! grep -q "#include \"${lexer_base_name}.h\"" "$work/$lexer_h"; then
            python3 -c "
import pathlib
p = pathlib.Path('$work/$lexer_h')
text = p.read_text()
p.write_text(text.replace(
    '#include \"antlr4-runtime.h\"',
    '#include \"antlr4-runtime.h\"\n#include \"${lexer_base_name}.h\"',
    1,
))
"
        fi
    fi

    cp "$BRIDGE_DIR/${lang}_bridge.cpp" "$work/bridge.cpp"

    local sources=(bridge.cpp)
    while IFS= read -r generated; do
        sources+=("$(basename "$generated")")
    done < <(find "$work" -maxdepth 1 -name '*.cpp' ! -name 'bridge.cpp' | sort)

    # Link the ANTLR runtime statically when the archive is available, so the
    # shipped library depends only on system libs. A dynamic link would bake in
    # an absolute path to the local install (e.g. Homebrew's), and the library
    # would silently fail to load anywhere else -- csim would quietly fall back
    # to the Python parser with no speedup and no error.
    local runtime_link=(-L"$ANTLR_LIB" -lantlr4-runtime)
    if [ -f "$ANTLR_LIB/libantlr4-runtime.a" ]; then
        runtime_link=("$ANTLR_LIB/libantlr4-runtime.a")
        echo "  linking ANTLR runtime statically"
    else
        echo "  warning: no libantlr4-runtime.a found; linking dynamically." >&2
        echo "           The result will only load where the runtime is installed." >&2
    fi

    (cd "$work" && "$CXX" -fPIC -shared \
        -I"$ANTLR_INCLUDE" -I. \
        "${sources[@]}" \
        "${runtime_link[@]}" \
        ${PORTABILITY_FLAGS[@]+"${PORTABILITY_FLAGS[@]}"} \
        -std=c++17 -O3 \
        -o "$out_lib$LIB_SUFFIX")

    mkdir -p "$LIB_DIR"
    cp "$work/$out_lib$LIB_SUFFIX" "$LIB_DIR/"
    echo "  installed $LIB_DIR/$out_lib$LIB_SUFFIX"
    echo
}

for lang in "${LANGUAGES[@]}"; do
    case "$lang" in
        java_20)
            build_language java_20 Java20Lexer.g4 Java20Parser.g4 "" libjava20_fast
            ;;
        java_24)
            build_language java_24 Java24Lexer.g4 Java24Parser.g4 \
                "Java24ParserBase.cpp Java24ParserBase.h" libjava24_fast
            ;;
        cpp_14)
            build_language cpp_14 CPP14Lexer.g4 CPP14Parser.g4 \
                "CPP14ParserBase.cpp CPP14ParserBase.h" libcpp14_fast
            ;;
        python_3)
            build_language python_3 Python3Lexer.g4 Python3Parser.g4 \
                "Python3LexerBase.cpp Python3LexerBase.h Python3ParserBase.cpp Python3ParserBase.h" \
                libpython3_fast
            ;;
        kotlin)
            # No C++ base class needed -- the grammar declares no superClass.
            # UnicodeClasses.g4 is an imported lexer grammar (not a base
            # class); it must be present alongside KotlinLexer.g4 for ANTLR's
            # `import UnicodeClasses;` to resolve, but ANTLR inlines it
            # directly into the generated lexer (no separate .cpp/.h of its
            # own), so it needs copying, not compiling.
            build_language kotlin KotlinLexer.g4 KotlinParser.g4 \
                "UnicodeClasses.g4" libkotlin_fast
            ;;
        c)
            build_language c CLexer.g4 CParser.g4 \
                "CLexerBase.cpp CLexerBase.h CParserBase.cpp CParserBase.h SymbolTable.cpp SymbolTable.h Symbol.h TypeClassification.h" \
                libc_fast
            ;;
        *)
            echo "error: no native parser is defined for '$lang'" >&2
            exit 1
            ;;
    esac
done

echo "Done. Verify with:  python -m pytest test/test_native_parsers.py"
