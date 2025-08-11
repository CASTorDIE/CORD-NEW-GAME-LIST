from datetime import datetime
import pytz

def now_ts():
    from time import time
    return int(time())

def local_now(tz_name: str):
    tz = pytz.timezone(tz_name)
    return datetime.now(tz)
