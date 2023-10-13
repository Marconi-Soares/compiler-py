from tokens import *

class Lexer:
    def __init__(self, source: str) -> None:
        self.source = open(source, "r")
        self.lexemes = []
        self.look_ahead = []

    def get_char(self):
        self.char = self.source.read(1)
        

    def return_char(self, i=1):
        self.source.seek(self.source.tell() - i)

    def tokenize(self):
        self.char = " " # This char will be ignored
    
        while self.char != "":
            self.get_char()

            if self.skipable(): continue
            if self.include(): continue
            if self.opening(): continue
            if self.closing(): continue
            if self.separator(): continue
            if self.block_start(): continue
            if self.block_end(): continue
            if self.end_instruction(): continue
            if self.comparison_and_assignment(): continue
            if self.digit(): continue
            if self.string(): continue
            self.identifier()

    def include(self):
        """
        # include {<|"} [a-zA-Z]+ .h {>|"}
        """
        if self.char == "#": # #
            include_body = self.source.read(7)
            self.char = include_body[-1]

            if include_body != "include": # include
                raise SyntaxError(f"{include_body} is not a valid token")
            
            self.get_char()
            while self.char == " ": # skip one or more whitespaces
                self.get_char()

            if self.char not in ['<', '"']: # {<|"}
                raise SyntaxError(f"Invalid include")
            
            self.get_char()

            while self.char.isalpha(): # [a-zA-Z]+
                self.get_char()

            self.return_char()

            if self.source.read(2) != ".h": # .h
                raise SyntaxError(f"Invalid include")
            
            self.get_char()

            if self.char not in ['"', '>']: # {>|"}
                raise SyntaxError(f"Invalid include")
            
            self.look_ahead.append(INCLUDE)
            return True

    def separator(self):
        if self.char == ',':
            self.look_ahead.append(SEPARATOR)
            self.lexemes.append(self.char)
            return True

    def string(self):
        """
        " [ASCII]+ "
        """
        if self.char == '"': # "
            self.lexemes.append(self.char)
            self.look_ahead.append(OPEN_STRING)

            string_body = ''
            self.get_char()

            while self.char != '"': # ASCII+ "
                string_body += self.char
                self.get_char()

            self.look_ahead.append(ASCII)
            self.lexemes.append(string_body)

            self.look_ahead.append(CLOSE_STRING)
            self.lexemes.append(self.char)

            return True

    def is_type(self, lexeme: str) -> bool:
        """ [ int | char | void ]"""
        return lexeme in ['int', 'char', 'void']

    def keyword(self, lexeme: str):
        """ [ if | else ]"""
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
            return True

    def assignment(self):
        if self.char == '=':
            self.lexemes.append(self.char)
            self.look_ahead.append(ASSIGNMENT)
            return True

    def digit(self):
        """
        [0-9]+
        """
        if self.char.isdigit(): # [0-9]
            lex = ""

            while self.char.isdigit(): # [0-9]+
                lex += self.char
                self.get_char()

            self.return_char()
            self.lexemes.append(lex)
            self.look_ahead.append(DIGIT)
            return True

    def block_start(self):
        if self.char == '{':
            self.lexemes.append(self.char)
            self.look_ahead.append(BLOCK_OPEN)
            return True
    
    def block_end(self):
        if self.char == '}':
            self.lexemes.append(self.char)
            self.look_ahead.append(BLOCK_CLOSE)
            return True

    def opening(self):
        if self.char == '(':
            self.lexemes.append(self.char)
            self.look_ahead.append(OPEN)
            return True

    def closing(self):
        if self.char == ')':
            self.lexemes.append(self.char)
            self.look_ahead.append(CLOSE)
            return True

    def comparison_and_assignment(self):
        """
        COMPARISON -> [!|<|>|=] =
        ASSIGNMENT -> =
        """
        if self.char in ['!', "<", ">", "="]: # [!|<|>|=]
            lex = self.char
            self.get_char()
            
            if self.char == "=": # =
                self.look_ahead.append(COMPARISON)
                self.lexemes.append(lex + "=")
            
            else: 
                self.return_char()
                self.look_ahead.append(ASSIGNMENT)
                self.lexemes.append("=")
            
            return True

    def identifier(self):
        """
        [a-zA-Z] [a-zA-Z0-9]+
        """
        if self.char.isalpha(): # [a-zA-Z]
            lex = ""
            while self.char.isalnum(): # [a-zA-Z0-9]+
                lex += self.char
                self.get_char()

            self.return_char()
            self.lexemes.append(lex)

            if self.is_type(lex): 
                self.look_ahead.append(TYPE)
                return
            
            if self.keyword(lex): 
                return

            self.look_ahead.append(IDENTIFIER)

    def skipable(self):
        if self.char in [' ', '\n', '\t']:
            return True
