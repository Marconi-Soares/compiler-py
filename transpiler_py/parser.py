from tokens import *
from converters import Converter


class Parser(Converter):
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
        self.function_list()

    def function_list(self):
        try:
            while self.look_ahead[0] in [TYPE, INCLUDE]:
                if self.look_ahead[0] == INCLUDE:
                    self.match(INCLUDE)

                self.function_definition()
        except IndexError:
            return

    def function_call(self):
        self.match(IDENTIFIER)
        self.convert_function()

    def default_function_call(self, function_identifier):
        self.res += function_identifier

        self.match(OPEN)
        self.res += self.lexemes.pop(0)
        
        if self.look_ahead[0] != CLOSE:
            self.param()

        self.match(CLOSE)
        self.res += self.lexemes.pop(0)

        self.match(END_INSTRUCTION)
        self.lexemes.pop(0) # throw ';' away
        self.res += '\n' + '\t'*self.current_identation    

    def variable_definition(self):
        self.match(TYPE)
        variable_type = self.convert_type()

        self.match(IDENTIFIER)
        self.res+= self.lexemes.pop(0) + f": {variable_type}"

        self.match(ASSIGNMENT)
        self.res+= ' ' + self.lexemes.pop(0) + ' '
        
        if self.look_ahead[0] == OPEN_STRING:
            self.match(OPEN_STRING)
            self.res += self.lexemes.pop(0)

            self.match(ASCII)
            self.res += self.lexemes.pop(0)

            self.match(CLOSE_STRING)
            self.res += self.lexemes.pop(0)
        
        else:
            self.match(DIGIT)
            self.res+= self.lexemes.pop(0)

        self.match(END_INSTRUCTION)
        self.lexemes.pop(0) # Throw ';' away
        self.res+= '\n' + '\t'*self.current_identation

    def function_definition(self):
        self.match(TYPE)
        return_type = self.convert_type()

        self.match(IDENTIFIER)
        self.res += f'def {self.lexemes.pop(0)}'
        self.match(OPEN)
        self.res += self.lexemes.pop(0)
        
        if self.look_ahead[0] != CLOSE:
            self.param()

        self.match(CLOSE)

        self.res += self.lexemes.pop(0) + f' -> {return_type}:\n'
        self.block()

    def block(self):
        self.match(BLOCK_OPEN)
        self.lexemes.pop(0) # throw '{' away
        self.res += "\t"
        self.current_identation += 1
        
        if self.look_ahead[0] != BLOCK_CLOSE:
            self.instructions()
        
        self.match(BLOCK_CLOSE)
        self.current_identation -= 1
        self.lexemes.pop(0) # throw '}' away
        self.res += '\n'


    def instructions(self):
        while self.look_ahead[0] in [TYPE, IDENTIFIER]:
            self.instruction()

    def instruction(self):
        if self.look_ahead[0] == TYPE:
            self.variable_definition()

        elif self.look_ahead[0] == IDENTIFIER: 
            self.function_call()

    def param(self):
        param_type = None

        if self.look_ahead[0] == TYPE:
            self.match(TYPE)
            param_type = self.convert_type()

        self.match(IDENTIFIER)
        self.res += self.lexemes.pop(0)

        if param_type:
             self.res+= f': {param_type}'

        if self.look_ahead[0] != ASSIGNMENT:
            return

        self.match(ASSIGNMENT)
        self.res += self.lexemes.pop(0)
        self.match(DIGIT)
        self.res += self.lexemes.pop(0)
