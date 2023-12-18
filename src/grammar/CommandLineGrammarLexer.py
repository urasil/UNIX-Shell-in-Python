# Generated from src/grammar/CommandLineGrammar.g4 by ANTLR 4.7.2
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\f")
        buf.write("\61\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t")
        buf.write("\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\3\2\3\2\3\3\3\3\3")
        buf.write("\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\n\6\n")
        buf.write(")\n\n\r\n\16\n*\3\13\6\13.\n\13\r\13\16\13/\2\2\f\3\3")
        buf.write("\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\3\2\4\4\2\13")
        buf.write("\13\"\"\n\2\f\f\"\"$$))=>@@bb~~\2\62\2\3\3\2\2\2\2\5\3")
        buf.write("\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2")
        buf.write("\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2")
        buf.write("\3\27\3\2\2\2\5\31\3\2\2\2\7\33\3\2\2\2\t\35\3\2\2\2\13")
        buf.write("\37\3\2\2\2\r!\3\2\2\2\17#\3\2\2\2\21%\3\2\2\2\23(\3\2")
        buf.write("\2\2\25-\3\2\2\2\27\30\7=\2\2\30\4\3\2\2\2\31\32\7~\2")
        buf.write("\2\32\6\3\2\2\2\33\34\7>\2\2\34\b\3\2\2\2\35\36\7@\2\2")
        buf.write("\36\n\3\2\2\2\37 \7)\2\2 \f\3\2\2\2!\"\7\f\2\2\"\16\3")
        buf.write("\2\2\2#$\7$\2\2$\20\3\2\2\2%&\7b\2\2&\22\3\2\2\2\')\t")
        buf.write("\2\2\2(\'\3\2\2\2)*\3\2\2\2*(\3\2\2\2*+\3\2\2\2+\24\3")
        buf.write("\2\2\2,.\n\3\2\2-,\3\2\2\2./\3\2\2\2/-\3\2\2\2/\60\3\2")
        buf.write("\2\2\60\26\3\2\2\2\5\2*/\2")
        return buf.getvalue()


class CommandLineGrammarLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    WHITESPACE = 9
    NON_KEYWORD = 10

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "';'", "'|'", "'<'", "'>'", "'''", "'\n'", "'\"'", "'`'" ]

    symbolicNames = [ "<INVALID>",
            "WHITESPACE", "NON_KEYWORD" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "WHITESPACE", "NON_KEYWORD" ]

    grammarFileName = "CommandLineGrammar.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


