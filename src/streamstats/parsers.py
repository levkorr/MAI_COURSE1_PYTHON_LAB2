import json
import csv
from datetime import datetime
from . import constants

from .constants import LEVELS, INVALID_LINES
from .errors import InvalidEventError, InvalidEventLevelError, InvalidEventMessageError, InvalidEventSourceError, InvalidEventTimestampError


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
                    constants.INVALID_LINES += 1
                else:
                    raise InvalidEventError(file_number, line_number)


def parse_csv(path, skip_invalid, file_number):
    with open(path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        line_number = 0

        for line in reader:
            line_number += 1

            try:
                data = json.loads(line)
                validate_event(data, file_number, line_number)
                yield make_event(data)
            except Exception:
                if skip_invalid:
                    constants.INVALID_LINES += 1
                else:
                    raise InvalidEventError(file_number, line_number)
