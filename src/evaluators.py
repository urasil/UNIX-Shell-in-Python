from grammar.CommandLineGrammarVisitor import CommandLineGrammarVisitor
from applications.appFactory import Application

"""
The evalutor class that will take the output of the object tree
created by the converter and evaluate it

Each node in the object tree will be evaluated by the visitor pattern

Visitor pattern: The accpet method of each object (defined in respective expression class)
will call the visit method of the visitor class
"""


class Evaluator(CommandLineGrammarVisitor):

    """
    Initializing variables for the
    implementation of the pipe command and output redirection
    """

    def __init__(self) -> None:

        self.pipe = None
        self.stdout = None
        self.outRedirection = None

    """
    Evaluates the command by calling the
    accept method of its child in the object tree
    """

    def visitCommand(self, command):

        return command.cmd.accept(self)

    """
    Evaluates call commands by creating theapplication object
    which executes the application and returns the output
    Output redirection is handled here since the output of
    the application is required to write to a file
    """

    def visitCallCommand(self, call):

        app = call.app.accept(self)
        args = []
        for arg in call.args:
            if app == "echo":
                if arg is None:
                    if len(args) == 0:
                        args.append(" ")
                    else:
                        args[len(args) - 1] += " "
                else:
                    tmp = arg.accept(self)
                    if len(args) > 0:
                        if tmp is not None:
                            args[len(args) - 1] += tmp
                    else:
                        args.append(arg.accept(self))
            else:
                if arg is not None:
                    tmp = arg.accept(self)
                    if tmp is not None:  # for output redirection
                        args.append(tmp)
        self.stdout = Application(app, args, self.pipe).applicationMap()
        if self.outRedirection:
            with open(self.outRedirection, 'w') as f:
                f.write(self.stdout)
            self.outRedirection = None
            return ""

        return self.stdout

    """
    Evaluates sequence commands by evaluating
    left then right command respectively
    """

    def visitSeqCommand(self, seq):

        res = ""
        out = []
        out.append(seq.cmd1.accept(self))
        out.append(seq.cmd2.accept(self))
        for elem in out:
            if elem is not None:
                res += elem.rstrip("\n") + "\n"
        return res

    """
    Evaluates the left call command first and passes
    the output to the variable defined for pipe command
    at initilization

    That variable is used by the second call command evaluate to an output
    """

    def visitPipeCommand(self, pipe):

        self.pipe = pipe.cmd1.accept(self)
        return pipe.cmd2.accept(self)

    """
    Evaluates atom by calling the accept method of
    its child which pushes to evaluation down to argument or redirection
    """

    def visitAtom(self, atom):

        return atom.node.accept(self)

    """
    Evaluates the argument by calling the accept method
    of its child which pushes to evaluation down to unquoted or quoted
    """

    def visitArgument(self, arg):

        return arg.node.accept(self)

    """
    Evaluates redirection according type of redirection

    If output redirection, an initialized variable for output
    redirection is set to to be evaluated at call

    If input redirection, the input is read from the file and
    passed as an argument to the application at call command
    """

    def visitRedirection(self, redirection):

        if redirection.type == '>':
            self.outRedirection = redirection.args.accept(self)
            return
        elif redirection.type == '<':
            return redirection.args.accept(self)

    """
    Evalautes quoted by calling the accept method of its
    child which pushes to evaluation down to single, double or back quoted
    """

    def visitQuoted(self, quoted):

        return quoted.node.accept(self)

    """
    Evaluates unquoted by returning the text
    """

    def visitUnquoted(self, unquoted):

        return unquoted.value

    """
    Evaluates single quoted by returning the text between the single quotes
    """

    def visitSingleQuoted(self, singleQuoted):

        return singleQuoted.value

    """
    Evaluates double quoted by returning the text between the double quotes
    """

    def visitDoubleQuoted(self, doubleQuoted):

        return doubleQuoted.value

    """
    Evaluates back quoted by returning the result of the command between the back quotes
    """

    def visitBackQuoted(self, backQuoted):

        return backQuoted.node.accept(self).replace("\n", " ")[:-1]
