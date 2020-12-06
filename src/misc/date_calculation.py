import datetime


def construct_datetime_list(start_date: datetime.datetime, end_date: datetime.datetime, stepsize: dict = None):
    if stepsize is None:
        stepsize = {"days": 1}

    constructed = False
    dates = []
    i = 0
    while not constructed:
        new_date = start_date + i * datetime.timedelta(**stepsize)

        if new_date > end_date:
            break
        dates.append(new_date)
        i += 1

    return dates
