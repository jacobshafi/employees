from zoneinfo import ZoneInfo
from datetime import datetime, timezone, timedelta
from typing import Final

SERVER_TZ = ZoneInfo("Europe/Berlin")  # mocked remote server timezone
LOCAL_TZ = ZoneInfo("Asia/Dubai")  # my local timezone


def get_server_now() -> datetime:
    return datetime.now(tz=SERVER_TZ)

def to_local_time(dt: datetime) -> datetime:
    return dt.astimezone(LOCAL_TZ)

def to_server_time(dt: datetime) -> datetime:
    return dt.astimezone(SERVER_TZ)


