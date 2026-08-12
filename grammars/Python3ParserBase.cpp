#include "Python3ParserBase.h"

using namespace antlr4;

Python3ParserBase::Python3ParserBase(antlr4::TokenStream *input) : Parser(input)
{
	Version = PythonVersion::Autodetect;
}

bool Python3ParserBase::CheckVersion(int version)
{
	return Version == PythonVersion::Autodetect || version == (int) Version;
}

void Python3ParserBase::SetVersion(int requiredVersion)
{
	Version = (PythonVersion) requiredVersion;
}
