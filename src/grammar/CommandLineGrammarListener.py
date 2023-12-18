# Generated from CommandLineGrammar.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CommandLineGrammarParser import CommandLineGrammarParser
else:
    from CommandLineGrammarParser import CommandLineGrammarParser

# This class defines a complete listener for a parse tree produced by CommandLineGrammarParser.
class CommandLineGrammarListener(ParseTreeListener):

    # Enter a parse tree produced by CommandLineGrammarParser#start.
    def enterStart(self, ctx:CommandLineGrammarParser.StartContext):
        pass

    # Exit a parse tree produced by CommandLineGrammarParser#start.
    def exitStart(self, ctx:CommandLineGrammarParser.StartContext):
        pass


    # Enter a parse tree produced by CommandLineGrammarParser#command.
    def enterCommand(self, ctx:CommandLineGrammarParser.CommandContext):
        pass

    # Exit a parse tree produced by CommandLineGrammarParser#command.
    def exitCommand(self, ctx:CommandLineGrammarParser.CommandContext):
        pass


    # Enter a parse tree produced by CommandLineGrammarParser#pipeCommand.
    def enterPipeCommand(self, ctx:CommandLineGrammarParser.PipeCommandContext):
        pass

    # Exit a parse tree produced by CommandLineGrammarParser#pipeCommand.
    def exitPipeCommand(self, ctx:CommandLineGrammarParser.PipeCommandContext):
        pass


    # Enter a parse tree produced by CommandLineGrammarParser#callCommand.
    def enterCallCommand(self, ctx:CommandLineGrammarParser.CallCommandContext):
        pass

    # Exit a parse tree produced by CommandLineGrammarParser#callCommand.
    def exitCallCommand(self, ctx:CommandLineGrammarParser.CallCommandContext):
        pass


    # Enter a parse tree produced by CommandLineGrammarParser#seqCommand.
    def enterSeqCommand(self, ctx:CommandLineGrammarParser.SeqCommandContext):
        pass

    # Exit a parse tree produced by CommandLineGrammarParser#seqCommand.
    def exitSeqCommand(self, ctx:CommandLineGrammarParser.SeqCommandContext):
        pass


    # Enter a parse tree produced by CommandLineGrammarParser#atom.
    def enterAtom(self, ctx:CommandLineGrammarParser.AtomContext):
        pass

    # Exit a parse tree produced by CommandLineGrammarParser#atom.
    def exitAtom(self, ctx:CommandLineGrammarParser.AtomContext):
        pass


    # Enter a parse tree produced by CommandLineGrammarParser#redirection.
    def enterRedirection(self, ctx:CommandLineGrammarParser.RedirectionContext):
        pass

    # Exit a parse tree produced by CommandLineGrammarParser#redirection.
    def exitRedirection(self, ctx:CommandLineGrammarParser.RedirectionContext):
        pass


    # Enter a parse tree produced by CommandLineGrammarParser#argument.
    def enterArgument(self, ctx:CommandLineGrammarParser.ArgumentContext):
        pass

    # Exit a parse tree produced by CommandLineGrammarParser#argument.
    def exitArgument(self, ctx:CommandLineGrammarParser.ArgumentContext):
        pass


    # Enter a parse tree produced by CommandLineGrammarParser#unquoted.
    def enterUnquoted(self, ctx:CommandLineGrammarParser.UnquotedContext):
        pass

    # Exit a parse tree produced by CommandLineGrammarParser#unquoted.
    def exitUnquoted(self, ctx:CommandLineGrammarParser.UnquotedContext):
        pass


    # Enter a parse tree produced by CommandLineGrammarParser#quoted.
    def enterQuoted(self, ctx:CommandLineGrammarParser.QuotedContext):
        pass

    # Exit a parse tree produced by CommandLineGrammarParser#quoted.
    def exitQuoted(self, ctx:CommandLineGrammarParser.QuotedContext):
        pass


    # Enter a parse tree produced by CommandLineGrammarParser#singleQuoted.
    def enterSingleQuoted(self, ctx:CommandLineGrammarParser.SingleQuotedContext):
        pass

    # Exit a parse tree produced by CommandLineGrammarParser#singleQuoted.
    def exitSingleQuoted(self, ctx:CommandLineGrammarParser.SingleQuotedContext):
        pass


    # Enter a parse tree produced by CommandLineGrammarParser#doubleQuoted.
    def enterDoubleQuoted(self, ctx:CommandLineGrammarParser.DoubleQuotedContext):
        pass

    # Exit a parse tree produced by CommandLineGrammarParser#doubleQuoted.
    def exitDoubleQuoted(self, ctx:CommandLineGrammarParser.DoubleQuotedContext):
        pass


    # Enter a parse tree produced by CommandLineGrammarParser#backQuoted.
    def enterBackQuoted(self, ctx:CommandLineGrammarParser.BackQuotedContext):
        pass

    # Exit a parse tree produced by CommandLineGrammarParser#backQuoted.
    def exitBackQuoted(self, ctx:CommandLineGrammarParser.BackQuotedContext):
        pass


