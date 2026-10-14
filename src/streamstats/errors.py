class StreamStatsError(Exception):
    pass


class UnsupportedFormatError(StreamStatsError):
    def __init__(self, format):
        super().__init__(f"Unsupported format: {format}")


class WrongFormatError(StreamStatsError):
    def __init__(self, format):
        super().__init__(f"Wrong format: you didn't mention {format}")


class InvalidEventError(StreamStatsError):
    def __init__(self, file_number, line_number):
        super().__init__(
            f"Invalid event: file number: {file_number}, line number: {line_number}")


class InvalidEventTimestampError(StreamStatsError):
    def __init__(self, file_number, line_number):
        super().__init__(
            f"Invalid event timestamp: file number: {file_number}, line number: {line_number}")


class InvalidEventLevelError(StreamStatsError):
    def __init__(self, file_number, line_number):
        super().__init__(
            f"Invalid event level: file number: {file_number}, line number: {line_number}")


class InvalidEventSourceError(StreamStatsError):
    def __init__(self, file_number, line_number):
        super().__init__(
            f"Invalid event source: file number: {file_number}, line number: {line_number}")


class InvalidEventMessageError(StreamStatsError):
    def __init__(self, file_number, line_number):
        super().__init__(
            f"Invalid event message: file number: {file_number}, line number: {line_number}")


class ReportFileError(StreamStatsError):
    def __init__(self, report_path):
        super().__init__(f"Can't write report to file: {report_path}")


class InvalidDelimiterError(StreamStatsError):
    def __init__(self, file_number):
        super().__init__(f"Invalid Delimiter: file number: {file_number}")

class InvalidCLIArgumentsError(StreamStatsError):
        def __init__(self):
            super().__init__(f"Invalid arguments, try:\n\npython -m streamstats --help")