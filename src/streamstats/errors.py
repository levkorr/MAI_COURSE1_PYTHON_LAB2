class StreamStatsError(Exception):
    pass

class UnsupportedFormatError(StreamStatsError):
    def __init__(self, format):
        super().__init__(f"Unsupported format: {format}")

class WrongFormatError(StreamStatsError):
    def __init__(self, format):
        super().__init__(f"Wrong format: you didnt mention {format}")

class InvalidEventError(StreamStatsError):
    def __init__(self, file_number, line_number):
        super().__init__(f"Invalid event: file number: {file_number}, line number: {line_number}")
    