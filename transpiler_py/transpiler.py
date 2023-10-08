class Lexer:
    def __init__(self) -> None:
        self.source = open('file.txt')
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
            self.string()
            self.identifier()
            self.opening()
            self.closing()
            self.block_start()
            self.end_instruction()
            self.block_end()
            self.assignment()
            self.digit()
            self.get_char()

    def string(self):
        if self.char == '"':
            self.lexemes.append(self.char)
            self.look_ahead.append('"')

            string_body = ''
            self.get_char()
            while self.char != '"':
                string_body += self.char
                self.get_char()

            self.look_ahead.append('ASCII')
            self.lexemes.append(string_body)
            self.look_ahead.append('"')
            self.lexemes.append(self.char)

    def is_type(self, lexeme):
        if lexeme in ['int', 'string', 'void']:
            return True

    def end_instruction(self):
        if self.char == ';':
            self.lexemes.append(self.char)
            self.look_ahead.append('END_INSTRUCTION')
            self.get_char()

    def assignment(self):
        if self.char == '=':
            self.lexemes.append(self.char)
            self.look_ahead.append('ASSIGNMENT')
            self.get_char()

    def digit(self):
        if self.char.isdigit():
            lex = ""
            while self.char.isdigit():
                lex += self.char
                self.get_char()
            self.return_char()
            self.lexemes.append(lex)
            self.look_ahead.append('DIGIT')

    def block_start(self):
        if self.char == '{':
            self.lexemes.append(self.char)
            self.look_ahead.append('BLOCK_START')
            self.get_char()
    
    def block_end(self):
        if self.char == '}':
            self.lexemes.append(self.char)
            self.look_ahead.append('BLOCK_END')
            self.get_char()

    def opening(self):
        if self.char == '(':
            self.lexemes.append(self.char)
            self.look_ahead.append('OPENING')
            self.get_char()

    def closing(self):
        if self.char == ')':
            self.lexemes.append(self.char)
            self.look_ahead.append('CLOSING')
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
                self.look_ahead.append('TYPE')
                return

            self.look_ahead.append('IDENTIFIER')

    def skip_space(self):
        if self.char == ' ':
            self.get_char()

class Parser:
    def __init__(self, lexemes, look_ahead) -> None:
        self.res = ""
        self.lexemes = lexemes
        self.look_ahead = look_ahead
        self.current_identation = 0
    
    def match(self, expected):
        if self.look_ahead[0] == expected:
            self.look_ahead.pop(0)
            return True
        else:
            raise SyntaxError('Invalid')

    def parse(self):
        """
        function_definition -> TYPE IDENTIFIER OPENING {PARAM} CLOSING BLOCK_START {BLOCK} BLOCK_END 
        function_call -> TYPE IDENTIFIER OPENING {PARAM} CLOSING END_INSTRUCTION
        BLOCK -> function_call
        PARAM -> IDENTIFIER ASSIGNMENT DIGIT
        variable_definition -> TYPE IDENTIFIER ASSIGNMENT VALUE
        VALUE = DIGIT | STRING
        STRING = " ASCII "
        """
        self.function_definition()

    def function_call(self):
        self.match('IDENTIFIER')
        function_identifier = self.convert_functions()
        self.res += function_identifier

        self.match('OPENING')
        self.res += self.lexemes.pop(0)
        
        if self.look_ahead[0] != 'CLOSING':
            self.param()

        self.match('CLOSING')
        self.res += self.lexemes.pop(0)

        self.match('END_INSTRUCTION')
        self.lexemes.pop(0) # throw ';' away
        self.res += '\n' + '\t'*self.current_identation    

    def variable_definition(self):
        self.match('TYPE')
        variable_type = self.convert_type()

        self.match('IDENTIFIER')
        self.res+= self.lexemes.pop(0) + f": {variable_type}"

        self.match('ASSIGNMENT')
        self.res+= ' ' + self.lexemes.pop(0) + ' '
        
        if self.look_ahead[0] == '"':
            self.match('"')
            self.res += self.lexemes.pop(0)

            self.match("ASCII")
            self.res += self.lexemes.pop(0)

            self.match('"')
            self.res += self.lexemes.pop(0)
        
        else:
            self.match('DIGIT')
            self.res+= self.lexemes.pop(0)

        self.match('END_INSTRUCTION')
        self.lexemes.pop(0) # Throw ';' away
        self.res+= '\n' + '\t'*self.current_identation

    def function_definition(self):
        self.match('TYPE')
        return_type = self.convert_type()

        self.match('IDENTIFIER')
        self.res += f'def {self.lexemes.pop(0)}'
        self.match('OPENING')
        self.res += self.lexemes.pop(0)
        
        if self.look_ahead[0] != 'CLOSING':
            self.param()

        self.match('CLOSING')

        self.res += self.lexemes.pop(0) + f' -> {return_type}:\n'
        self.block()

    def block(self):
        self.match('BLOCK_START')
        self.lexemes.pop(0) # throw '{' away
        self.res += "\t"
        self.current_identation += 1
        
        if self.look_ahead[0] != 'BLOCK_END':
            self.instructions()

        self.match('BLOCK_END')
        self.lexemes.pop(0) # throw '}' away
        self.res += '\n'

    def instructions(self):
        while self.look_ahead[0] in ['TYPE', 'IDENTIFIER']:
            self.instruction()

    def instruction(self):
        if self.look_ahead[0] == 'TYPE':
            self.variable_definition()

        elif self.look_ahead[0] == 'IDENTIFIER': 
            self.function_call()

    def param(self):
        param_type = None

        if self.look_ahead[0] == 'TYPE':
            self.match('TYPE')
            param_type = self.convert_type()

        self.match('IDENTIFIER')
        self.res += self.lexemes.pop(0)

        if param_type:
             self.res+= f': {param_type}'

        if self.look_ahead[0] != 'ASSIGNMENT':
            return

        self.match('ASSIGNMENT')
        self.res += self.lexemes.pop(0)
        self.match('DIGIT')
        self.res += self.lexemes.pop(0)

    def convert_type(self):
        match self.lexemes.pop(0):
            case 'int':
                return 'int'

            case 'string':
                return 'str'

            case 'void':
                return 'None'
    
    def convert_functions(self):
        lexeme = self.lexemes.pop(0)
        match lexeme:
            case 'printf':
                return 'print'

            case 'scan':
                return 'input'

l = Lexer()
l.tokenize()
p = Parser(l.lexemes, l.look_ahead)
p.parse()
print(p.res)
