/**
 * Kotlin Parser Bridge - flat binary emitter.
 *
 * Flat preorder int32 buffer format (same as java_20_bridge.cpp,
 * java_24_bridge.cpp, cpp_14_bridge.cpp, python_3_bridge.cpp):
 *
 *     [count, (label, numChildren) * count]
 *
 * Label encoding:
 *   - rule nodes      -> ruleIndex (no relabeling needed -- unlike java_24/
 *                        python_3, this grammar has no ANTLR labeled
 *                        alternatives sharing a rule index, so every rule
 *                        already has a unique, unambiguous identity)
 *   - terminal tokens -> TERMINAL_BASE + tokenType + 1
 *
 * Uses grammars-v4/kotlin/kotlin grammar. Entry rule is `kotlinFile`. No
 * custom lexer/parser base class is needed: the grammar declares no
 * superClass at all -- string-template interpolation is handled entirely
 * via native ANTLR lexer modes, which the C++ target supports without any
 * hand-written glue code.
 */

#include "KotlinLexer.h"
#include "KotlinParser.h"
#include <antlr4-runtime.h>
#include <vector>
#include <cstdint>

using namespace antlr4;

static const int32_t TERMINAL_BASE = 1000000;

static void flatten(tree::ParseTree* node, std::vector<int32_t>& out) {
    if (!node) return;

    if (auto terminal = dynamic_cast<tree::TerminalNode*>(node)) {
        int32_t tokenType = terminal->getSymbol()
            ? static_cast<int32_t>(terminal->getSymbol()->getType())
            : -1;
        out.push_back(TERMINAL_BASE + tokenType + 1);
        out.push_back(0);  // terminals have no children
        return;
    }

    if (auto rule = dynamic_cast<RuleContext*>(node)) {
        out.push_back(static_cast<int32_t>(rule->getRuleIndex()));
        out.push_back(static_cast<int32_t>(rule->children.size()));
        for (auto* child : rule->children) {
            flatten(child, out);
        }
    }
}

extern "C" {
    // Buffer persists until the next call on this thread.
    static thread_local std::vector<int32_t> buffer;

    /**
     * Parse Kotlin source and emit the flat tree buffer.
     *
     * @param code      UTF-8 source
     * @param out_size  receives the number of int32 elements in the buffer
     * @return pointer to the buffer, or nullptr on error. Caller must not free.
     */
    const int32_t* parse_kotlin_flat(const char* code, int32_t* out_size) {
        if (out_size) *out_size = 0;
        if (!code) return nullptr;

        try {
            ANTLRInputStream input(code);
            KotlinLexer lexer(&input);
            lexer.removeErrorListeners();
            CommonTokenStream tokens(&lexer);
            KotlinParser parser(&tokens);
            parser.removeErrorListeners();

            tree::ParseTree* parseTree = parser.kotlinFile();
            if (!parseTree) return nullptr;

            buffer.clear();
            buffer.reserve(16384);
            flatten(parseTree, buffer);

            if (out_size) *out_size = static_cast<int32_t>(buffer.size());
            return buffer.data();
        } catch (...) {
            return nullptr;
        }
    }
}
