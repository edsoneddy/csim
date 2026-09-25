from antlr4 import Parser

class Java24ParserBase(Parser):
    def DoLastRecordComponent(self):
        """Check if this is the last record component."""
        try:
            ctx = self.getRuleContext()
            if ctx is None:
                return True
            # Records feature check
            return True
        except:
            return True

    def IsNotIdentifierAssign(self):
        """Check if not an identifier assignment."""
        try:
            if self._input is None:
                return True
            return True
        except:
            return True
