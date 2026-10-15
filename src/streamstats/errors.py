class StreamStatsError(Exception):
    "Родительский класс всех ошибок модуля streamstats"
    pass


class UnsupportedFormatError(StreamStatsError):
    "Неподдерживаемый формат файла"
    def __init__(self, format):
        super().__init__(f"Unsupported format: {format}")


class WrongFormatError(StreamStatsError):
    "Указан неправильный формат файла"
    def __init__(self, format):
        super().__init__(f"Wrong format: you didn't mention {format}")


class InvalidEventError(StreamStatsError):
    "Неверное событие"
    def __init__(self, file_number, line_number):
        super().__init__(
            f"Invalid event: file number: {file_number}, line number: {line_number}")


class InvalidEventTimestampError(StreamStatsError):
    "Неверное время события"
    def __init__(self, file_number, line_number):
        super().__init__(
            f"Invalid event timestamp: file number: {file_number}, line number: {line_number}")


class InvalidEventLevelError(StreamStatsError):
    "Неверный уровень события"
    def __init__(self, file_number, line_number):
        super().__init__(
            f"Invalid event level: file number: {file_number}, line number: {line_number}")


class InvalidEventSourceError(StreamStatsError):
    "Неверный источник события"
    def __init__(self, file_number, line_number):
        super().__init__(
            f"Invalid event source: file number: {file_number}, line number: {line_number}")


class InvalidEventMessageError(StreamStatsError):
    "Неверное сообщение события"
    def __init__(self, file_number, line_number):
        super().__init__(
            f"Invalid event message: file number: {file_number}, line number: {line_number}")


class ReportFileError(StreamStatsError):
    "Ошибка при выводе статистики в файл"
    def __init__(self, report_path):
        super().__init__(f"Can't write report to file: {report_path}")


class InvalidDelimiterError(StreamStatsError):
    "Неверный разделитель в CSV"
    def __init__(self, file_number):
        super().__init__(f"Invalid Delimiter: file number: {file_number}")

class InvalidCLIArgumentsError(StreamStatsError):
    "Неверные аргументы CLI"
    def __init__(self):
        super().__init__("Invalid arguments, try:\n\npython -m streamstats --help")
