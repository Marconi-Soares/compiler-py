"""
expr -> term {ADDOP term}
term -> term {factor MULOP factor}
factor -> IDENTIFIER | NUMBERS | '(' expr ')'
asignment -> IDENTIFIER ASGNMOP expr
"""

class Parser:
    def __init__(self, code) -> None:
        for token_read in code.splitlines():
            self.parse_token(token_read)
    
    def parse_token(self, token_read):
        if token_read == 'IDENTIFIER' and look_ahead == 'ASIGNMOP':
            self.asignment()

        elif token_read == 'IDENTIFIER':
            self.expr(token_read)

    def read_from_token_code(self, code):
        return code.splitlines()[0]


    def expr(self):

        self.term()
        while (token_read == 'ADDOP'):
            readop = token_read
            self.term()
            print()

    def term(self):
        pass

pr = Parser(p.token_code)
