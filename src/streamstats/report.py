import pathlib
import sys

from .errors import FileAccessError


def report(stats, report_path):
    if report_path:
        try:
            pathlib.Path("reports").mkdir(exist_ok=True)
            with open(f"reports/{report_path}", "w", encoding="utf-8") as file:
                file.write(stats)
                sys.exit(0)
        except OSError:
            raise FileAccessError(report_path)
    else:
        print(stats)
