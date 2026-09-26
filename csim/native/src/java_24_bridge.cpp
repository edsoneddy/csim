/**
 * Java 24 Parser Bridge - flat binary emitter.
 *
 * Flat preorder int32 buffer format (same as java_20_bridge.cpp, cpp_14_bridge.cpp):
 *
 *     [count, (label, numChildren) * count]
 *
 * Label encoding:
 *   - rule nodes      -> ruleIndex, EXCEPT assignment-shaped `expression`
 *                        nodes (see effectiveRuleIndex() below)
 *   - terminal tokens -> TERMINAL_BASE + tokenType + 1
 *
 * Uses grammars-v4/java/java grammar (Java 24, optimized, left-factored).
 */

#include "Java24Lexer.h"
#include "Java24Parser.h"
#include <antlr4-runtime.h>
#include <vector>
#include <cstdint>

using namespace antlr4;

static const int32_t TERMINAL_BASE = 1000000;

// Must match SYNTHETIC_ASSIGNMENT_EXPR in csim/java_24/utils.py.
static const int32_t SYNTHETIC_ASSIGNMENT_EXPR = 200;

/**
 * java_24's grammar folds assignment into the unified `expression` rule as
 * one alternative among many, sharing both the rule index (RuleExpression)
 * and the generated label (#BinaryOperatorExpression) with every other
 * binary operator -- see grammars/Java24Parser.g4, "Level 1, Assignment".
 * Neither lets EXCLUDED_RULE_TYPES isolate assignments the way java_20's
 * separate `assignment` rule does. What DOES isolate it: an
 * assignment-shaped expression is always `expression bop=(ASSIGN|...)
 * expression` -- exactly 3 children, with child 1 being one of the 12
 * assignment-operator tokens. This mirrors relabel_node() in
 * csim/java_24/utils.py exactly; keep both in sync.
 */
static bool isAssignmentOperatorToken(int32_t tokenType) {
    switch (tokenType) {
        case Java24Lexer::ASSIGN:
        case Java24Lexer::ADD_ASSIGN:
        case Java24Lexer::SUB_ASSIGN:
        case Java24Lexer::MUL_ASSIGN:
        case Java24Lexer::DIV_ASSIGN:
        case Java24Lexer::AND_ASSIGN:
        case Java24Lexer::OR_ASSIGN:
        case Java24Lexer::XOR_ASSIGN:
        case Java24Lexer::MOD_ASSIGN:
        case Java24Lexer::LSHIFT_ASSIGN:
        case Java24Lexer::RSHIFT_ASSIGN:
        case Java24Lexer::URSHIFT_ASSIGN:
            return true;
        default:
            return false;
    }
}

static int32_t effectiveRuleIndex(RuleContext* rule) {
    size_t idx = rule->getRuleIndex();
    if (idx == Java24Parser::RuleExpression && rule->children.size() == 3) {
        if (auto mid = dynamic_cast<tree::TerminalNode*>(rule->children[1])) {
            if (mid->getSymbol() && isAssignmentOperatorToken(
                    static_cast<int32_t>(mid->getSymbol()->getType()))) {
                return SYNTHETIC_ASSIGNMENT_EXPR;
            }
        }
    }
    return static_cast<int32_t>(idx);
}

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
        out.push_back(effectiveRuleIndex(rule));
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
    const int32_t* parse_java24_flat(const char* code, int32_t* out_size) {
        if (out_size) *out_size = 0;
        if (!code) return nullptr;

        try {
            ANTLRInputStream input(code);
            Java24Lexer lexer(&input);
            lexer.removeErrorListeners();
            CommonTokenStream tokens(&lexer);
            Java24Parser parser(&tokens);
            parser.removeErrorListeners();

            tree::ParseTree* parseTree = parser.compilationUnit();
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
