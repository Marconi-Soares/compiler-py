%{
        int number_of_lines;
        int number_of_chars;
%}


%%
\n {
        ++number_of_lines;
}

. {
        ++number_of_chars;
}
%%


int yywrap(){}
int main (int argc, char **argv)
{
        yylex();
        printf("number of lines = %d,\nnumber of chars = %d", 
                number_of_lines, number_of_chars);
}
