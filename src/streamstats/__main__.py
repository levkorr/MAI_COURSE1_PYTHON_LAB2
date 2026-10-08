from .parsers import *
import sys
from .errors import StreamStatsError, FileAccessError
import pathlib
import argparse
from .report import report

# python -m streamstats analyze data/events.jsonl data/events.csv --format jsonl csv
# python -m streamstats analyze data/empty.jsonl data/events_comma.csv data/events_copy.jsonl data/events_semicolon.csv data/events_tab.csv data/events.jsonl data/invalid_events.jsonl --format jsonl csv --skip-invalid --output report.json

def parse_help():
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
                                                (by default saves to )
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
    parse_help()
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
                    sys.exit(0)
            except Exception:
                raise FileAccessError(report_path)
        else:
            print(data)
            sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except StreamStatsError as e:
        print(f"Expected error: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(2)