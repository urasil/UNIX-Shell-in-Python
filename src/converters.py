from grammar.CommandLineGrammarVisitor import CommandLineGrammarVisitor
from grammar.CommandLineGrammarParser import CommandLineGrammarParser as CLGP
from evaluators import Evaluator
from expressions import (
    Command,
    CallCommand,
    PipeCommand,
    SeqCommand,
    Argument,
    Atom,
    Redirection,
    Unquoted,
    Quoted,
    SingleQuoted,
    DoubleQuoted,
    BackQuoted
)

"""
Converter class converts the abstract syntax tree created by
Antlr4 into a tree that can be used by the evaluator

Each node in the tree will be created into an expression
as the above example - each node will be its own class

Each expression (node class) will then be evaluated by
the evaluator to produce the output
"""


class Converter(CommandLineGrammarVisitor):

    """
    Starting point of the abstract syntax tree created by Antlr4 -
    has one child, which is Command
    """

    def visitStart(self, ctx: CLGP.StartContext):

        return self.visitCommand(ctx.command())

    """
    Command can only become CallCommand, PipeCommand, or SeqCommand
    """

    def visitCommand(self, ctx: CLGP.CommandContext):

        return Command(self.visit(ctx.getChild(0)))

    """
    Example AST:

    Command(
        PipeCommand(
            CallCommand(
                Argument(
                    Unquoted("cat")
                ),
                Argument(
                    Unquoted("foo")
                )
            ),
            CallCommand(
                Argument(
                    Unquoted("tail")
                )
            )
        )
    )

    PipeCommand has either two CallCommands or one PipeCommand and one CallCommand
    """

    def visitPipeCommand(self, ctx: CLGP.PipeCommandContext):

        if ctx.callCommand(0) and ctx.callCommand(1):
            return PipeCommand(self.visitCallCommand(ctx.callCommand(0)),
                               self.visitCallCommand(ctx.callCommand(1)))
        elif ctx.pipeCommand() and ctx.callCommand(0):
            return PipeCommand(self.visitPipeCommand(ctx.pipeCommand()),
                               self.visitCallCommand(ctx.callCommand(0)))

    """
    Example AST:

    Command(
        CallCommand(
            Argument(
                Unquoted("echo")
            ),
            Atom(
                Redirection(
                    ">",
                    Argument(
                        Unquoted("foo")
                    )
                )
            )
        )
    )
    CallCommand has arguments, atoms and redirections as children
    """

    def visitCallCommand(self, ctx: CLGP.CallCommandContext):

        expression = []
        firstAtom = False

        for child in ctx.children:
            if isinstance(child, CLGP.ArgumentContext):
                expression.append(self.visitArgument(child))
            elif isinstance(child, CLGP.RedirectionContext):
                expression.append(self.visitRedirection(child))
            elif isinstance(child, CLGP.AtomContext):
                firstAtom = True
                expression.append(self.visitAtom(child))
            elif firstAtom and (not isinstance(child, CLGP.AtomContext) or
                                not isinstance(child, CLGP.ArgumentContext) or
                                not isinstance(child, CLGP.RedirectionContext)
                                ):
                expression.append(None)
        return CallCommand(*expression)

    """
    Example AST:

    Command(
        SeqCommand(
            CallCommand(
                Argument(
                    Unquoted("echo")
                ),
                Argument(
                    Unquoted("foo")
                )
            ),
            CallCommand(
                Argument(
                    Unquoted("echo")
                ),
                Argument(
                    Unquoted("foo")
                )
            )
        )
    )

    SeqCommand can have CallCommand, PipeCommand as
    its left child and CallCommand, PipeCommand, SeqCommand as its right child
    """

    def visitSeqCommand(self, ctx: CLGP.SeqCommandContext):

        left = ctx.getChild(0)
        right = ctx.getChild(2)
        if (isinstance(left, CLGP.CallCommandContext) and
                isinstance(right, CLGP.CallCommandContext)):

            return SeqCommand(self.visitCallCommand(left),
                              self.visitCallCommand(right))

        elif (isinstance(left, CLGP.CallCommandContext) and
                isinstance(right, CLGP.PipeCommandContext)):

            return SeqCommand(self.visitCallCommand(left),
                              self.visitPipeCommand(right))

        elif (isinstance(left, CLGP.PipeCommandContext) and
                isinstance(right, CLGP.CallCommandContext)):

            return SeqCommand(self.visitPipeCommand(left),
                              self.visitCallCommand(right))

        elif (isinstance(left, CLGP.PipeCommandContext) and
                isinstance(right, CLGP.PipeCommandContext)):

            return SeqCommand(self.visitPipeCommand(left),
                              self.visitPipeCommand(right))

        elif (isinstance(left, CLGP.CallCommandContext) and
                isinstance(right, CLGP.SeqCommandContext)):

            return SeqCommand(self.visitCallCommand(left),
                              self.visitSeqCommand(right))

        elif (isinstance(left, CLGP.PipeCommandContext) and
                isinstance(right, CLGP.SeqCommandContext)):

            return SeqCommand(self.visitPipeCommand(left),
                              self.visitSeqCommand(right))

    """
    Atom can be a redirection or argument
    """

    def visitAtom(self, ctx: CLGP.AtomContext):

        if ctx.argument():
            return Atom(self.visitArgument(ctx.argument()))
        elif ctx.redirection():
            return Atom(self.visitRedirection(ctx.redirection()))

    """
    Redirection handle the input of args from a file or output of result to a file

    Output redirection won't output to standard output but only to the file
    """

    def visitRedirection(self, ctx: CLGP.RedirectionContext):

        if ctx.getChild(0).getText() == '>':
            return Redirection('>', self.visitArgument(ctx.argument()))
        elif ctx.getChild(0).getText() == '<':
            return Redirection('<', self.visitArgument(ctx.argument()))

    """
    Argument is text that is quoted or unquoted
    """

    def visitArgument(self, ctx: CLGP.ArgumentContext):

        args = [self.visit(arg) for arg in ctx.getChildren()]
        return Argument(*args)

    """
    Unquoted returns the text as it is
    """

    def visitUnquoted(self, ctx: CLGP.UnquotedContext):

        return Unquoted(ctx.getText())

    """
    Quoted can be single, double or back quoted,
    which will be handled by their respective functions
    """

    def visitQuoted(self, ctx: CLGP.QuotedContext):

        if ctx.singleQuoted():
            return Quoted(self.visitSingleQuoted(ctx.singleQuoted()))
        elif ctx.doubleQuoted():
            return Quoted(self.visitDoubleQuoted(ctx.doubleQuoted()))
        elif ctx.backQuoted():
            return Quoted(self.visitBackQuoted(ctx.backQuoted()))

    """
    SingleQuoted returns the text as it is - doesn't have command substitution
    """

    def visitSingleQuoted(self, ctx: CLGP.SingleQuotedContext):

        return SingleQuoted(ctx.getText()[1:-1])

    """
    DoubleQuoted returns the text as it is without the double quotes -
    can have command substitution if there is doublequotes within
    """

    def visitDoubleQuoted(self, ctx: CLGP.DoubleQuotedContext):

        text = ctx.getText()[1:-1]

        for child in ctx.getChildren():
            if isinstance(child, CLGP.BackQuotedContext):
                out = self.visitBackQuoted(child).accept(Evaluator())
                text = text.replace(f"`{child.getText()[1:-1]}`", out)
        return DoubleQuoted(text)

    """
    BackQuoted is used for command substitution
    """

    def visitBackQuoted(self, ctx: CLGP.BackQuotedContext):

        if ctx.command():
            return BackQuoted(self.visitCommand(ctx.command()))
