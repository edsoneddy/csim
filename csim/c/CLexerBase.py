"""CLexerBase -- vendored from antlr/grammars-v4/c, patched for csim.

Two changes from upstream, both required for safe use inside csim (a library
called from `csim group`/`report`/`tree`, not a standalone per-file CLI tool):

1. Upstream read `sys.argv` directly to decide preprocessing mode. Inside
   csim, `sys.argv` holds *csim's own* CLI arguments (`--path`, `--lang c`,
   ...), which have nothing to do with C preprocessing -- reading it here
   would silently fall through to upstream's default (a real `gcc` shell-out
   via subprocess, once per file) regardless of what csim's caller actually
   wanted. Replaced with an explicit `set_args()`/`_args` class attribute,
   mirroring the native bridge's C++ `CLexerBase::setArgs()`.
2. The default (no explicit args) is now `--nopp` (skip preprocessing), not
   `--gcc`. csim can't assume gcc/clang is on PATH in a production
   container, and judge-submission .c files won't have consistent include
   paths anyway -- real preprocessing was never going to work here. The
   grammar's `Directive` lexer rule already swallows `#include`/`#define`/
   etc. lines as hidden tokens even unexpanded, so unpreprocessed source
   still parses (see csim/c/utils.py and CHANGELOG.md for the tradeoffs this
   implies). `--gcc`/`--clang` remain available via `set_args()` for anyone
   who explicitly wants real preprocessing.

Also drops the unconditional write of the source text to `<name>.p` in the
`--nopp` path: upstream did this on every single call (even in the
pass-through case), which is wasted I/O per file and a race condition under
concurrent use, for a debug artifact csim has no use for.
"""

import platform
import subprocess
import sys

from antlr4 import Lexer, InputStream


class CLexerBase(Lexer):
    _args = []

    def __init__(self, input, output=sys.stdout):
        super().__init__(CLexerBase.runGccAndMakeStream(input), output)

    @staticmethod
    def set_args(args):
        """Configure preprocessing mode. Must be called before any CLexer
        instance is created. See the module docstring for available flags.
        """
        CLexerBase._args = args

    @staticmethod
    def runGccAndMakeStream(input):
        is_windows = platform.system() == "Windows"

        args = CLexerBase._args

        vsc = any("--vsc" in a.lower() for a in args)
        gcc = any("--gcc" in a.lower() for a in args)
        clang = any("--clang" in a.lower() for a in args)
        nopp = any("--nopp" in a.lower() for a in args)

        if not (vsc or gcc or clang):
            nopp = True

        ppOptions = CLexerBase.extractPreprocessorOptions(args)

        sourceName = getattr(input, 'name', None) or getattr(input, 'fileName', None) or ""
        inputText = input.getText(0, input.size - 1)

        if not sourceName or not sourceName.endswith(".c"):
            sourceName = "stdin.c"

        outputName = sourceName + ".p"

        if nopp:
            return InputStream(inputText)

        if sourceName == "stdin.c":
            with open(sourceName, "w") as f:
                f.write(inputText)

        if gcc:
            output = ""
            try:
                gccCommand = "gcc.exe" if is_windows else "gcc"
                ppOptsStr = " ".join('"' + o + '"' for o in ppOptions)
                cmd = f'{gccCommand} -std=c2x -E -C {ppOptsStr} "{sourceName}"'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                output = result.stdout
            except:
                pass
            with open(outputName, "w") as f:
                f.write(output)
            return InputStream(output)

        if clang:
            output = ""
            try:
                clangCommand = "clang.exe" if is_windows else "clang"
                ppOptsStr = " ".join('"' + o + '"' for o in ppOptions)
                cmd = f'{clangCommand} -std=c2x -E -C {ppOptsStr} "{sourceName}"'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                output = result.stdout
            except:
                pass
            with open(outputName, "w") as f:
                f.write(output)
            return InputStream(output)

        raise Exception("No preprocessor specified.")

    @staticmethod
    def extractPreprocessorOptions(args):
        options = []
        for arg in args:
            if arg.startswith("--D"):
                options.append("-D" + arg[3:])
            elif arg.startswith("--I"):
                options.append("-I" + arg[3:])
        return options
