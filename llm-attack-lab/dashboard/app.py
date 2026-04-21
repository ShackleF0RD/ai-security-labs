import json
from pathlib import Path

import pandas as pd
import streamlit as st

LOG_FILE = Path("logs/events.jsonl")

st.set_page_config(page_title="AI Security Lab Dashboard", layout="wide")
st.title("AI Security Lab - Attack Success Rate Dashboard")


def load_jsonl(path: Path):
    rows = []
    if not path.exists():
        return rows

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return rows


def load_events():
    events = load_jsonl(LOG_FILE)
    if not events:
        return pd.DataFrame()

    flat_rows = []
    for event in events:
        row = {
            "timestamp": event.get("timestamp"),
            "event_type": event.get("event_type"),
        }

        data = event.get("data", {})
        if isinstance(data, dict):
            for k, v in data.items():
                row[k] = str(v)

        flat_rows.append(row)

    return pd.DataFrame(flat_rows)


def classify_auto_tests(df: pd.DataFrame):
    if df.empty:
        return {
            "total_attacks": 0,
            "blocked_attacks": 0,
            "allowed_attacks": 0,
            "total_benign": 0,
            "blocked_benign": 0,
            "answered_benign": 0,
            "attack_success_rate": 0.0,
        }

    attack_df = df[df["event_type"] == "auto_attack"].copy()
    benign_df = df[df["event_type"] == "auto_benign"].copy()

    def is_blocked(val):
        return str(val).lower() == "true"

    blocked_attacks = attack_df["blocked"].apply(is_blocked).sum() if "blocked" in attack_df else 0
    total_attacks = len(attack_df)
    allowed_attacks = total_attacks - blocked_attacks

    blocked_benign = benign_df["blocked"].apply(is_blocked).sum() if "blocked" in benign_df else 0
    total_benign = len(benign_df)
    answered_benign = total_benign - blocked_benign

    attack_success_rate = (allowed_attacks / total_attacks * 100) if total_attacks else 0.0

    return {
        "total_attacks": int(total_attacks),
        "blocked_attacks": int(blocked_attacks),
        "allowed_attacks": int(allowed_attacks),
        "total_benign": int(total_benign),
        "blocked_benign": int(blocked_benign),
        "answered_benign": int(answered_benign),
        "attack_success_rate": round(attack_success_rate, 2),
    }


df = load_events()
metrics = classify_auto_tests(df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Attacks", metrics["total_attacks"])
col2.metric("Blocked Attacks", metrics["blocked_attacks"])
col3.metric("Allowed Attacks", metrics["allowed_attacks"])
col4.metric("Attack Success Rate", f"{metrics['attack_success_rate']}%")

col5, col6, col7 = st.columns(3)
col5.metric("Benign Tests", metrics["total_benign"])
col6.metric("Benign Answered", metrics["answered_benign"])
col7.metric("Benign Blocked", metrics["blocked_benign"])

st.subheader("Attack Results Overview")
chart_df = pd.DataFrame(
    {
        "Category": ["Blocked Attacks", "Allowed Attacks", "Benign Answered", "Benign Blocked"],
        "Count": [
            metrics["blocked_attacks"],
            metrics["allowed_attacks"],
            metrics["answered_benign"],
            metrics["blocked_benign"],
        ],
    }
)
st.bar_chart(chart_df.set_index("Category"))

st.subheader("Recent Logged Events")
if df.empty:
    st.info("No events found yet. Run auto_attack.py first.")
else:
    st.dataframe(df.tail(25), use_container_width=True)