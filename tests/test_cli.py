import json
import sys

import pytest

from streamstats.__main__ import main
from streamstats.errors import InvalidEventError

# Успешные запуски

def test_cli_valid_jsonl(capsys):
    sys.argv = ["streamstats", "analyze",
                "tests/test_data/events.jsonl", "--format", "jsonl"]
    main()
    result = json.loads(capsys.readouterr().out)
    assert result["total_events"] == 3
    assert result["by_level"]["ERROR"] == 1
    assert result["by_source"]["api"] == 2


def test_cli_valid_csv(capsys):
    sys.argv = ["streamstats", "analyze",
                "tests/test_data/events.csv", "--format", "csv"]
    main()
    result = json.loads(capsys.readouterr().out)
    assert result["total_events"] == 3
    assert result["by_level"]["CRITICAL"] == 1


def test_cli_multiple_files(capsys):
    sys.argv = ["streamstats", "analyze", "tests/test_data/events.jsonl",
                "tests/test_data/events.csv", "--format", "jsonl", "csv"]
    main()
    result = json.loads(capsys.readouterr().out)
    assert result["total_events"] == 6
    assert result["by_source"] == {"app": 2, "api": 3, "db": 1}


def test_cli_empty_file(capsys):
    sys.argv = ["streamstats", "analyze",
                "tests/test_data/empty.jsonl", "--format", "jsonl"]
    main()
    assert json.loads(capsys.readouterr().out)["total_events"] == 0


def test_cli_skip_invalid(capsys):
    sys.argv = ["streamstats", "analyze", "tests/test_data/invalid.jsonl",
                "--format", "jsonl", "--skip-invalid"]
    main()
    result = json.loads(capsys.readouterr().out)
    assert result["total_events"] == 2
    assert result["invalid_lines"] == 1


def test_cli_top_5(capsys):
    sys.argv = ["streamstats", "analyze",
                "tests/test_data/top5.jsonl", "--format", "jsonl"]
    main()
    result = json.loads(capsys.readouterr().out)
    assert list(result["top_error_sources"]) == ["a", "b", "c", "d", "e"]


# Неуспешные запуски

def test_cli_invalid_line():
    sys.argv = ["streamstats", "analyze",
                "tests/test_data/invalid.jsonl", "--format", "jsonl"]
    with pytest.raises(InvalidEventError, match="line number: 2"):
        main()


def test_cli_help(capsys):
    sys.argv = ["streamstats", "--help"]
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == 0
    assert "Streamstats - csv and jsonl file streaming analyzer" in capsys.readouterr().out
