import time
from collections import defaultdict
from typing import Dict, Tuple

from .twitch_client import TwitchClient
from .storage import conn
from .util import now_ts

class LiveTracker:
    def __init__(self, config: Dict):
        self.cfg = config
        self.client = TwitchClient()

    def poll_once(self):
        # Walk the streams pagination, aggregating by game_id
        after = None
        agg_viewers = defaultdict(int)
        channels = defaultdict(int)
        while True:
            data = self.client.get_streams(after=after, first=100)
            for s in data.get("data", []):
                gid = s.get("game_id")
                gname = s.get("game_name") or ""
                v = s.get("viewer_count", 0)
                if not gid:
                    continue
                agg_viewers[gid] += v
                channels[gid] += 1
                # record first seen
                with conn() as c:
                    c.execute(
                        "INSERT OR IGNORE INTO stream_seen (game_id, game_name, first_seen_ts) VALUES (?,?,?)",
                        (gid, gname, now_ts())
                    )
            after = data.get("pagination", {}).get("cursor")
            if not after:
                break
        # Store sample
        ts = now_ts()
        with conn() as c:
            for gid, viewers in agg_viewers.items():
                ch = channels.get(gid, 0)
                c.execute("INSERT INTO stats_samples (ts, game_id, viewers, channels) VALUES (?,?,?,?)",
                          (ts, gid, viewers, ch))

    def run_forever(self):
        interval = int(self.cfg["metrics"].get("polling_interval_minutes", 5)) * 60
        while True:
            try:
                self.poll_once()
            except Exception as e:
                print("poll error:", e, flush=True)
            time.sleep(interval)
