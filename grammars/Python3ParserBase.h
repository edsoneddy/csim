#pragma once

#include "antlr4-runtime.h"

class Python3ParserBase : public antlr4::Parser {
	public:
		enum PythonVersion
		{
			Autodetect,
			Python2 = 2,
			Python3 = 3
		};
		Python3ParserBase(antlr4::TokenStream *input);
		bool CheckVersion(int version);
		void SetVersion(int requiredVersion);
		int Version;
};
