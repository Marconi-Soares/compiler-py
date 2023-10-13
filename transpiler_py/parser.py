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
        self.program()

    def program(self):
        """
        program -> {function_definition | include}+
        """
        try:
            while self.look_ahead[0] in [TYPE, INCLUDE]: # {function_definition | include} +

                if self.look_ahead[0] == INCLUDE:
                    self.match(INCLUDE)                  # Remove includes from look ahead

                self.function_definition()
        except IndexError:
            return

    def function_call(self):
        self.match(IDENTIFIER)
        self.convert_function()

    def default_function_call(self, function_identifier):
        """
        function_call -> identifier OPEN {params+} CLOSE
        """
        self.res += function_identifier

        self.match(OPEN)
        self.res += self.lexemes.pop(0)
        
        if self.look_ahead[0] != CLOSE:         # {params+}
            self.params()

        self.match(CLOSE)
        self.res += self.lexemes.pop(0)

    def return_definition(self):
        """
        return_definition -> RETURN {DIGIT | IDENTIFIER}
        """
        self.match(RETURN)
        self.res += self.lexemes.pop(0) + " "
        
        if self.look_ahead[0] == DIGIT:
            self.match(DIGIT)
            self.res += self.lexemes.pop(0)
            return 
        
        if self.look_ahead[0] == IDENTIFIER:
            self.match(IDENTIFIER)
            self.res += self.lexemes.pop(0)
            return

    def variable_definition(self):
        """
        variable_definition -> {TYPE} IDENTIFIER ASSIGNMENT [DIGIT | STRING]
        """
        # STRING -> OPEN_STRING ASCII CLOSE_STRING
        if self.look_ahead[0] == TYPE:                              # {TYPE}
            self.match(TYPE)
            variable_type = self.convert_type()

            self.match(IDENTIFIER)
            self.res+= self.lexemes.pop(0) + f": {variable_type}"   # "var: int"

        else:
            # redefinition of a variable
            self.match(IDENTIFIER)
            self.res += self.lexemes.pop(0)

        self.match(ASSIGNMENT)
        self.res+= ' ' + self.lexemes.pop(0) + ' '
        

        if self.look_ahead[0] == OPEN_STRING: # STRING
            self.match(OPEN_STRING)
            self.res += self.lexemes.pop(0)

            self.match(ASCII)
            self.res += self.lexemes.pop(0)

            self.match(CLOSE_STRING)
            self.res += self.lexemes.pop(0)
        
        else:                                 # DIGIT
            self.match(DIGIT)
            self.res+= self.lexemes.pop(0)

    def function_definition(self):
        """
        function_definition -> TYPE IDENTIFIER OPEN {params} CLOSE block 
        """

        self.match(TYPE)
        return_type = self.convert_type()

        self.match(IDENTIFIER)
        function_identifier = self.lexemes.pop(0)

        if function_identifier == "main":
            self.convert_main()

        # add a breakline if it is not the first function in the program
        if len(self.res) != 0: self.res += "\n" 

        self.match(OPEN)
        self.res += f'def {function_identifier}{self.lexemes.pop(0)}' # def identifier(
        
        if self.look_ahead[0] != CLOSE: # {PARAMS+}
            self.params()

        self.match(CLOSE)

        self.res += self.lexemes.pop(0) + f' -> {return_type}:\n' # -> int:
        self.block()

    def if_definition(self):
        """
        if_definition -> IF OPEN IDENTIFIER COMPARISON IDENTIFIER CLOSE  [block | instruction]
        """

        self.match(IF)
        self.res += self.lexemes.pop(0)
        
        self.match(OPEN)
        self.lexemes.pop(0) # Throw "(" away
        self.res += " "

        self.match(IDENTIFIER)
        self.res += self.lexemes.pop(0)

        self.match(COMPARISON)
        self.res += f" {self.lexemes.pop(0)} "
        
        self.match(IDENTIFIER)
        self.res += self.lexemes.pop(0)

        self.match(CLOSE)
        self.lexemes.pop(0) # Throw ")" away
        self.res += ":\n"

        # [block | instruction]
        if self.look_ahead[0] != BLOCK_OPEN:             
            self.current_identation += 1
            self.instruction()
            self.current_identation -= 1
            return

        self.block()

    def else_definition(self):
        """
        else_definition -> ELSE [if_definition | instruction | block]
        """
        self.res += "\n" + "\t"*self.current_identation # add a breakline before an if statement
        self.match(ELSE)
        else_body = self.lexemes.pop(0)
        
        if self.look_ahead[0] == IF:
            self.res += 'el'
            self.if_definition()
            return
        
        self.res += else_body + ":\n"

        if self.look_ahead[0] != BLOCK_OPEN:
            self.current_identation += 1
            self.instruction()
            self.current_identation -= 1
            return

        self.block()

    def block(self):
        """
        block -> BLOCK_OPEN {instructions} BLOCK_CLOSE
        """
        self.match(BLOCK_OPEN)
        self.lexemes.pop(0) # throw '{' away
        self.current_identation += 1
        
        if self.look_ahead[0] != BLOCK_CLOSE: # {instruction+}
            self.instructions()
        
        self.match(BLOCK_CLOSE)
        self.current_identation -= 1
        self.lexemes.pop(0) # throw '}' away


    def instructions(self):
        """
        instructions -> {instruction+}
        """
        while self.look_ahead[0] in [TYPE, IDENTIFIER, IF, ELSE, RETURN]: # {instruction+}
            self.instruction()

    def instruction(self):
        """
        instruction -> [
              variable_definition 
            | function_call 
            | if_definition 
            | else_definition
            | RETURN
        ]
                       END_INSTRUCTION
        """
        self.res += "\t"*self.current_identation
        if self.look_ahead[0] == TYPE:
            self.variable_definition()

        elif self.look_ahead[0] == RETURN:
            self.return_definition()

        elif self.look_ahead[0] == IDENTIFIER and self.look_ahead[1] == OPEN: 
            self.function_call()

        elif (
            self.look_ahead[0] == IDENTIFIER 
            and self.look_ahead[1] == ASSIGNMENT
        ):
            self.variable_definition()

        elif self.look_ahead[0] == IF:
            self.res += "\n" + "\t"*self.current_identation # add a breakline before an if statement
            self.if_definition()
            return

        elif self.look_ahead[0] == ELSE:
            self.else_definition()
            return

        self.match(END_INSTRUCTION)
        self.lexemes.pop(0) # throw ';' away
        self.res += '\n'

    def params(self):
        while self.look_ahead[0] in [TYPE, IDENTIFIER]:
            self.param()

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

