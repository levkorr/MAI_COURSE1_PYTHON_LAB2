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


class FileAccessError(StreamStatsError):
    def __init__(self, report_path):
        super().__init__(f"Can't access file: {report_path}")


class InvalidDelimeterError(StreamStatsError):
    def __init__(self, file_number):
        super().__init__(f"Invalid Delimeter: file number: {file_number}")
