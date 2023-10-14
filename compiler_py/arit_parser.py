from keywords import KEYWORDS
from tokens import TOKENS
from wrt_log import TraceFile
import errorcpl
# from main import exit_error

"""
program -> BEGINPRG stmtlist ENDPRG
stmtlist -> stmt { stmt }
stmt -> asignment | expr
asignment -> IDENTIFIER ASGNMOP expr
expr -> term {ADDOP term}
    term -> factor {MULOP factor}
    factor -> IDENTIFIER | NUMBERS | '(' expr ')'
"""


class Parser:
    def __init__(self, lexer) -> None:
        self.output=""
        self.token_ctr=0
        self.lexer = lexer
        # self.lexer.look_ahead=code.splitlines()
        # TraceFile.write_log(msg=str(self.lexer.look_ahead[self.token_ctr]), fnc="initparser")

    # def match(self, expected):
    #     TraceFile.write_log(msg=str(self.token_read)+" expected["+expected+"]", fnc="match")
    #     # if self.lexer.look_ahead[self.token_ctr]==expected:
    #     if self.token_read==expected:
    #         if self.token_read != "ENDPRG":
    #             self.token_read = self.gettoken()
    #         else:
    #             return
                

    # def gettoken(self):
    #     rsl = self.lexer.look_ahead[self.token_ctr]
    #     self.token_ctr+=1
    #     return rsl

    # expr -> term {ADDOP term}
    def expr(self):
        print("expr")
        self.output+="expr "
        self.term()
        # entry = self.lexer.symtab_lookup(self.token_read, 'ADDOP')
        # if not entry:
        #     self.output+="Unexpected token" + {self.token_read}
        #     errorcpl.exit_error(f'Unexpected token {self.token_read}')
        # 
        # while (self.token_read == 'OPERATORS' and entry['TYPE'] == 'ADDOP'):
        #     readop = self.lexer.lex_tape[entry['INDEX']]
        #     self.lexer.match('OPERATORS')
        #     self.term()
        #     print(" " + readop)
        #     self.output+=" " + str(readop)
        # return

    # term -> factor {MULOP factor}
    def term(self):
        print("term")
        self.output+="term"
        self.factor()
        # entry = self.lexer.symtab_lookup(self.token_read, 'MULOP')
        # if not entry:
        #     errorcpl.exit_error(f'Unexpected token {self.token_read}')
        # 
        # while (self.token_read == 'OPERATORS' and entry['TYPE'] == 'MULOP'):
        #     readop = self.lexer.lex_tape[entry['INDEX']]
        #     self.lexer.match('OPERATORS')
        #     self.factor()
        #     print(" " + readop)
        #     self.output+=" " + str(readop)
        # return
    
    # factor -> IDENTIFIER | NUMBERS | '(' expr ')'
    def factor(self):
        if self.lexer.look_ahead == KEYWORDS['INT']:
                self.lexer.match('INT')

        elif self.lexer.look_ahead == KEYWORDS['FLOAT']:
                self.lexer.match('FLOAT')

        elif self.lexer.look_ahead == TOKENS['ID']:
                self.lexer.match('ID')

        # case KEYWORDS['FLOAT']:
        #     self.lexer.match('FLOAT')

            # case KEYWORDS['ID']:
            #     self.lexer.match('ID')
        #    

        # if self.token_read == 'IDENTIFIER':
        #     self.lexer.match('IDENTIFIER') 
        #     self.output+="IDENTIFIER"
        #     print("IDENTIFIER")
        # elif self.token_read == 'NUMBERS':
        #     self.lexer.match('NUMBERS')  
        #     self.output+="NUMBERS"
        #     print("NUMBERS")
        # elif self.token_read == 'OPENING':
        #     self.lexer.match('OPENING')
        #     self.output+="OPENING "
        #     self.expr()
        #     self.lexer.match('CLOSING')
        #     self.output+="CLOSING "
        # else:
        #     self.output+='parse error token:' + str({self.token_read})
        #     errorcpl.exit_error(f'parse error token: {self.token_read}')
        # return

    def stmt(self):
        if self.lexer.look_ahead == TOKENS['ID']:
            self.asignment()

        # if self.token_read == 'IDENTIFIER' and self.lexer.look_ahead[self.token_ctr] == 'ASGNMOP':
        #     self.asignment()
        #     return

        # elif self.token_read == 'IDENTIFIER' or self.token_read == 'NUMBERS':
        #     self.expr()
        #     return
        # 
        # elif self.lexer.look_ahead == 'ENDPRG':
        #     return

        # else:
        #     self.output+="parse error"
        #     print("parse error")
        #     exit(1)

    def stmtlist(self):
        self.stmt()
        while self.lexer.look_ahead != KEYWORDS["ENDP"]: 
            self.stmt()

    def program(self):
        self.lexer.match("BEGINPRG")
        self.stmtlist()
        self.lexer.match("ENDPRG")
    
    # asignment -> IDENTIFIER ASGNMOP expr
    def asignment(self):
        self.output+="IDENTIFIER"
        self.lexer.match('IDENTIFIER')
        self.output+="ASGNMOP"
        self.lexer.match('ASGNMOP')
        self.expr()
        print("asignment")
        self.output+="ASSIGNMENT"
        return
