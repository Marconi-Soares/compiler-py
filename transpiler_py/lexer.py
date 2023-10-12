from tokens import *

class Lexer:
    def __init__(self, source: str) -> None:
        self.source = open(source, "r")
        self.lexemes = []
        self.look_ahead = []

    def get_char(self):
        self.char = self.source.read(1)

    def return_char(self):
        self.source.seek(self.source.tell() - 1)

    def tokenize(self):
        self.get_char()
    
        while self.char != "":
            if self.skip_space(): continue
            if self.include(): continue
            if self.opening(): continue
            if self.closing(): continue
            if self.separator(): continue
            if self.block_start(): continue
            if self.end_instruction(): continue
            if self.block_end(): continue
            if self.comparison(): continue
            if self.assignment(): continue
            if self.digit(): continue
            if self.string(): continue
            self.identifier()

            self.get_char()

    def include(self):
        if self.char == "#":
            include_body = ""

            while self.char != ">":
                include_body += self.char
                self.get_char()

            self.return_char()
            self.get_char()
            self.look_ahead.append(INCLUDE)
            return True

    def separator(self):
        if self.char == ',':
            self.look_ahead.append(SEPARATOR)
            self.lexemes.append(self.char)
            self.get_char()
            return True

    def string(self):
        if self.char == '"':
            self.lexemes.append(self.char)
            self.look_ahead.append(OPEN_STRING)

            string_body = ''
            self.get_char()

            while self.char != '"':
                string_body += self.char
                self.get_char()

            self.look_ahead.append(ASCII)
            self.lexemes.append(string_body)
            self.look_ahead.append(CLOSE_STRING)
            self.lexemes.append(self.char)
            self.get_char()
            return True

    def is_type(self, lexeme: str) -> bool:
        return lexeme in ['int', 'char', 'void']

    def keyword(self, lexeme: str):
        if lexeme == 'if':
            self.look_ahead.append(IF)
            return True

        elif lexeme == 'else':
            self.look_ahead.append(ELSE)
            return True

        return False

    def end_instruction(self):
        if self.char == ';':
            self.lexemes.append(self.char)
            self.look_ahead.append(END_INSTRUCTION)
            self.get_char()
            return True

    def assignment(self):
        if self.char == '=':
            self.lexemes.append(self.char)
            self.look_ahead.append(ASSIGNMENT)
            self.get_char()
            return True

    def digit(self):
        if self.char.isdigit():
            lex = ""

            while self.char.isdigit():
                lex += self.char
                self.get_char()

            self.return_char()
            self.get_char()
            self.lexemes.append(lex)
            self.look_ahead.append(DIGIT)

            return True

    def block_start(self):
        if self.char == '{':
            self.lexemes.append(self.char)
            self.look_ahead.append(BLOCK_OPEN)
            self.get_char()
            return True
    
    def block_end(self):
        if self.char == '}':
            self.lexemes.append(self.char)
            self.look_ahead.append(BLOCK_CLOSE)
            self.get_char()
            return True

    def opening(self):
        if self.char == '(':
            self.lexemes.append(self.char)
            self.look_ahead.append(OPEN)
            self.get_char()
            return True

    def closing(self):
        if self.char == ')':
            self.lexemes.append(self.char)
            self.look_ahead.append(CLOSE)
            self.get_char()
            return True

    def comparison(self):
        """
        COMPARISON -> {=|!} =
        """
        if self.char in ['!', "<", ">", "="]:
            lex: str = self.char
            self.get_char()
            
            if self.char == "=":
                self.look_ahead.append(COMPARISON)
                self.lexemes.append(lex + self.char)
                self.get_char()
                return True

            self.return_char()
            self.return_char()
            self.get_char()

    def identifier(self):
        if self.char.isalpha():
            lex = ""
            while self.char.isalnum():
                lex += self.char
                self.get_char()

            self.return_char()
            self.lexemes.append(lex)

            if self.is_type(lex): 
                self.look_ahead.append(TYPE)
                return
            
            if self.keyword(lex): return

            self.look_ahead.append(IDENTIFIER)

    def skip_space(self):
        if self.char == ' ':
            self.get_char()
