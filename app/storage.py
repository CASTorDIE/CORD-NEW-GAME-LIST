import os
import sqlite3
from contextlib import contextmanager

DB_PATH = os.environ.get("DB_PATH", "/data/tracker.sqlite")

SCHEMA = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS stream_seen (
  game_id TEXT,
  game_name TEXT,
  first_seen_ts INTEGER,
  PRIMARY KEY (game_id)
);
CREATE TABLE IF NOT EXISTS stats_samples (
  ts INTEGER,
  game_id TEXT,
  viewers INTEGER,
  channels INTEGER
);
CREATE TABLE IF NOT EXISTS reports (
  report_date TEXT,
  game_id TEXT,
  game_name TEXT,
  peak_viewers INTEGER,
  avg_viewers REAL,
  hours_watched REAL,
  total_streams INTEGER,
  unique_channels INTEGER,
  peak_channels INTEGER,
  PRIMARY KEY (report_date, game_id)
);
"""

@contextmanager
def conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    c = sqlite3.connect(DB_PATH)
    try:
        yield c
    finally:
        c.commit()
        c.close()

with conn() as c:
    c.executescript(SCHEMA)
