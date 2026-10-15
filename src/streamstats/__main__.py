import argparse
import contextlib
import copy
import io
import json
import pathlib
import sys

from .analysis import analyze
from .constants import STATS, SUPPORTED_FORMATS, TOP_K
from .errors import (
    InvalidCLIArgumentsError,
    StreamStatsError,
    UnsupportedFormatError,
    WrongFormatError,
)
from .parsers import parse_csv, parse_jsonl
from .report import report


def parse_help():
    ''' Модуль выводящий help при аргументе --help

    Args:
        None

    Returns:
        None
    '''
    if "--help" in sys.argv:
        print("""
        Streamstats - csv and jsonl file streaming analyzer

        Commands:
            analyze                     Main command for file analysis

        Arguments:
            INPUT [INPUT, ...]          Input file paths
        
        Options:
            --format FORMAT [FORMAT, ...]       File formats (required)
            --output FILE                       Save JSON report to FILE
                                                (if is not present, prints to terminal)
            --skip-invalid                      Skip invalid events instead of stopping
        
        Support:
            Analysis of multiple files
            CSV and JSONL files
            CSV delimiters: ',', ';', TAB
            ISO 8601 timestamps
            Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

        Stats:
            Total number of events
            Number of events by level
            Number of events by source
            Top-k ERROR/CRITICAL sources
            First and last timestamps
            Number of invalid lines (for --skip-invalid)
    
        Examples of working programs:
            python -m streamstats analyze INPUT --format jsonl csv
            python -m streamstats analyze INPUT1 INPUT2 --format jsonl csv --output REPORT.json
            python -m streamstats analyze INPUT --format csv --skip-invalid
        """)
        sys.exit(0)


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
    ''' Являетсе единственным входом и выходом программы
    Обрабатывает ввод в CLI, входные аргументы
    Отвечает за запуск нужных функций
    Хранит основную логику analyze

    Args:
        None

    Returns:
        None

    Raises:
        StreamstatsError: При ожидаемой ошибке
    '''
    parse_help()
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            args = parse()
    except SystemExit:
        raise InvalidCLIArgumentsError()
    if args.command == "analyze":
        # Чтение аргументов
        inputs = args.inputs
        formats = args.formats
        report_path = args.report_path
        skip_invalid = args.skip_invalid

        # Запуск парсера
        stats = copy.deepcopy(STATS)

        for file_number, file in enumerate(inputs, start=1):
            path = pathlib.Path(file)
            file_format = path.suffix.strip(".")

            if file_format not in formats and file_format in SUPPORTED_FORMATS:
                raise WrongFormatError(path.suffix.strip("."))

            if file_format == "jsonl":
                for event in parse_jsonl(path, skip_invalid, file_number, stats):
                    stats = analyze(event, stats)
            elif file_format == "csv":
                for event in parse_csv(path, skip_invalid, file_number, stats):
                    stats = analyze(event, stats)

            else:
                raise UnsupportedFormatError(file_format)

        stats["top_error_sources"] = dict(
            sorted(
                stats["top_error_sources"].items(),
                key=lambda item: (-item[1], item[0])
            )[:TOP_K])

        if not skip_invalid:
            stats.pop("invalid_lines", None)

        stats = json.dumps(stats, indent=4)

        report(stats, report_path)


if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except StreamStatsError as e:
        print(f"Expected error: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(2)
