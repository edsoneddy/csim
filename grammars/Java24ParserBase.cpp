#include "Java24Parser.h"

using namespace antlr4;

bool Java24ParserBase::DoLastRecordComponent()
{
    auto ctx = this->getRuleContext();
    auto tctx = dynamic_cast<Java24Parser::RecordComponentListContext*>(ctx);
    if (tctx == nullptr) return true;
    auto rcs = tctx->recordComponent();
    if (rcs.empty()) return true;
    int count = rcs.size();
    for (int c = 0; c < count; ++c)
    {
        if (rcs[c]->ELLIPSIS() != nullptr && c + 1 < count)
            return false;
    }
    return true;
}

bool Java24ParserBase::IsNotIdentifierAssign()
{
    auto la = this->_input->LA(1);
    switch (la) {
        case Java24Parser::IDENTIFIER:
        case Java24Parser::MODULE:
        case Java24Parser::OPEN:
        case Java24Parser::REQUIRES:
        case Java24Parser::EXPORTS:
        case Java24Parser::OPENS:
        case Java24Parser::TO:
        case Java24Parser::USES:
        case Java24Parser::PROVIDES:
        case Java24Parser::WHEN:
        case Java24Parser::WITH:
        case Java24Parser::TRANSITIVE:
        case Java24Parser::YIELD:
        case Java24Parser::SEALED:
        case Java24Parser::PERMITS:
        case Java24Parser::RECORD:
        case Java24Parser::VAR:
            break;
        default:
            return true;
    }
    auto la2 = this->_input->LA(2);
    if (la2 != Java24Parser::ASSIGN) return true;
    return false;
}
