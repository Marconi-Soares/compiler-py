from arit_tokenizer import Lexer
from arit_parser import Parser


if __name__ == '__main__':
    lexer = Lexer(input('>>> '))
    lexer.generate_token_code()
    print(lexer.token_code)
    # parser = Parser(code=lexer.token_code)
