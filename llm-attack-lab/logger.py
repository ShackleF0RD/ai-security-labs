import json
from datetime import datetime
import os

# Log file path.
# JSONL format means each event is stored as one JSON object per line.
LOG_FILE = os.path.join("logs", "events.jsonl")


def log_event(event_type: str, data: dict):
    # Make sure the logs directory exists before writing.
    os.makedirs("logs", exist_ok=True)

    # Build a structured event record.
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "data": data
    }

    # Append the event to the log file.
    # Each line is valid JSON, which makes it easy for the dashboard to read.
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")