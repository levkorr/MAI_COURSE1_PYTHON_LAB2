import argparse

# python -m streamstats analyze INPUT [INPUT ...] --format csv|jsonl --output REPORT.json
# python -m streamstats analyze INPUT --format jsonl --skip-invalid


def parse():
    ''' Модуль создающий парсер
    
    Args:
        None
    
    Returns:
        args: Аргументы парсера
    '''
    parser = argparse.ArgumentParser(
        prog="streamstats",
        description="Combines the files.",
        usage="straamstats <command> [arguments]",
        add_help=False
    )
    commands = parser.add_subparsers(dest="command")


    # Для команды analyze
    parse_convert = commands.add_parser("analyze")
    parse_convert.add_argument("files")
    parse_convert.add_argument("--format", dest="format", required=True)
    parse_convert.add_argument("--output", dest="to_unit", required=False)

    # Аргументы парсера
    args = parser.parse_args()
    return args

