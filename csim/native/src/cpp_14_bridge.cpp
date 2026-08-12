/**
 * Java 20 Parser Bridge - flat binary emitter.
 *
 * JSON serialization proved to be ~90x more expensive than the parse itself,
 * so the tree is emitted as a flat preorder int32 buffer instead:
 *
 *     [count, (label, numChildren) * count]
 *
 * Label encoding matches csim's own convention in utils.py:
 *   - rule nodes      -> ruleIndex
 *   - terminal tokens -> TERMINAL_BASE + tokenType + 1
 *
 * Python rebuilds the tree from the buffer with a single preorder stack walk.
 */

#include "CPP14Lexer.h"
#include "CPP14Parser.h"
#include <antlr4-runtime.h>
#include <vector>
#include <cstdint>

using namespace antlr4;

// Terminals are emitted above this base so they can never collide with rule
// indices. The +1 shift keeps EOF (token type -1) inside the terminal space.
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
     * Parse Java source and emit the flat tree buffer.
     *
     * @param code      UTF-8 source
     * @param out_size  receives the number of int32 elements in the buffer
     * @return pointer to the buffer, or nullptr on error. Caller must not free.
     */
    const int32_t* parse_cpp_flat(const char* code, int32_t* out_size) {
        if (out_size) *out_size = 0;
        if (!code) return nullptr;

        try {
            ANTLRInputStream input(code);
            CPP14Lexer lexer(&input);
            lexer.removeErrorListeners();
            CommonTokenStream tokens(&lexer);
            CPP14Parser parser(&tokens);
            parser.removeErrorListeners();

            tree::ParseTree* parseTree = parser.translationUnit();
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
