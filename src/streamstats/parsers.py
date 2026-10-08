import json
import pathlib
import csv
from datetime import datetime

from .analysis import analyze, invalid_analyze
from .constants import DATA
from .constants import TOP_K, SUPPORTED_FORMATS, LEVELS
from .errors import InvalidEventError, WrongFormatError, UnsupportedFormatError, InvalidEventLevelError, InvalidEventMessageError, InvalidEventSourceError, InvalidEventTimestampError

invalid_lines = 0


def validate_event(data, file_number, line_number):
    raw_timestamp = data.get("timestamp")
    raw_level = data.get("level")
    raw_source = data.get("source")
    raw_message = data.get("message")

    # timestamp
    try:
        datetime.fromisoformat(raw_timestamp)
    except (ValueError, TypeError):
        raise InvalidEventTimestampError(file_number, line_number)
    # level
    if raw_level not in LEVELS:
        raise InvalidEventLevelError(file_number, line_number)
    # source
    if not isinstance(raw_source, str) or not raw_source.strip():
        raise InvalidEventSourceError(file_number, line_number)
    # message
    if not isinstance(raw_message, str) or not raw_message.strip():
        raise InvalidEventMessageError(file_number, line_number)


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
        global invalid_lines
        for line in file:
            line_number += 1

            if not line.strip():
                continue
            try:
                data = json.loads(line)
                validate_event(data, file_number, line_number)
                yield make_event(data)
            except Exception:
                if skip_invalid:
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


def full_parse(inputs, skip_invalid, formats):
    global invalid_lines
    data = DATA
    file_number = 0

    for file in inputs:
        file_number += 1
        path = pathlib.Path(file)
        file_format = path.suffix.strip(".")
        if file_format not in formats and file_format in SUPPORTED_FORMATS:
            raise WrongFormatError(path.suffix.strip("."))
        if file_format == "jsonl":
            for event in parse_jsonl(path, skip_invalid, file_number):
                data = analyze(event, data)

        elif file_format == "csv":
            for event in parse_csv(path, skip_invalid, file_number):
                data = analyze(event, data)
        else:
            raise UnsupportedFormatError(file_format)
    data["top_error_sources"] = dict(
        sorted(
            data["top_error_sources"].items(),
            key=lambda item: (-item[1], item[0])
        )[:TOP_K])

    invalid_analyze(data, skip_invalid, invalid_lines)

    return json.dumps(data, indent=4)
