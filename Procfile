# For Render/Railway (example)
# worker: python -m app.main  # long-running poller (simple mode)
# Alternatively, split processes:
# poller: python -c "from app.main import load_config; from app.tracker import LiveTracker; import time; cfg=load_config(); LiveTracker(cfg).run_forever()"
# reporter: python -c "from app.reporting import compute_first_day_stats, write_csv; from app.main import load_config; from datetime import datetime; import pytz; cfg=load_config(); import pytz; now=datetime.now(pytz.timezone(cfg['timezone'])); print(write_csv(cfg, compute_first_day_stats(cfg, now), now))"
