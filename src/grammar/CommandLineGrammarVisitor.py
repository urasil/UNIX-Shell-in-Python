# Generated from src/grammar/CommandLineGrammar.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CommandLineGrammarParser import CommandLineGrammarParser
else:
    from CommandLineGrammarParser import CommandLineGrammarParser

# This class defines a complete generic visitor for a parse tree produced by CommandLineGrammarParser.

class CommandLineGrammarVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CommandLineGrammarParser#start.
    def visitStart(self, ctx:CommandLineGrammarParser.StartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandLineGrammarParser#command.
    def visitCommand(self, ctx:CommandLineGrammarParser.CommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandLineGrammarParser#pipeCommand.
    def visitPipeCommand(self, ctx:CommandLineGrammarParser.PipeCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandLineGrammarParser#callCommand.
    def visitCallCommand(self, ctx:CommandLineGrammarParser.CallCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandLineGrammarParser#seqCommand.
    def visitSeqCommand(self, ctx:CommandLineGrammarParser.SeqCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandLineGrammarParser#atom.
    def visitAtom(self, ctx:CommandLineGrammarParser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandLineGrammarParser#redirection.
    def visitRedirection(self, ctx:CommandLineGrammarParser.RedirectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandLineGrammarParser#argument.
    def visitArgument(self, ctx:CommandLineGrammarParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandLineGrammarParser#unquoted.
    def visitUnquoted(self, ctx:CommandLineGrammarParser.UnquotedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandLineGrammarParser#quoted.
    def visitQuoted(self, ctx:CommandLineGrammarParser.QuotedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandLineGrammarParser#singleQuoted.
    def visitSingleQuoted(self, ctx:CommandLineGrammarParser.SingleQuotedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandLineGrammarParser#doubleQuoted.
    def visitDoubleQuoted(self, ctx:CommandLineGrammarParser.DoubleQuotedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CommandLineGrammarParser#backQuoted.
    def visitBackQuoted(self, ctx:CommandLineGrammarParser.BackQuotedContext):
        return self.visitChildren(ctx)



del CommandLineGrammarParser