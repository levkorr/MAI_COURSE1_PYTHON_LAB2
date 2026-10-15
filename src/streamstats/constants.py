TOP_K = 5
SUPPORTED_FORMATS = ["csv", "jsonl"]
LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
STATS = {
    "total_events": 0,
    "by_level": {
        "CRITICAL": 0,
        "DEBUG": 0,
        "ERROR": 0,
        "INFO": 0,
        "WARNING": 0
    },
    "by_source": {
    },
    "top_error_sources": {
    },
    "first_timestamp": "",
    "last_timestamp": "",
    "invalid_events": 0
}
