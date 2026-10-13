import csv
import json
import logging
from datetime import datetime

from .constants import LEVELS
from .errors import InvalidDelimeterError, InvalidEventError

logger = logging.getLogger(__name__)


def validate_event(data, file_number, line_number):
    ''' Проводит валидацию события

    Args:
        data: Данные строки из файла
        file_number: Номер читаемого файла
        line_number: Номер читаемой строки из файла

    Returns:
        None

    Raises:
        InvalidEventError: Если событие неправильно
    '''
    raw_timestamp = data.get("timestamp")
    raw_level = data.get("level")
    raw_source = data.get("source")
    raw_message = data.get("message")

    # timestamp
    try:
        datetime.fromisoformat(raw_timestamp)
    except (ValueError, TypeError):
        raise InvalidEventError(file_number, line_number)
    # level
    if raw_level not in LEVELS:
        raise InvalidEventError(file_number, line_number)
    # source
    if not isinstance(raw_source, str) or not raw_source.strip():
        raise InvalidEventError(file_number, line_number)
    # message
    if not isinstance(raw_message, str):
        raise InvalidEventError(file_number, line_number)


def make_event(data):
    ''' Создает событие по данным

    Args:
        data: Данные строки из файла

    Returns:
        Словарь содержащий событие
    '''
    return {
        "timestamp": data.get("timestamp"),
        "level": data.get("level"),
        "source": data.get("source"),
        "message": data.get("message")
    }


def parse_jsonl(path, skip_invalid, file_number, stats):
    ''' Обрабатывает файл jsonl

    Args:
        path: Путь к файлу
        skip_invalid: Пропуск неправильного файла
        file_number: Номер читаемого файла
        stats: Итоговая статистика

    Returns:
        None

    Yields:
        make_event(data): Созданное событие из строки

    Raises:
        InvalidEventError: Если событие неправильно
    '''
    with open(path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file):

            try:
                data = json.loads(line)
                validate_event(data, file_number+1, line_number+1)
                yield make_event(data)
            except (InvalidEventError, json.JSONDecodeError):
                if skip_invalid:
                    stats["invalid_lines"] += 1
                    logger.warning(
                        f"Invalid Event: file number: {file_number+1}, line number: {line_number+1}")
                else:
                    raise InvalidEventError(file_number+1, line_number+1)


def parse_csv(path, skip_invalid, file_number, stats):
    ''' Обрабатывает файл csv

    Args:
        path: Путь к файлу
        skip_invalid: Пропуск неправильного файла
        file_number: Номер читаемого файла
        stats: Итоговая статистика

    Returns:
        None

    Yields:
        make_event(data): Созданное событие из строки

    Raises:
        InvalidDelimeterError: Если неправильный разделитель в файле
        InvalidEventError: Если событие неправильно
    '''
    with open(path, "r", encoding="utf-8", newline="") as file:

        try:
            sample = file.readline()
            if not sample:
                return
            file.seek(0)

            delimiter = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            raise InvalidDelimeterError(file_number)

        reader = csv.DictReader(file, dialect=delimiter)

        for line_number, data in enumerate(reader):

            try:
                validate_event(data, file_number+1, line_number+1)
                yield make_event(data)
            except InvalidEventError:
                if skip_invalid:
                    stats["invalid_lines"] += 1
                    logger.warning(
                        f"Invalid Event: file number: {file_number+1}, line number: {line_number+1}")
                else:
                    raise InvalidEventError(file_number+1, line_number+1)
