%{
#include "token.h"
%}

LOOP_KEYWORD (while|for)
CONDITION_KEYWORD (if|else)
LETTERS [a-zA-Z]
DIGITS [0-9]

%%
(" "|\t|\n) /* IGNORE */
{LOOP_KEYWORD} { return TOKEN_LOOP_KEYWORD; }
{CONDITION_KEYWORD} { return TOKEN_CONDITION_KEYWORD; }
{LETTERS}+ { return TOKEN_CHAR; }
{DIGITS}+ { return TOKEN_DIGIT; }
.       { return TOKEN_ERROR; }
%%

int yywrap() {}
