#pragma once

#include "antlr4-runtime.h"
#include <memory>
#include <string>
#include <vector>

/// CLexerBase — vendored from antlr/grammars-v4/c, patched for csim.
///
/// Integrates preprocessing into the lexer: the constructor accepts the
/// original (un-preprocessed) CharStream and transparently replaces it
/// with a preprocessed version before any token is produced.
///
/// Preprocessing modes (configured via setArgs() before construction):
///   (default)  — skip preprocessing (pass-through)
///   --nopp     — skip preprocessing (pass-through), same as default
///   --gcc      — gcc -std=c2x -E -C
///   --clang    — clang -std=c2x -E -C
///
/// Additional options forwarded to the preprocessor:
///   --Dname=value   → -Dname=value
///   --Ipath         → -Ipath
///
/// csim-specific change from upstream: the default was originally --gcc
/// (shell out to a real `gcc` via popen() on every parse). csim can't assume
/// gcc/clang is on PATH in a production container, and judge-submission .c
/// files won't have consistent include paths anyway -- real preprocessing
/// was never going to work here. Defaulting to --nopp instead means csim
/// gets correct behavior without every call site needing to remember to opt
/// out; the grammar's `Directive` lexer rule already swallows `#include`/
/// `#define`/etc. lines as hidden tokens even unexpanded, so unpreprocessed
/// source still parses (see csim/c/utils.py and CHANGELOG.md for the
/// tradeoffs this implies). --gcc/--clang remain available via setArgs() for
/// anyone who explicitly wants real preprocessing.
class CLexerBase : public antlr4::Lexer {
public:
    /// Construct lexer, transparently preprocessing the input stream.
    CLexerBase(antlr4::CharStream *input);

    /// Set command-line arguments that control preprocessing behaviour.
    /// Must be called **before** any CLexer instance is created.
    static void setArgs(const std::vector<std::string>& args);

    /// Run the appropriate preprocessor on @p input and return a new
    /// ANTLRInputStream with the preprocessed content.
    /// Returns nullptr when input should be used as-is.
    static std::unique_ptr<antlr4::ANTLRInputStream>
    runGccAndMakeStream(antlr4::CharStream *input);

private:
    /// Delegating constructor — receives the already-preprocessed stream.
    /// Lexer is initialised with the preprocessed stream (or original if null).
    CLexerBase(antlr4::CharStream *original,
              std::unique_ptr<antlr4::ANTLRInputStream> preprocessed);

    static bool hasArg(const std::string& arg);
    static std::vector<std::string> extractPreprocessorOptions();

    /// Arguments set via setArgs().  Inline-initialised empty.
    inline static std::vector<std::string> args_;

    /// Holds the preprocessed stream so it outlives the lexer.
    std::unique_ptr<antlr4::ANTLRInputStream> preprocessedStream_;
};
