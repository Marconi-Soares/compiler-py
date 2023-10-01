from string import ascii_letters
from wrt_log import write_log
# from wrt_log import write_log


NUMBERS = '0123456789.'
ADDOP = '+-'
MULOP = '*/'
OPERATORS = '+-*/'
IDENTIFIER = ascii_letters
OPENNING = '('
CLOSING = ')'
SCOPE_BEGIN = '{'
SCOPE_END = '}'
ASSIGNMENT = '='

# Index  | LexLvl | Categ |  Type  | Offset 
# 0        0        0       0        0                        <------ Linha 0 nao utilizada.
# 1        7       VAR     int      -12
# 2        8      FUNCT   float     -16
# *

LEX_LVL = 0

class Lexer:
    def __init__(self, source):
        self.source = [letter for letter in source]
        self.tokens = []
        self.char = ""
        self.symtab = []
        self.lex_tape = []

        while len(self.source) > 0:
            self.char = self.source.pop(0)
            write_log(self.char, 'INIT')

            if self.char in " ":
                continue

            self.append_entries()

            # if self.char in NUMBERS:
            #     self.append_numbers()

            # if self.char in OPERATORS:
            #     self.append_operators()

            # if self.char in IDENTIFIER:
            #     self.append_identifier()
            #     sequence = self.get_sequence(IDENTIFIER)
            #     self.tokens.append({'type': 'IDENTIFIER', 'value': sequence})

            # if self.char in OPENNING:
            #     self.tokens.append({'type': 'OPENNING', 'value': self.char})

            # if self.char in CLOSING:
            #     self.tokens.append({'type': 'CLOSING', 'value': self.char})

            # if self.char in ASSIGNMENT:
            #     self.tokens.append({'type': 'ASSIGNMENT', 'value': self.char})

    def append_entries(self):
        global LEX_LVL

        entry = {
            'LEX_LVL': LEX_LVL,
            'INDEX': len(self.lex_tape),
            'CATEGORY': ''
        }
        token_type = None
        token_value = self.char
        token_context = None

        if self.char in NUMBERS:
            sequence = self.get_sequence(NUMBERS)
            token_context = ('INT', 'FLOAT') [isinstance(sequence, int)]
            token_type = 'NUMBERS'

        elif self.char in OPERATORS:
            token_context = ('ADDOP', 'MULOP') [self.char in '*/']
            token_type = 'OPERATORS'

        elif self.char in IDENTIFIER:
            token_type = 'IDENTIFIER'
            token_value = self.get_sequence(IDENTIFIER)

        elif self.char in ASSIGNMENT:
            token_type = 'ASGNMOP'

        elif self.char in OPENNING:
            token_context = 'PRECEDENCE_BEGIN'
            token_type = 'OPENNING'

        elif self.char in CLOSING:
            token_context = 'PRECEDENCE_END'
            token_type = 'CLOSING'

        # elif self.char in SCOPE_BEGIN:
        #     token_type = 'OPENNING'
        #     LEX_LVL += 1

        # elif self.char in SCOPE_END:
        #     token_type = 'CLOSING'
        #     LEX_LVL -= 1


        else:
            return False

        self.tokens.append({'type': token_type, 'value': token_value})
        entry['CATEGORY'] = token_type
        entry['TYPE'] = token_context

        self.symtab.append(entry)
        self.lex_tape.append(token_value)

    def get_sequence(self, token_type):
        write_log(self.char, 'get_sequence')
        
        seq = self.char

        while len(self.source) > 0:
            self.char = self.source.pop(0)

                
            if self.char == " ":
                return seq

            if self.char in token_type:
                seq += self.char

            elif token_type:
                self.source.insert(0, self.char)
                break

        return seq
    
    def generate_token_code(self):
        self.token_code = ""

        for token in self.tokens:
            self.token_code += token['type'] + '\n' 

