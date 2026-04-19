import json
from datetime import datetime
import os

LOG_FILE = os.path.join("logs", "events.jsonl")

def log_event(event_type: str, data: dict):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "data": data
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")