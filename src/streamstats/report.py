import pathlib
import json

from .constants import DATA, SUPPORTED_FORMATS, TOP_K
from .errors import WrongFormatError, UnsupportedFormatError
from .parsers import parse_csv, parse_jsonl
from .analysis import analyze, invalid_analyze

invalid_lines = 0

def report(inputs, skip_invalid, formats):
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