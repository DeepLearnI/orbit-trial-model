from dateutil import relativedelta


def get_dates_in_range(start_date, end_date):
    assert end_date >= start_date
    assert end_date.day == start_date.day
    dates = []
    while end_date != start_date:
        dates.append(end_date)
        end_date += relativedelta(months=-1)
    dates.append(end_date)
    return dates


def zero_time_and_set_day_to_1(dt):
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def increment_months(dt, n_months):
    return dt + relativedelta(months=n_months)
