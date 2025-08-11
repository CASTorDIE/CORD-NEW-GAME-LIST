# Twitch New Games Tracker

## Deploy (Railway example)
1. **New Project → Deploy from GitHub** (push this repo to your GitHub).
2. Add a **Service** from the repo.
3. Set **Environment Variables**:
   - `TWITCH_CLIENT_ID`
   - `TWITCH_CLIENT_SECRET`
   - `TZ=America/Chicago`
   - (optional) `CONFIG_YAML` – paste your YAML to override file
4. Add a **Persistent Volume** mounted at `/data`.
5. Create a **Worker** process:
   - Command: `python -m app.main` (poller)
6. Create a **Cron Job** (daily reporter):
   - Schedule: `0 9 * * *` (for 09:00 CT; adjust for host's timezone)
   - Command:
     ```bash
     python -c "from app.reporting import compute_first_day_stats, write_csv; from app.main import load_config; from datetime import datetime; import pytz; cfg=load_config(); now=datetime.now(pytz.timezone(cfg['timezone'])); print(write_csv(cfg, compute_first_day_stats(cfg, now), now))"
     ```
7. Download the CSV from the mounted volume `/data/reports` or configure an object store target.

## Notes
- Metrics are computed from periodic snapshots of Twitch live streams. True **unique channel** counts require per-channel IDs; this implementation approximates using peak channels as a lower bound. If you want exact uniques, we can extend storage to record channel IDs per game.
- To include Google Sheets or alerts, wire any webhook or Google API client where marked in code.
