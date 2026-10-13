import pathlib

from .errors import ReportFileError


def report(stats, report_path):
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
            pathlib.Path("reports").mkdir(exist_ok=True)
            with open(f"reports/{report_path}", "w", encoding="utf-8") as file:
                file.write(stats)
        except OSError:
            raise ReportFileError(report_path)
    else:
        print(stats)
