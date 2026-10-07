import json
import pathlib
import csv

from .analysis import analyze, invalid_analyze
from .constants import DATA
from .constants import TOP_K
from .errors import InvalidEventError, WrongFormatError, UnsupportedFormatError, EmptyFileError

invalid_lines = 0
invalid_files = 0


def make_event(data):
    return {
        "timestamp": data.get("timestamp"),
        "level": data.get("level"),
        "source": data.get("source"),
        "message": data.get("message")
    }


def parse_jsonl(path, skip_invalid, file_number):
    with open(path, "r", encoding="utf-8") as file:
        line_number = 0
        for line in file:
            line_number += 1

            if not line.strip():
                continue
            try:
                data = json.loads(line)
                yield make_event(data)
            except Exception:
                if skip_invalid:
                    global invalid_lines
                    invalid_lines += 1
                else:
                    raise InvalidEventError(file_number, line_number)


def parse_csv(path, skip_invalid, file_number):
    with open(path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        line_number = 0

        for line in reader:
            line_number += 1

            try:
                yield make_event(line)
            except Exception:
                if skip_invalid:
                    print("Hello")
                else:
                    raise InvalidEventError(file_number, line_number)


def full_parse(inputs, skip_invalid, format):
    global invalid_lines
    global invalid_files
    data = DATA
    file_number = 0

    for file in inputs:
        file_number += 1
        path = pathlib.Path(file)

        if path.stat().st_size == 0:
            if skip_invalid:
                invalid_files += 1
            else:
                raise EmptyFileError(file)

        if path.suffix.strip(".") not in format:
            raise WrongFormatError(path.suffix.strip("."))

        if path.suffix == ".jsonl":
            for event in parse_jsonl(path, skip_invalid, file_number):
                data = analyze(event, data)

        elif path.suffix == ".csv":
            for event in parse_csv(path, skip_invalid, file_number):
                data = analyze(event, data)

    data["top_error_sources"] = dict(
        sorted(
            data["top_error_sources"].items(),
            key=lambda item: (-item[1], item[0])
        )[:TOP_K])

    invalid_analyze(data, skip_invalid, invalid_lines, invalid_files)

    return json.dumps(data, indent=4)
