from datetime import datetime

def analyze(event, data):
    data["total_events"] += 1
    data["by_level"][event["level"]] += 1
    if event["level"] == "ERROR" or event["level"] == "CRITICAL":
        if event["source"] in data["top_error_sources"]:
            data["top_error_sources"][event["source"]] += 1
        else:
            data["top_error_sources"][event["source"]] =1
    
    if event["source"] in data["by_source"]:
        data["by_source"][event["source"]] += 1
    else:
        data["by_source"][event["source"]] = 1

    if data["first_timestamp"] == "":
        data["first_timestamp"] = event["timestamp"]
        data["last_timestamp"] = event["timestamp"]
    else:
        if datetime.fromisoformat(event["timestamp"]) < datetime.fromisoformat(data["first_timestamp"]):
            data["first_timestamp"] = event["timestamp"]
        elif datetime.fromisoformat(event["timestamp"]) > datetime.fromisoformat(data["last_timestamp"]):
            data["last_timestamp"] = event["timestamp"]
    return data