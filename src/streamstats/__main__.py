from .parsers import *
import sys
from .errors import StreamStatsError, FileAccessError
import pathlib
import argparse
from .report import report
# python -m streamstats analyze INPUT [INPUT ...] --format csv|jsonl --output REPORT.json
# python -m streamstats analyze INPUT --format jsonl --skip-invalid

# python -m streamstats analyze data/events.jsonl data/events.csv --format jsonl csv


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
        usage="streamstats <command> [arguments]",
        add_help=False
    )
    commands = parser.add_subparsers(dest="command")

    # Для команды analyze
    parse_analyze = commands.add_parser("analyze")
    parse_analyze.add_argument("inputs", nargs="+")
    parse_analyze.add_argument(
        "--format", dest="formats", nargs="+", required=True)
    parse_analyze.add_argument("--output", dest="report_path", required=False)
    parse_analyze.add_argument("--skip-invalid", action="store_true")

    # Аргументы парсера
    args = parser.parse_args()
    return args


def main():
    args = parse()
    if args.command == "analyze":
        # Чтение аргументов
        inputs = args.inputs
        formats = args.formats
        report_path = args.report_path
        skip_invalid = args.skip_invalid
        # Запуск парсера
        data = report(inputs, skip_invalid, formats)
        # Вывод в терминал или в определенное место
        if report_path:
            try:
                pathlib.Path("reports").mkdir(exist_ok=True)
                with open(f"reports/{report_path}", "w", encoding="utf-8") as file:
                    file.write(data)
            except Exception:
                raise FileAccessError(report_path)
        else:
            print(data)


if __name__ == "__main__":
    try:
        main()
    except StreamStatsError as e:
        print(f"Expected error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
