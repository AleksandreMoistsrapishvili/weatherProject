import datetime

def format_date(date):
    year_month_day_format = '%Y-%m-%d'
    formatted = date.strftime(year_month_day_format)
    return formatted

def today_date():
    now = datetime.datetime.now(datetime.timezone.utc)
    format = format_date(now)
    return format

def tomorrow_date():
    tomorow = datetime.date.today() + datetime.timedelta(days=1)
    year_month_day_format = '%Y-%m-%d'
    formatted = tomorow.strftime(year_month_day_format)
    return formatted

def twoday_date():
    twoday = datetime.date.today() + datetime.timedelta(days=2)
    format = format_date(twoday)
    return format

def threeday_date():
    threeday = datetime.date.today() + datetime.timedelta(days=3)
    format = format_date(threeday)
    return format

def fourthday_date():
    fourthday = datetime.date.today() + datetime.timedelta(days=4)
    format = format_date(fourthday)
    return format
