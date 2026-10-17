import pytest

from streamstats.errors import (
    InvalidEventError,
    InvalidEventLevelError,
    InvalidEventSourceError,
    InvalidEventTimestampError,
)
from streamstats.parsers import parse_csv, parse_jsonl


# Успешные запуски

# Полный файл
@pytest.mark.parametrize(
    "file_format, parser", [
        ("jsonl", parse_jsonl),
        ("csv", parse_csv),
    ])
def test_valid_file(file_format, parser):
    result = list(parser(
        path=f"tests/test_data/events.{file_format}",
        skip_invalid=False,
        file_number=1,
        stats={}))
    assert len(result) == 3
    assert result[0]["source"] == "api" or result[0]["source"] == "app"


# Пустой файл
@pytest.mark.parametrize(
    "file_format, parser", [
        ("jsonl", parse_jsonl),
        ("csv", parse_csv),
    ])
def test_empty_file(file_format, parser):
    result = list(parser(
        path=f"tests/test_data/empty.{file_format}",
        skip_invalid=False,
        file_number=1,
        stats={}
        ))
    assert result == []


# Есть невалидные строки, --skip-invalid
@pytest.mark.parametrize(
    "file_format, parser", [
        ("jsonl", parse_jsonl),
        ("csv", parse_csv),
    ])
def test_skip_invalid(file_format, parser):
    stats = {"invalid_events": 0}
    result = list(parser(
        path=f"tests/test_data/invalid.{file_format}",
        skip_invalid=True,
        file_number=1,
        stats=stats
        ))
    assert len(result) == 2
    assert stats["invalid_events"] == 1


# Неуспешные запуски


# Неправильные поля у события
@pytest.mark.parametrize(
    "filename, error", [
        ("invalid_timestamp.jsonl", InvalidEventTimestampError),
        ("invalid_level.jsonl", InvalidEventLevelError),
        ("invalid_source.jsonl", InvalidEventSourceError),
    ])
def test_invalid_fields(filename, error):
    with pytest.raises(error, match="Invalid event"):
        list(parse_jsonl(
            path=f"tests/test_data/{filename}",
            skip_invalid=False,
            file_number=1,
            stats={}
            ))


# Неправильное событие
def test_invalid_json():
    with pytest.raises(InvalidEventError, match="line number: 2"):
        list(parse_jsonl(
            path="tests/test_data/invalid.jsonl",
            skip_invalid=False,
            file_number=1,
            stats={}
            ))
