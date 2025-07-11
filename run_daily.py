import schedule
import time
import subprocess
import datetime
import os
import sys

# -----------------------------
# 🔧 Setup Paths (Optional for portability)
# -----------------------------
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SCHEDULER_SCRIPT = os.path.join(PROJECT_ROOT, "workflows", "scheduler.py")

# -----------------------------
# 🕘 Scheduled Task
# -----------------------------
def job():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🔁 [{now}] Running daily compliance check...")

    try:
        result = subprocess.run(
            [sys.executable, SCHEDULER_SCRIPT],  # Uses current Python interpreter
            capture_output=True,
            text=True,
            check=True
        )
        print("✅ Compliance check complete.")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print("❌ Error running scheduler.py")
        print(e.stderr)

# -----------------------------
# 📅 Schedule Job
# -----------------------------
schedule.every().day.at("09:00").do(job)

print("📅 Daily Scheduler started. Will run at 09:00 AM every day.")
print("⏳ Waiting for next run...\n")

# -----------------------------
# ⏱️ Continuous Loop
# -----------------------------
while True:
    schedule.run_pending()
    time.sleep(60)
