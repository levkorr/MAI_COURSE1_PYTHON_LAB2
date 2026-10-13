from datetime import datetime


def analyze(event, stats):
    ''' Анализирует данные из события для создания статистики

    Args:
        event: Анализируемое событие
        stats: Промежуточная статистика

    Returns:
        stats: Промежуточная статистика
    '''
    stats["total_events"] += 1
    stats["by_level"][event["level"]] += 1
    if event["level"] == "ERROR" or event["level"] == "CRITICAL":
        if event["source"] in stats["top_error_sources"]:
            stats["top_error_sources"][event["source"]] += 1
        else:
            stats["top_error_sources"][event["source"]] = 1

    if event["source"] in stats["by_source"]:
        stats["by_source"][event["source"]] += 1
    else:
        stats["by_source"][event["source"]] = 1

    if stats["first_timestamp"] == "":
        stats["first_timestamp"] = event["timestamp"]
        stats["last_timestamp"] = event["timestamp"]
    else:
        if datetime.fromisoformat(event["timestamp"]) < datetime.fromisoformat(stats["first_timestamp"]):
            stats["first_timestamp"] = event["timestamp"]
        elif datetime.fromisoformat(event["timestamp"]) > datetime.fromisoformat(stats["last_timestamp"]):
            stats["last_timestamp"] = event["timestamp"]
    return stats
