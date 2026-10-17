import pathlib

from .errors import ReportFileError


def report(stats, report_path, inputs):
    ''' Обрабатывает вывод статистики

    Args:
        stats: Итоговая статистика
        report_path: Название файла в который будет загружена статистика

    Returns:
        None

    Raises:
        ReportFileError: Если неполучилось записать файл
    '''
    if report_path:
        try:
            output = pathlib.Path(report_path)
            output = output.resolve()
            for input in inputs:
                input = pathlib.Path(input)
                input = input.resolve()
                if output==input:
                    raise ReportFileError(report_path)

            output.parent.mkdir(parents=True, exist_ok=True)

            with open(output, "w", encoding="utf-8") as file:
                file.write(stats)
        except OSError:
            raise ReportFileError(report_path)
    else:
        print(stats)
