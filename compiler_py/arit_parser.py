from wrt_log import TraceFile
import errorcpl
# from main import exit_error

"""
asignment -> IDENTIFIER ASGNMOP expr
expr -> term {ADDOP term}
    term -> factor {MULOP factor}
    factor -> IDENTIFIER | NUMBERS | '(' expr ')'
"""


class Parser:
    def __init__(self, code, lexer) -> None:
        self.output=""
        self.token_ctr=0
        self.lexer = lexer
        self.look_ahead=code.splitlines()
        TraceFile.write_log(msg=str(self.look_ahead[self.token_ctr]), fnc="initparser")
        self.token_read= self.gettoken()
        self.parse_token()

    def match(self, expected):
        TraceFile.write_log(msg=str(self.token_read)+" expected["+expected+"]", fnc="match")
        # if self.look_ahead[self.token_ctr]==expected:
        if self.token_read==expected:
            self.token_read = self.gettoken()

    def gettoken(self):
        rsl = self.look_ahead[self.token_ctr]
        self.token_ctr+=1
        return rsl
    
    def parse_token(self):
        TraceFile.write_log(f"self.token_read[{self.token_read}] self.look_ahead[{self.look_ahead[self.token_ctr]}] ","parse_token" )
        if self.token_read == 'IDENTIFIER' and self.look_ahead[self.token_ctr] == 'ASGNMOP':
            self.asignment()
            exit(1)

        elif self.token_read == 'IDENTIFIER' or self.token_read == 'NUMBERS':
            self.expr()
            exit(1)
        else:
            self.output+="parse error"
            print("parse error")
            exit(1)

    # expr -> term {ADDOP term}
    def expr(self):
        print("expr")
        self.output+="expr "
        self.term()
        entry = self.lexer.symtab_lookup(self.token_read)
        if not entry:
            self.output+="Unexpected token" + {self.token_read}
            errorcpl.exit_error(f'Unexpected token {self.token_read}')
        
        while (self.token_read == 'OPERATORS' and entry['CATEGORY'] == 'ADDOP'):
            readop = self.lexer.lex_tape[entry['INDEX']]
            self.match('OPERATORS')
            self.term()
            print(" " + readop)
            self.output+=" " + str(readop)
        return

    # term -> factor {MULOP factor}
    def term(self):
        print("term")
        self.output+="term"
        self.factor()
        entry = self.lexer.symtab_lookup(self.token_read)
        if not entry:
            errorcpl.exit_error(f'Unexpected token {self.token_read}')
        
        while (self.token_read == 'OPERATORS' and entry['CATEGORY'] == 'MULOP'):
            readop = self.lexer.lex_tape[entry['INDEX']]
            self.match('OPERATORS')
            self.factor()
            print(" " + readop)
            self.output+=" " + str(readop)
        return
    
    # factor -> IDENTIFIER | NUMBERS | '(' expr ')'
    def factor(self):
        if self.token_read == 'IDENTIFIER':
            self.match('IDENTIFIER') 
            self.output+="IDENTIFIER"
            print("IDENTIFIER")
        elif self.token_read == 'NUMBERS':
            self.match('NUMBERS')  
            self.output+="NUMBERS"
            print("NUMBERS")
        elif self.token_read == 'OPENING':
            self.match('OPENING')
            self.output+="OPENING "
            self.expr()
            self.match('CLOSING')
            self.output+="CLOSING "
        else:
            self.output+='parse error token:' + str({self.token_read})
            errorcpl.exit_error(f'parse error token: {self.token_read}')
        return
    
    # asignment -> IDENTIFIER ASGNMOP expr
    def asignment(self):
        self.output+="IDENTIFIER"
        self.match('IDENTIFIER')
        self.output+="ASGNMOP"
        self.match('ASGNMOP')
        self.expr()
        print("asignment")
        self.output+="ASSIGNMENT"
        return
    


