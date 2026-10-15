import copy

import pytest

from streamstats.analysis import analyze
from streamstats.constants import STATS


def event(level="INFO", source="app", timestamp="2026-01-01T10:00:00"):
    return {"timestamp": timestamp, "level": level, "source": source, "message": "Привет"}


def test_empty_statistics():
    stats = copy.deepcopy(STATS)
    assert stats["total_events"] == 0
    assert stats["by_source"] == {}
    assert stats["top_error_sources"] == {}


def test_one_event():
    stats = copy.deepcopy(STATS)
    stats = analyze(event(), stats)
    assert stats["total_events"] == 1
    assert stats["by_level"]["INFO"] == 1
    assert stats["by_source"]["app"] == 1


@pytest.mark.parametrize("level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
def test_levels(level):
    stats = copy.deepcopy(STATS)
    stats = analyze(event(level), stats)
    assert stats["by_level"][level] == 1
    assert stats["top_error_sources"] == ({"app": 1} if level in ("ERROR", "CRITICAL") else {})


def test_first_and_last_timestamp():
    stats = copy.deepcopy(STATS)
    for timestamp in ["2026-01-03T00:00:00", "2026-01-01T00:00:00", "2026-01-02T00:00:00"]:
        analyze(event(timestamp=timestamp), stats)
    assert stats["first_timestamp"] == "2026-01-01T00:00:00"
    assert stats["last_timestamp"] == "2026-01-03T00:00:00"


def test_sources_and_errors():
    stats = copy.deepcopy(STATS)
    for item in [event("ERROR", "api"), event("CRITICAL", "api"), event("INFO", "web")]:
        analyze(item, stats)
    assert stats["total_events"] == 3
    assert stats["by_source"] == {"api": 2, "web": 1}
    assert stats["top_error_sources"] == {"api": 2}
