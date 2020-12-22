from datetime import datetime
from typing import List, Union
import isoweek


def convert_unix_to_datetime(timestamps: Union[List[int], int]):
    if isinstance(timestamps, (int, float)):
        return datetime.fromtimestamp(timestamps)
    else:
        return [datetime.fromtimestamp(t) for t in timestamps]


def convert_datetime_to_unix(datetimes: Union[List[datetime], datetime]):
    if isinstance(datetimes, datetime):
        return int(datetime.timestamp(datetimes))
    else:
        return [int(datetime.timestamp(d)) for d in datetimes]


def convert_datetime_to_isoweek(datetimes: Union[List[datetime], datetime]):
    if isinstance(datetimes, datetime):
        return datetimes.strftime("%G-%V")
    else:
        return [d.strftime("%G-%V") for d in datetimes]


def convert_isoweek_to_datetime(isoweeks: Union[List[str], str]):
    if isinstance(isoweeks, str):
        return isoweek.Week(int(isoweeks[0]), int(isoweeks[1])).Monday
    else:
        isoweeks = [i.split("-") for i in isoweeks]
        return [datetime.fromordinal(isoweek.Week(int(i[0]), int(i[1])).monday().toordinal()) for i in isoweeks]


def get_months_from_datetime(datetimes: Union[List[datetime], datetime]):
    if isinstance(datetimes, datetime):
        return datetimes.month
    else:
        return [d.month for d in datetimes]


def get_year_from_datetime(datetimes: Union[List[datetime], datetime]):
    if isinstance(datetimes, datetime):
        return datetimes.year
    else:
        return [d.year for d in datetimes]


def get_day_from_datetime(datetimes: Union[List[datetime], datetime]):
    if isinstance(datetimes, datetime):
        return datetimes.day
    else:
        return [d.day for d in datetimes]


def get_calendar_week_from_datetime(datetimes: Union[List[datetime], datetime]):
    if isinstance(datetimes, datetime):
        return datetimes.strftime("%V")
    else:
        return [d.strftime("%V") for d in datetimes]
