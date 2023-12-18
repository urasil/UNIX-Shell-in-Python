from pygments.lexer import RegexLexer
from pygments.token import Token

"""

"""


class CustomCommandLineLexer(RegexLexer):
    tokens = {
        "root": [
            (
                r"(\b(cat|cd|cut|echo|find|grep|head|ls|pwd|sort|tail|uniq)\b)",
                Token.Command,
            ),
            (r"[<>|;]", Token.Operator),
            (r'"[^"]*"', Token.Doublequote),
            (r"'[^']*'", Token.Singlequote),
            (r"`[^`]*`", Token.Backquote),
            (r"\b([^\"'`<|;]+)\b", Token.Unquoted)
        ]
    }
