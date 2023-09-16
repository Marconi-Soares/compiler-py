#include <stdio.h>
#include "token.h"

#define true 1

int main()
{
        int yylex();
        extern char *yytext;

        extern FILE *yyin; 
        yyin = fopen("program", "r");

        if (!yyin)
        {
                printf("Could not open program!\n");
                return 1;
        }

        while (true)
        {
                token_t token = yylex();

                if (token == TOKEN_EOF)
                        break;
                
                printf("token: %d text: %s\n", token, yytext);
        }

}
