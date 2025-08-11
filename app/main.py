import os
import time
import yaml
from datetime import datetime
import pytz

from app.tracker import LiveTracker
from app.reporting import compute_first_day_stats, write_csv

CONFIG_PATH = os.environ.get("CONFIG_PATH", "tracker.config.yaml")

def load_config():
    inline = os.environ.get("CONFIG_YAML")
    if inline:
        return yaml.safe_load(inline)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

if __name__ == "__main__":
    cfg = load_config()
    tracker = LiveTracker(cfg)

    # Start background poller in this simple single-process model
    # (For more robust setups, run two processes: a poller worker and a daily reporter cron.)
    report_time = cfg["delivery_time"]  # e.g., "09:00"
    tz = pytz.timezone(cfg["timezone"])

    while True:
        # 1) Poll once (every loop) – the LiveTracker internally controls cadence
        tracker.run_forever()  # long-running; if you prefer separate processes, split this file.
        # NOTE: In most hosts, you'll instead run tracker.run_forever() in one worker
        # and a separate daily cron that calls compute_first_day_stats + write_csv.
