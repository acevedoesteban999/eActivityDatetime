import pytz
from datetime import datetime, time, date
from dateutil.tz import tzlocal

def get_server_utc_datetime(hour: int, minute: int):
    server_tz = tzlocal()
    local_dt = datetime.combine(date.today(), time(hour, minute)).replace(tzinfo=server_tz)
    return local_dt.astimezone(pytz.UTC).replace(tzinfo=None)