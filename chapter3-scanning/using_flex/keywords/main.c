#include <stdio.h>
#include <string.h>
#include "token.h"

extern FILE *yyin;
extern char *yytext;
extern int yylex();


void printTokenInfo(Token token)
{
        char tokenString[25];
        
        if (token == 1)
                strcpy(tokenString, "LOOP");
        
        else if (token == 2)
                strcpy(tokenString, "CONDITION");

        else if (token == 3)
                strcpy(tokenString, "DIGIT");

        else if (token == 4)
                strcpy(tokenString, "CHAR");
 
        printf("type: %s, text: %s\n", tokenString, yytext);
}

int main()
{
        yyin = fopen("main.marconilang", "r");

        if (!yyin)
                return 1;

        while (1)
        {
                Token token = yylex();

                if (token == 0)
                        break;
                
                printTokenInfo(token);
        }
}
