# Программирование на языке Python. Лабораторная работа №2.

## Работа программы

Программа: Python-пакет с CLI, читающий события из CSV и JSONL и создающий статистический отчёт.

### Для пользователя:
Стандартные команды для терминала:
**Использование только в корневом каталоге проекта**
```bash
python -m streamstats analyze INPUT --format jsonl csv
python -m streamstats analyze INPUT1 INPUT2 --format jsonl csv --output OUTPUT
python -m streamstats analyze INPUT --format csv --skip-invalid
python -m streamstats analyze --help
```

### Для разработчика:
Установка пакетов:
```bash
pip install ".[dev]"
```
Команды тестирования:
```bash
python -m pytest
ruff check .
```
### Анализатор поддерживает:

- Анализ нескольких файлов.
- Файлы `.csv` и `.jsonl`.
- Для .csv: Разделители: `,`, `;`, `TAB`.
- Пропуск неправильных событий при `--skip-invalid`.
- Даты в формате `ISO 8601`.
- Уровни `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.

### Статистический отчет включает в себя:

- Общее количество событий.
- Количество событий по уровню.
- Количество событий по источнику.
- Топ 5 источников событий уровня `ERROR` и `CRITICAL`.


### Возможные ошибки:

#### Ошибки Анализатора (StreamStatsError):

- `UnsupportedFormatError` - Файл имеет неподдерживаемое расширение
- `WrongFormatError` - Указан неправильный формат файла в `--fomat`
- `InvalidEventError` - Неправильное событие
- `InvalidEventLevelError` - Неправильный уровень события
- `InvalidEventSourceError` - Неправильный источник события
- `InvalidEventMessageError` - Неправильное сообщение события
- `InvalidEventTimestampError` - Неправильное время события
- `ReportFileError` - Ошибка при сохранении статистического отчета
- `InvalidDelimeterError` - Неверный разделитель у csv файла
- `InvalidCLIArgumentsError` - Неверные аргументы для CLI

## Структура проекта

```text
lab_01/
  src/streamstats/
    __init__.py
    __main__.py
    analysis.py
    constants.py
    errors.py
    parsers.py
    report.py
  tests/
    test_data/
      empty.csv
      empty.jsonl
      events.csv
      events.jsonl
      invalid_level.jsonl
      invalid_source.jsonl
      invalid_timestamp.jsonl
      invalid.csv
      invalid.jsonl
      top5.jsonl
    __init__.py
    test_analysis.py
    test_cli.py
    test_parser.py
  .gitignore
  pyproject.toml
  pytest.ini
  README.md
```

### Модули проекта

#### Системный модуль
- **pyproject.toml** - Системная информация, модули, метаданные
- **README.md** - Описание работы программы, методик, инструкция по запуску

#### Основной модуль
- **__main__.py** - Основной вход и выход программы, содержится основная логика
- **parsers.py** - Содержит функции парсинга файлов, создания события, валидации события
- **analysis.py** - Содержится логика обновления статистики
- **constants.py** - Содержит константы
- **report.py** - Содержит логику сохранения отчета

#### Тестирование ДОПИСАТЬ ДОПИСАТЬ
- **test_data** - Папка с файлами для тестирования
- **test_analysis** - Тестирование анализатора
- **test_cli** - Тестирование CLI
- **test_parsers** - Тестирование парсеров

## Методика

### Считываение аргументов
1. Происходит считывание аргументов из командной строки с помощью argparse
2. Происходит анализ аргументов
- При ошибке argparse, выводится ошибка `IndvalidCLIArgumetsError`
- Если присутствует `--help` то выводится help

### Создание статистики

1. Происходит анализ файла
- В зависимости от расширения файла, запускается определенный модуль parser
- Если есть ошибка: Вызывается дочерний класс от StreamstatsError, программа завершается с кодом 2
2. Происходит построчный анализ файла
- Событие проходит валидацию, yield события
- Если есть ошибка: Вызывается дочерний класс от StreamstatsError, программа завершается с кодом 2
3. Событие обновляет статистику:
- В зависимости от того, что содержится в событии, статистика обновляется
4. Итоговая статистика проходит обработку на top-k источников событий с уровнями `CRITICAL` и `ERROR`
5. Происходит обработка вывода статистики в зависимости от `--output`
- Если есть ошибка: Вызывается дочерний класс от StreamstatsError, программа завершается с кодом 2
6. Вывод статистики

## Инструкция по установке

Скопировать директорию:
```bash
git clone https://github.com/levkorr/MAI_COURSE1_PYTHON_LAB2 lab_02
cd lab_02
```

Создать виртуальное окружение:
``` bash
python -m venv venv
venv/scripts/activate
```
Установить streamstats:
``` bash
pip install .
```
