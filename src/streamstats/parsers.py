import csv
import json
from datetime import datetime

from . import constants
from .constants import LEVELS
from .errors import InvalidDelimeterError, InvalidEventError


def validate_event(data, file_number, line_number):
    raw_timestamp = data.get("timestamp")
    raw_level = data.get("level")
    raw_source = data.get("source")
    raw_message = data.get("message")

    # timestamp
    try:
        datetime.fromisoformat(raw_timestamp)
    except (ValueError, TypeError):
        raise InvalidEventError(file_number, line_number)
    # level
    if raw_level not in LEVELS:
        raise InvalidEventError(file_number, line_number)
    # source
    if not isinstance(raw_source, str) or not raw_source.strip():
        raise InvalidEventError(file_number, line_number)
    # message
    if not isinstance(raw_message, str) or not raw_message.strip():
        raise InvalidEventError(file_number, line_number)


def make_event(data):
    return {
        "timestamp": data.get("timestamp"),
        "level": data.get("level"),
        "source": data.get("source"),
        "message": data.get("message")
    }


def parse_jsonl(path, skip_invalid, file_number):
    with open(path, "r", encoding="utf-8") as file:

        for line_number, line in enumerate(file):

            try:
                data = json.loads(line)
                validate_event(data, file_number, line_number)
                yield make_event(data)
            except (InvalidEventError, json.JSONDecodeError):
                if skip_invalid:
                    constants.INVALID_LINES += 1
                else:
                    raise InvalidEventError(file_number, line_number)


def parse_csv(path, skip_invalid, file_number):
    with open(path, "r", encoding="utf-8", newline="") as file:

        try:
            sample = file.read(1024)
            file.seek(0)

            delimiter = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            raise InvalidDelimeterError(file_number)

        reader = csv.DictReader(file, dialect=delimiter)

        for line_number, data in enumerate(reader):

            try:
                validate_event(data, file_number, line_number)
                yield make_event(data)
            except InvalidEventError:
                if skip_invalid:
                    constants.INVALID_LINES += 1
                else:
                    raise InvalidEventError(file_number, line_number)
