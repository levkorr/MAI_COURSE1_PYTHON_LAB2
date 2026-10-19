import json
import subprocess
import sys

import pytest

from streamstats.__main__ import main
from streamstats.errors import InvalidEventError

# Integration test CLI с временным каталогом.


def test_cli_integration_valid(tmp_path):
    input_file = tmp_path / "events.jsonl"

    event = {"timestamp": "2026-01-01T12:00:00", "level": "ERROR",
             "source": "api", "message": "Ошибка сервера"}

    with input_file.open("w", encoding="utf-8") as file:
        json.dump(event, file, ensure_ascii=False)

    output_file = tmp_path / "report.json"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "streamstats",
            "analyze",
            str(input_file),
            "--format",
            "jsonl",
            "--output",
            str(output_file)
        ],
        capture_output=True,
        check=False,
        text=True,
        encoding="utf-8"
    )

    assert result.returncode == 0
    assert output_file.exists()

    stats = json.loads(output_file.read_text(encoding="utf-8"))

    assert stats["total_events"] == 1
    assert stats["by_level"]["ERROR"] == 1
    assert stats["by_source"]["api"] == 1
    assert stats["top_error_sources"] == {"api": 1}
    assert stats["first_timestamp"] == "2026-01-01T12:00:00"
    assert stats["last_timestamp"] == "2026-01-01T12:00:00"

    saved_event = json.loads(input_file.read_text(encoding="utf-8"))

    assert saved_event == event


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
    assert result["invalid_events"] == 1


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
