from wrt_log import write_log

"""
expr -> term {ADDOP term}
term -> term {factor MULOP factor}
factor -> IDENTIFIER | NUMBERS | '(' expr ')'
asignment -> IDENTIFIER ASGNMOP expr
"""

class Parser:
    def __init__(self, code, lexer) -> None:
        self.token_ctr=0
        self.look_ahead=""
        self.token_read=""
        self.look_ahead=code.splitlines()
        self.token_read = self.gettoken()
        self.parse_token()

    def gettoken(self):
        self.token_read = self.look_ahead[self.token_ctr]
        self.token_ctr+=1
    
    def parse_token(self):
        write_log(f"self.token_read[{self.token_read}] self.look_ahead[{self.look_ahead[self.token_ctr]}] ","parse_token" )
        if self.token_read == 'IDENTIFIER' and self.look_ahead[self.token_ctr] == 'ASGNMOP':
            self.asignment()
            exit(1)

        elif self.token_read == 'IDENTIFIER' or self.token_read == 'NUMBERS':
            self.expr()
            exit(1)
        else:
            print("parse error")
            exit(1)

    # expr -> term {ADDOP term}
    def expr(self):
        print("expr")
        self.term()
        while (self.token_read == 'OPERATORS'):
            readop = self.token_read
            self.term()
            print(" " + readop)

    # term -> term {factor MULOP factor}
    def term(self):
        print("term")
        return
    
    # factor -> IDENTIFIER | NUMBERS | '(' expr ')'
    def factor(self):
        print("factor")
        return
    
    # asignment -> IDENTIFIER ASGNMOP expr
    def asignment(self):
        print("asignment")
        return
    

