/**
 * Python 3 Parser Bridge - flat binary emitter.
 *
 * Flat preorder int32 buffer format (same as java_24_bridge.cpp, cpp_14_bridge.cpp):
 *
 *     [count, (label, numChildren) * count]
 *
 * Label encoding:
 *   - rule nodes      -> ruleIndex, EXCEPT import-shaped `small_stmt` nodes
 *                        (see effectiveRuleIndex() below)
 *   - terminal tokens -> TERMINAL_BASE + tokenType + 1
 *
 * Uses grammars-v4/python/python grammar (the "universal Python 2/3" grammar,
 * optimized lexer, C++ target published upstream). Entry rule is
 * `file_input`, matching python_3_13's convention.
 *
 * Known gap vs python_3_13: this grammar does not parse positional-only
 * parameters (PEP 570, '/' in a def), the walrus operator (':=' , PEP 572),
 * or match/case (PEP 634) -- csim/native/loader.py falls back to the
 * pure-Python python_3_13 parser automatically when native parsing fails,
 * so this only costs speed on files using those constructs, not correctness.
 */

#include "Python3Lexer.h"
#include "Python3Parser.h"
#include <antlr4-runtime.h>
#include <vector>
#include <cstdint>

using namespace antlr4;

static const int32_t TERMINAL_BASE = 1000000;

// Must match the SYNTHETIC_* constants in csim/python_3/utils.py.
static const int32_t SYNTHETIC_IMPORT_STMT = 200;
static const int32_t SYNTHETIC_TRY_STMT = 201;
static const int32_t SYNTHETIC_IF_STMT = 202;
static const int32_t SYNTHETIC_WHILE_STMT = 203;
static const int32_t SYNTHETIC_FOR_STMT = 204;
static const int32_t SYNTHETIC_WITH_STMT = 205;
static const int32_t SYNTHETIC_CLASS_OR_FUNC_STMT = 206;

/**
 * Hub-rule alternatives that need a rule identity different from the rest
 * of their shared rule index. Mirrors relabel_node() in
 * csim/python_3/utils.py exactly; keep both in sync.
 *
 * `small_stmt`: IMPORT dotted_as_names (#import_stmt) and FROM ... IMPORT
 * ... (#from_stmt) share RuleSmall_stmt with every other simple-statement
 * kind. HASHED_RULE_INDICES hashes small_stmt wholesale for tree size,
 * which would make "import sys" and "from sys import stdin" hash
 * differently; python_3_13 instead collapses its import machinery to a
 * content-free marker.
 *
 * `compound_stmt`'s six labeled alternatives (#if_stmt, #while_stmt,
 * #for_stmt, #with_stmt, #try_stmt, #class_or_func_def_stmt) all share
 * RuleCompound_stmt. Hashing compound_stmt directly would make
 * distance_metrics.py's label_distance() treat a `for`-vs-`while` swap as
 * "same rule, different hash" (0.5 cost) instead of the 1.0 cost
 * python_3_13 assigns (separate, unshared rules there) -- under-penalizing
 * a real control-flow difference. Giving each alternative its own synthetic
 * id restores that distinction. try_stmt routes to EXCLUDED_RULE_TYPES (not
 * hashed) per the separate try/except fix; the rest route to
 * HASHED_RULE_INDICES.
 */
static int32_t effectiveRuleIndex(RuleContext* rule) {
    size_t idx = rule->getRuleIndex();
    if (rule->children.empty()) return static_cast<int32_t>(idx);

    if (idx == Python3Parser::RuleSmall_stmt) {
        auto first = dynamic_cast<tree::TerminalNode*>(rule->children[0]);
        if (first && first->getSymbol()) {
            auto tt = first->getSymbol()->getType();
            if (tt == Python3Lexer::IMPORT || tt == Python3Lexer::FROM) {
                return SYNTHETIC_IMPORT_STMT;
            }
        }
        return static_cast<int32_t>(idx);
    }

    if (idx == Python3Parser::RuleCompound_stmt) {
        // if/while/try always start with their keyword; for/with may be
        // preceded by ASYNC; class_or_func_def_stmt has no leading keyword
        // token -- detected via a classdef/funcdef child instead (skipping
        // any leading decorator children).
        for (auto* child : rule->children) {
            if (auto term = dynamic_cast<tree::TerminalNode*>(child)) {
                if (!term->getSymbol()) break;
                auto tt = term->getSymbol()->getType();
                if (tt == Python3Lexer::IF) return SYNTHETIC_IF_STMT;
                if (tt == Python3Lexer::WHILE) return SYNTHETIC_WHILE_STMT;
                if (tt == Python3Lexer::FOR) return SYNTHETIC_FOR_STMT;
                if (tt == Python3Lexer::WITH) return SYNTHETIC_WITH_STMT;
                if (tt == Python3Lexer::TRY) return SYNTHETIC_TRY_STMT;
                if (tt == Python3Lexer::ASYNC) continue;
                break;
            } else if (auto childRule = dynamic_cast<RuleContext*>(child)) {
                size_t cidx = childRule->getRuleIndex();
                if (cidx == Python3Parser::RuleClassdef || cidx == Python3Parser::RuleFuncdef) {
                    return SYNTHETIC_CLASS_OR_FUNC_STMT;
                }
                if (cidx == Python3Parser::RuleDecorator) continue;
                break;
            }
        }
        return static_cast<int32_t>(idx);
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
     * Parse Python source and emit the flat tree buffer.
     *
     * @param code      UTF-8 source
     * @param out_size  receives the number of int32 elements in the buffer
     * @return pointer to the buffer, or nullptr on error. Caller must not free.
     */
    const int32_t* parse_python3_flat(const char* code, int32_t* out_size) {
        if (out_size) *out_size = 0;
        if (!code) return nullptr;

        try {
            ANTLRInputStream input(code);
            Python3Lexer lexer(&input);
            lexer.removeErrorListeners();
            CommonTokenStream tokens(&lexer);
            Python3Parser parser(&tokens);
            parser.removeErrorListeners();

            tree::ParseTree* parseTree = parser.file_input();
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
