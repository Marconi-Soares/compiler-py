from typing import TypedDict


class WeekDayCount(TypedDict):
    segunda: int
    terça: int
    quarta: int
    quinta: int
    sexta: int
    sábado: int
    domingo: int


def process_file(filename: str) -> WeekDayCount:
    """
    Processa o arquivo provido como argumento na linha de comando
    através da função match_days_of_week e retorna o número de
    ocorrência de cada dia da semana desse arquivo.
    """
    weekday_count: WeekDayCount = {
        "segunda": 0,
        "terça":   0,
        "quarta":  0,
        "quinta":  0,
        "sexta":   0,
        "sábado":  0,
        "domingo": 0,
    }

    with open(filename, 'r') as file:

        for row in file:
            weekday_count = match_days_of_week(row, weekday_count)

    return weekday_count


def match_days_of_week(
    row: str,
    weekday_count: WeekDayCount
) -> WeekDayCount:
    """
    Atualiza a informação sobre a quantidade de ocorrência
    de cada dia da semana com base na linha do arquivo provida.
    """
    valid_weekday: list[str] = [
        'segunda',
        'terça',
        'quarta',
        'quinta',
        'sexta',
        'sábado',
        'domingo'
    ]

    for word in row.split():

        if word.lower() in valid_weekday:
            weekday_count[word.lower()] += 1 # type: ignore

        else:
            print(f"\"{word}\" não é um dia da semana válido.")
            exit()

    return weekday_count


def print_tokens(weekday_count: WeekDayCount):
    """
    Exibe os dias da semana e o número de ocorrência
    de cada dia.
    """
    for weekday, count in weekday_count.items():
        print(f"{weekday:<7}: {count:>3}")
