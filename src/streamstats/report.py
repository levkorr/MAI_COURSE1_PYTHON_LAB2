import json
import pathlib
import copy

from .analysis import analyze
from .constants import STATS, SUPPORTED_FORMATS, TOP_K
from .errors import UnsupportedFormatError, WrongFormatError
from .parsers import parse_csv, parse_jsonl


def report(inputs, skip_invalid, formats):
    stats = copy.deepcopy(STATS)

    for file_number, file in enumerate(inputs):
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

    return json.dumps(stats, indent=4)