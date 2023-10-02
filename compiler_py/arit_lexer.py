from string import ascii_letters
from errorcpl import exit_error
from wrt_log import TraceFile


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
BEGINP = 'BEGINP'
ENDP = 'ENDP'

# Index  | LexLvl | Categ |  Type  | Offset 
# 0        0        0       0        0                        <------ Linha 0 nao utilizada.
# 1        7       VAR     int      -12
# 2        8      FUNCT   float     -16
# *

# LEX_LVL = 0

class Lexer:
    def __init__(self, filepath):
        TraceFile.write_log(filepath, 'Lexer __init__')
         
        self.file_stream = open(filepath, 'r')
        self.tokens = []
        self.lex_lvl = 0
        self.char = ""
        self.symtab = []
        self.lex_tape = []

        # while len(self.source) > 0:
        #     self.char = self.source.pop(0)

        #     if self.char == " \n\t\r":
        #         continue

        # self.append_entries()
    
    # id = [a-Z] [0-9 a-Z]
    def isID(self):
        i = 0
        lexeme: list[str] = []
        lexeme[i] = self.get_char()

        if lexeme[i].isalpha():
            i += 1
            lexeme[i] = self.get_char()
            while lexeme[i].isalnum():
                i += 1
                lexeme[i] = self.get_char()

            self.unget_char()
            i = self.is_keyword(lexeme)
            if not i:
                return i

            return IDENTIFIER
        
        self.unget_char()
        return False

    def unget_char(self):
        self.file_stream.seek(self.file_stream.tell() -1)

    def get_char(self):
        return self.file_stream.read(1)
    
    def is_keyword(self, lexeme):
        pass

    # floating = UINT ('.' digit* enotation? | enotation) | '.' digit+ enotation?
    def isNUM(self):
        pass
    
    def isRELOP(self):
        pass

    def isADD(self):
        pass

    def isMUL(self):
        pass

    def isASGNM(self):
        pass


    def get_token(self):
        # self.skipspaces()
        token = None
        if token := self.isID():
            return token

        elif token := self.isNUM():
            return token

        elif token := self.isRELOP():
            return token

        elif token := self.isADD():
            return token

        elif token := self.isMUL():
            return token

        elif token := self.isASGNM():
            return token



    def append_entries(self):
        # global LEX_LVL

        entry = {
            'LEX_LVL': self.lex_lvl,
            'INDEX': len(self.lex_tape),
            'CATEGORY': ''
        }
        token_type = None
        token_value = self.char
        token_context = None
        
        if self.char in BEGINP:
            sequence = self.get_sequence(BEGINP)
            token_type = 'BEGINP'

        if self.char in ENDP:
            sequence = self.get_sequence(ENDP)
            token_type = 'ENDP'

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
        # i = 0;
        # lexeme[i] = toupper(getc(tape));
        # if (isalpha(lexeme[i])) {
        #     while (isalnum(lexeme[++i] = toupper(getc(tape))));
        #     ungetc(lexeme[i], tape);
        #     lexeme[i] = 0;
        #     if ( (i = iskeyword(lexeme)) )
        #         return i;
        #     return ID;
        # }
        # ungetc(lexeme[i], tape);
        TraceFile.write_log(self.char, 'get_sequence')
        
        seq = self.char

        while len(self.source) > 0:
            self.char = self.source.pop(0)
            
            if self.char in token_type:
                seq += self.char

            elif token_type and self.char in ' \n':
                self.source.insert(0, self.char)
                break

            elif token_type:
                exit_error(f'token mismatch: tokent = [{token_type}], char = [{self.char}]')

            if self.char in " \n":
                return seq


        return seq
    def symtab_lookup(self, token, token_type=None):
        for entry in self.symtab:
            TraceFile.write_log(msg=f"entry={entry}",fnc="symtab_lookup")
            if token == entry['CATEGORY']:
                if token_type and token_type != entry['TYPE']:
                    continue

                return entry
        return False
        
    def generate_token_code(self):
        self.token_code = ""

        for token in self.tokens:
            self.token_code += token['type'] + '\n' 

