grammar CommandLineGrammar;

// Parser

start
    : command ';'? EOF;

command
    : pipeCommand
    | callCommand
    | seqCommand;

pipeCommand
    : callCommand '|' callCommand
    | pipeCommand '|' callCommand;

callCommand
    : WHITESPACE? (redirection WHITESPACE)* argument (WHITESPACE? atom)* WHITESPACE?;

seqCommand
    : (callCommand | pipeCommand) ';' (callCommand | pipeCommand)
    | (callCommand | pipeCommand) ';' seqCommand;

atom
    : redirection
    | argument;

redirection
    : '<' WHITESPACE? argument
    | '>' WHITESPACE? argument;

argument
    : quoted
    | unquoted;

unquoted
    : (NON_KEYWORD)+;

quoted
    : singleQuoted
    | doubleQuoted
    | backQuoted;

singleQuoted
    : '\'' ~('\n' | '\'')* '\'';

doubleQuoted
    : '"' ( backQuoted | ~( '\n' | '\'' | '"' ))* '"';

backQuoted
    : '`' command '`';

// Lexer


WHITESPACE : [ \t]+ ;
NON_KEYWORD : ~[\n "';<>`|]+;