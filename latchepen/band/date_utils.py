from django.utils import timezone
from calendar import Calendar


def format_date(le_date):
    """
    Format date to display in gig list in the template.
    For example: "Sunday 27 January 2018"

    Parameters
    ----------
    le_date: Datetime.date

    Returns
    formatted_date: str
    """
    date_num = le_date.strftime("%d")
    if date_num[0]=='0':
        date_num=date_num[1]
    return le_date.strftime("%A ")+date_num + le_date.strftime(" %B %Y")

def get_third_sunday_of_month(year, month):
    """
    Finds the third Sunday of a given month in a year

    Parameters
    ----------
    year, month: Datetime.year, Datetime.month (ie: integers)

    Returns
    -------
    third_sunday: Datetime.date
    """
    iter_dates = Calendar().itermonthdates(year, month)
    list_days = [c for c in iter_dates if c.month==month]
    third_sunday = [day for day in list_days if day.strftime("%A")=="Sunday"][2]
    return third_sunday

def get_next_third_sunday():
    """
    Finds the next third Sunday

    Returns
    -------
    the next Sunday: Datetime.date
    """
    third_sunday_current_month = get_third_sunday_of_month(year=timezone.now().year, month=timezone.now().month)
    if third_sunday_current_month >= timezone.now().date():
        return third_sunday_current_month
    else:
        le_year = timezone.now().year
        next_month = timezone.now().month+1
        if next_month == 13:
            le_year, next_month = timezone.now().year+1, 1
        return get_third_sunday_of_month(year=le_year, month=next_month)
