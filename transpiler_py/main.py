import os
import sys
from lexer import Lexer
from parser import Parser


def get_input_file() -> str:
    args: list[str] = sys.argv
    file_name: str

    if len(args) < 2:
        file_name = "main.c"
    else:
        file_name = args[1]

    if len(file_name.split('.')) != 2:
        print("Formato invalido, o arquivo deve estar no padrão '*.c'")
        exit()

    if os.path.exists(file_name):
        return file_name
    
    print(f'O arquivo "{file_name}" não foi encontrado.')
    exit()

def get_output_file(input_file) -> str:
    args = sys.argv

    if len(args) < 3:
        file_name, _ = input_file.split('.')
        output_file: str = file_name + '.py'
    else:
        output_file: str = args[2]

    if not os.path.exists(output_file):
        return output_file

    msg: str = f'deseja substituir o arquivo {output_file} existente? [Sim/N]'
    action: str = input(msg)

    if action != 'Sim':
        exit()

    return output_file

def main() -> None:
    input_file: str = get_input_file()
    output_file: str = get_output_file(input_file)

    lexer: Lexer = Lexer(input_file)
    lexer.tokenize()
    
    print(lexer.lexemes)
    print(lexer.look_ahead)

    parser: Parser = Parser(lexer.lexemes, lexer.look_ahead)
    parser.parse()

    with open(output_file, 'w') as file:
        file.write(parser.res)

if __name__ == '__main__':
    main()
