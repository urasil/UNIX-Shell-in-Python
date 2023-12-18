
import os
import sys
from antlr4 import InputStream, CommonTokenStream
from grammar.CommandLineGrammarLexer import CommandLineGrammarLexer
from grammar.CommandLineGrammarParser import CommandLineGrammarParser
from grammar.ParserErrorListener import ParserErrorListener
from evaluators import Evaluator
from converters import Converter
from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from customLexer import CustomCommandLineLexer


styles = Style.from_dict(
    {
        "pygments.command": "#FFFF00",
        "pygments.operator": "#00FF00",
        "pygments.doublequote": "#FFA500",
        "pygments.singlequote": "#800080",
        "pygments.backquote": "#7ED4FF",
        "pygments.unquoted": "#156fd6",
        'prompt': '#44ff00',
    }
)


"""
Implementing the sytnax highlighting and automatic suggestion features of the shell
"""


history = FileHistory('history.txt')
auto_suggest = AutoSuggestFromHistory()

session = PromptSession(
    lexer=PygmentsLexer(CustomCommandLineLexer),
    style=styles,
    history=history,
    auto_suggest=auto_suggest,
)

"""
Converts the command line into an abstract syntax tree
which is then converted into an object tree to be evaluated
"""


def convert(cmdline):

    input_stream = InputStream(cmdline)
    lexer = CommandLineGrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CommandLineGrammarParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(ParserErrorListener())
    tree = parser.start()
    expression = tree.accept(Converter())
    return expression


"""
Evaluates the object tree starting the from the root object - command
"""


def eval_expression(expression):

    return expression.accept(Evaluator())


if __name__ == "__main__":

    args_num = len(sys.argv) - 1
    if args_num > 0:
        if args_num != 2:
            raise ValueError("wrong number of command line arguments")
        if sys.argv[1] != "-c":
            raise ValueError(f"unexpected command line argument {sys.argv[1]}")
        out = eval_expression(convert(sys.argv[2]))
        if out:
            print(out)
    else:

        """
        The main shell loop
        """
        while True:

            try:
                cmdline = session.prompt(os.getcwd() + "> ")
                expression = convert(cmdline)
                out = eval_expression(expression)
                if out:
                    print(out)
            except Exception as e:
                print(e.__class__.__name__ + ": " + str(e))
                continue
            except KeyboardInterrupt:
                break
