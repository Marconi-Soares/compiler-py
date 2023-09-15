from string import ascii_letters


NUMBERS = '0123456789'
OPERATORS = '+-*/'
IDENTIFIER = ascii_letters
OPENNING = '([{'
CLOSING = '}])'
ASSIGNMENT = '='


class Parser:
    def __init__(self, source):
        self.source = [letter for letter in source]
        self.tokens = []
        self.char = ""

        while len(self.source) > 0:
            self.char = self.source.pop(0)

            if self.char in " ":
                continue

            if self.char in NUMBERS:
                sequence = self.get_sequence(NUMBERS)
                self.tokens.append({'type': 'NUMBER', 'value': sequence})

            if self.char in OPERATORS:
                self.tokens.append({'type': 'OPERATOR', 'value': self.char})

            if self.char in IDENTIFIER:
                sequence = self.get_sequence(IDENTIFIER)
                self.tokens.append({'type': 'IDENTIFIER', 'value': sequence})

            if self.char in OPENNING:
                self.tokens.append({'type': 'OPENNING', 'value': self.char})

            if self.char in CLOSING:
                self.tokens.append({'type': 'CLOSING', 'value': self.char})

            if self.char in ASSIGNMENT:
                self.tokens.append({'type': 'ASSIGNMENT', 'value': self.char})


    def get_sequence(self, token_type):
        seq = self.char

        while len(self.source) > 0:
            self.char = self.source.pop(0)
                
            if self.char == " ":
                return seq

            if self.char in token_type:
                seq += self.char
            else:
                break

        return seq

source = input('>>> ')
p = Parser(source)

for token in p.tokens:
    print(f"{token['type']}: {token['value']}")
