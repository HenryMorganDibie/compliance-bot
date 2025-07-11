import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import sys
import os
import json
import pandas as pd
from datetime import datetime
from notifications.slack_bot import send_slack_alert

# -----------------------------
# 📁 Add root to path (for imports)
# -----------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# -----------------------------
# 🗂 File Config
# -----------------------------
DATA_FILE = "data/filing_schedule.json"

# -----------------------------
# 📦 Load Data
# -----------------------------
def load_filings():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# -----------------------------
# 🧠 Utility Functions
# -----------------------------
def get_days_left(due_date):
    due = pd.to_datetime(due_date)
    today = pd.Timestamp.now().normalize()
    return (due - today).days

# -----------------------------
# 🔔 Check Filings and Alert
# -----------------------------
def check_and_alert():
    print("📡 Running compliance alert scan...")
    filings = load_filings()
    alerts_sent = 0

    for filing in filings:
        if filing.get("completed", False):
            continue

        days_left = get_days_left(filing["due_date"])
        print(f"🔍 Checking '{filing['filing_name']}' — {days_left} day(s) left")

        if days_left < 0:
            message = (
                f"🚨 *{filing['filing_name']}* is OVERDUE!\n"
                f"Due: {filing['due_date']} — Contact: {filing['escalation_contact']}"
            )
            send_slack_alert(message)
            alerts_sent += 1

        elif days_left == 0:
            message = (
                f"⚠️ *{filing['filing_name']}* is due TODAY!\n"
                f"Jurisdiction: {filing['jurisdiction']} — Contact: {filing['escalation_contact']}"
            )
            send_slack_alert(message)
            alerts_sent += 1

        elif days_left <= 2:
            message = (
                f"🕒 *{filing['filing_name']}* is due in {days_left} day(s).\n"
                f"Type: {filing['filing_type']} — Contact: {filing['escalation_contact']}"
            )
            send_slack_alert(message)
            alerts_sent += 1

    if alerts_sent == 0:
        print("✅ No urgent filings found.")
    else:
        print(f"📨 {alerts_sent} alert(s) sent to Slack.")

# -----------------------------
# 🔧 CLI Entry Point
# -----------------------------
if __name__ == "__main__":
    check_and_alert()
