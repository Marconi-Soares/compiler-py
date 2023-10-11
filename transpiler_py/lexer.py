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
        """
        identifier -> {a-zA-Z}{a-zA-Z0-9}+
        number -> [0-9]+
        OPENING -> '('
        CLOSING -> ')'
        BLOCK_START -> '{'
        BLOCK_END -> '}'
        END_INSTRUCTION -> ';'
        TYPE -> int | string
        " -> "
        """
        self.get_char()
    
        while self.char != "":
            self.skip_space()
            self.include()
            self.string()
            self.identifier()
            self.opening()
            self.closing()
            self.separator()
            self.block_start()
            self.end_instruction()
            self.block_end()
            self.assignment()
            self.digit()
            self.get_char()

    def include(self):
        if self.char == "#":
            include_body = ""

            while self.char != ">":
                include_body += self.char
                self.get_char()

            self.return_char()
            self.look_ahead.append(INCLUDE)

    def separator(self):
        if self.char == ',':
            self.look_ahead.append(SEPARATOR)
            self.lexemes.append(self.char)
            self.get_char()

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

    def is_type(self, lexeme):
        if lexeme in ['int', 'string', 'void']:
            return True

    def end_instruction(self):
        if self.char == ';':
            self.lexemes.append(self.char)
            self.look_ahead.append(END_INSTRUCTION)
            self.get_char()

    def assignment(self):
        if self.char == '=':
            self.lexemes.append(self.char)
            self.look_ahead.append(ASSIGNMENT)
            self.get_char()

    def digit(self):
        if self.char.isdigit():
            lex = ""
            while self.char.isdigit():
                lex += self.char
                self.get_char()
            self.return_char()
            self.lexemes.append(lex)
            self.look_ahead.append(DIGIT)

    def block_start(self):
        if self.char == '{':
            self.lexemes.append(self.char)
            self.look_ahead.append(BLOCK_OPEN)
            self.get_char()
    
    def block_end(self):
        if self.char == '}':
            self.lexemes.append(self.char)
            self.look_ahead.append(BLOCK_CLOSE)
            self.get_char()

    def opening(self):
        if self.char == '(':
            self.lexemes.append(self.char)
            self.look_ahead.append(OPEN)
            self.get_char()

    def closing(self):
        if self.char == ')':
            self.lexemes.append(self.char)
            self.look_ahead.append(CLOSE)
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

            self.look_ahead.append(IDENTIFIER)

    def skip_space(self):
        if self.char == ' ':
            self.get_char()
