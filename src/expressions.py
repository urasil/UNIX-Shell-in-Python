"""
Base abstract class for all expression classes
"""


class Expression:
    pass


"""
Represents a command in the abstract syntax tree as a Command object
"""


class Command(Expression):

    def __init__(self, cmd):

        self.cmd = cmd

    def accept(self, visitor):

        return visitor.visitCommand(self)


"""
Represents a command in the abstract syntax tree as a Command object
"""


class CallCommand(Expression):

    def __init__(self, *args):

        self.app = None
        if isinstance(args[0], Argument):
            self.app = args[0]
            self.args = [arg for arg in args[1:]]

        elif isinstance(args[0], Redirection):
            self.app = args[1]
            self.args = [args[0]] + [arg for arg in args[2:]]

    def accept(self, visitor):

        return visitor.visitCallCommand(self)


"""
Represents a pipe command in the abstract syntax tree as a PipeCommand object
"""


class PipeCommand(Expression):

    def __init__(self, left, right):

        self.cmd1 = left
        self.cmd2 = right

    def accept(self, visitor):

        return visitor.visitPipeCommand(self)


"""
Represents a sequence command in the abstract syntax tree as a SeqCommand object
"""


class SeqCommand(Expression):

    def __init__(self, left, right):

        self.cmd1 = left
        self.cmd2 = right

    def accept(self, visitor):

        tmp = visitor.visitSeqCommand(self)
        return tmp


"""
Represents an argument in the abstract syntax tree as an Argument object
"""


class Argument(Expression):

    def __init__(self, node):

        self.node = node

    def accept(self, visitor):

        return visitor.visitArgument(self)


"""
Represents an atom in the abstract syntax tree as an Atom object
"""


class Atom:

    def __init__(self, node):

        self.node = node

    def accept(self, visitor):

        return visitor.visitAtom(self)


"""
Represents a redirection in the abstract syntax tree as a Redirection object
"""


class Redirection:

    def __init__(self, type, args):

        self.type = type
        self.args = args

    def accept(self, visitor):

        return visitor.visitRedirection(self)


"""
Represents an unquoted text in the abstract syntax tree as an Unquoted object
"""


class Unquoted:

    def __init__(self, value):

        self.value = value

    def accept(self, visitor):

        return visitor.visitUnquoted(self)


"""
Represents a quoted text in the abstract syntax tree as a Quoted object
"""


class Quoted:

    def __init__(self, node):

        self.node = node

    def accept(self, visitor):

        return visitor.visitQuoted(self)


"""
Represents a single quoted text in the abstract syntax tree as a SingleQuoted object
"""


class SingleQuoted:

    def __init__(self, value):

        self.value = value

    def accept(self, visitor):

        return visitor.visitSingleQuoted(self)


"""
Represents a double quoted text in the abstract syntax tree as a DoubleQuoted object
"""


class DoubleQuoted:

    def __init__(self, value):

        self.value = value

    def accept(self, visitor):

        return visitor.visitDoubleQuoted(self)


"""
Represents a back quoted text in the abstract syntax tree as a BackQuoted object
"""


class BackQuoted:

    def __init__(self, node):

        self.node = node

    def accept(self, visitor):

        return visitor.visitBackQuoted(self)
