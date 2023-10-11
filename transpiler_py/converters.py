from tokens import *


class Converter:
    def __init__(self) -> None:
        self.current_identation: int
        self.res: str = ""
        self.lexemes: list[str] = []
        self.look_ahead: list[int] = []

    def match(self, expected):
        raise NotImplementedError()

    def default_function_call(self, arg: str) -> None:
        raise NotImplementedError()

    def convert_type(self) -> str:
        match self.lexemes.pop(0):
            case 'int':
                return 'int'

            case 'string':
                return 'str'

            case 'void':
                return 'None'

            case _:
                raise SyntaxError("Invalid")
    
    def convert_function(self) -> None:
        lexeme = self.lexemes.pop(0)
        match lexeme:
            case 'printf':
                return self.convert_print()
            case _:
                return self.default_function_call(lexeme)
    

    def convert_print(self) -> None:
        self.res += "print"

        self.match(OPEN)
        self.res += self.lexemes.pop(0)
        
        self.match(OPEN_STRING)
        self.res += self.lexemes.pop(0)
         
        self.match(ASCII)
        string_body: str = self.lexemes.pop(0)
        print_end: str = ", end=''"

        if string_body.endswith("\\n"):
            string_body = string_body[0:-2]
            print_end = ""

        self.match(CLOSE_STRING)
        string_body += self.lexemes.pop(0)

        if self.look_ahead[0] == SEPARATOR:
            for placeholder in ["%d", "%s", "%c"]:
                string_body = string_body.replace(placeholder, "{}")

            string_body += ".format("

            while self.look_ahead[0] == SEPARATOR:
                self.match(SEPARATOR)
                self.lexemes.pop(0) # throw "," away
                self.match(IDENTIFIER)
                string_body += self.lexemes.pop(0) +", "

            string_body = string_body[0:-2] # Remove the last "," at the .format() method

            string_body += ")"

        self.res += string_body

        if self.look_ahead[0] == SEPARATOR:
            self.match(SEPARATOR)
            self.lexemes.pop(0)
            self.match(IDENTIFIER)
            print(self.lexemes.pop(0))

        self.res += print_end

        self.match(CLOSE)
        self.res += self.lexemes.pop(0)

        self.match(END_INSTRUCTION)
        self.lexemes.pop(0)
        self.res += '\n' + '\t'*self.current_identation
