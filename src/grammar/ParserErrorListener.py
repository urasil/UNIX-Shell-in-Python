from antlr4.error.ErrorListener import ErrorListener


class ParserErrorListener(ErrorListener):

    def __init__(self):
        super(ParserErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxError(f"unexpected token {offendingSymbol.text}")
