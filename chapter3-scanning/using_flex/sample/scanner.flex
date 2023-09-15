%{
#include "token.h"
%}


DIGIT [0-9]
LETTER [a-zA-Z]


%%
(" "|\t|\n)   /* skip whitespace */
\+            { return TOKEN_ADD; }
while         { return TOKEN_WHILE; }
{LETTER}+    { return TOKEN_IDENT; }
{DIGIT}+     { return TOKEN_NUMBER; }
.             { return TOKEN_ERROR; }
%%

int yywrap() { return 1; }

extern FILE *yyin;
extern int yylex();
extern char *yytext;

int main()
{
        yyin = fopen("program.c", "r");
        if (!yyin)
        {
                printf("Could not open program.c\n");
                return 1;
        }

        while (1)
        {
                token_t t = yylex();

                if (t == TOKEN_EOF)
                      break;

                printf("token: %d text: %s\n", t, yytext);
        }
}
