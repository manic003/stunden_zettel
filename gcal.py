"""
author: max nicolay
date: 06.08.22
"""

from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from datetime import datetime as dt
from datetime import timedelta

calendar_haushalt = GoogleCalendar("regg900o16pp20bc9fcbnud2gg@group.calendar.google.com")
calendar_arbeit= GoogleCalendar('raspmaxcal@gmail.com')

start = dt(2022, 4, 1, 21, 0)
end = dt(2020, 8, 3, 22, 0)


def add_termin(titel, start, end):
    event = Event(titel, start, end)
    calendar_haushalt.add_event(event)

def return_event_on_day(datetime_date):
    """
    returns first event at the given day or None if there's no event
    """
    start= datetime.datetime.combine(datetime_date,datetime.time(hour=0))
    end = start+ datetime.timedelta(hours=23,minutes=59)
    for i in calendar_arbeit.get_events(time_min=start,time_max=end):
        if i is None:
            return None
        else:
            return i


def get_events_month(month:int,query="",year=None,order_by="startTime",calendar=calendar_arbeit):
    """
        returns the events of calendar_arbeit for the given month, optional filtered by query parameter.

        month : int     the month for which you want the events (current year)
        query : str     an optional query parameter (summary field of calender) caseinsensitiv 
        year  : int     default year is current year, if you want to get events from an recent year use this parameter

    """

    t = dt.today()

    if not year:
        year = t.year

    beginn_of_month = dt(year,month,1)
    end_of_month = dt(year,month+1,1) - timedelta(days=1)


    if query:
        x = calendar.get_events( beginn_of_month, end_of_month,query=query,order_by=order_by,single_events=True)
    else:
        x = calendar.get_events( beginn_of_month, end_of_month,order_by=order_by,single_events=True)

    return list(x)

