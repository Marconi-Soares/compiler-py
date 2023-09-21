import os
import sys
from days_of_week import (
    print_tokens,
    process_file
)


def clear() -> None:
    """
    Limpa o terminal dependendo do sistema operacional
    em que o script está sendo executado.
    """
    if os.name:
        "unix"
        os.system('clear')
        return

    os.system("cls")


def get_filename() -> str:
    if not len(sys.argv) > 1:
        print("Nenhum arquivo foi fornecido.")
        exit()

    return sys.argv[1]


if __name__ == "__main__":
    filename: str = get_filename()

    try:
        tokens = process_file(filename)

    except FileNotFoundError:
        print(f"O arquivo {filename} não pôde ser encontrado.")
        exit()

    clear()
    print_tokens(tokens)
