#pragma once

#include "antlr4-runtime.h"

class Java24ParserBase : public antlr4::Parser {
public:
    Java24ParserBase(antlr4::TokenStream *input) : Parser(input) { }
    bool DoLastRecordComponent();
    bool IsNotIdentifierAssign();
};
