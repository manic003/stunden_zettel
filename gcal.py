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

# noch letzte Woche automatisch einstellen hinzufügen.. start aktuelle kw-1 bis ende
#allgemeine Funktion für Zeitraum
def check_events(time_start, time_end,name_of_job):
#    for i in calendar_arbeit.get_events(time_start, time_end):

    for i in calendar_arbeit.get_events():
            print(i.summary)  
#
#    #        if name_of_job in i.summary:
#            print("Termin'{}'.".format(name_of_job))
#            return (i.start.isocalendar()[1])
#        else:
#            return(False)

def return_event_on_day(datetime_date):
    start= datetime.datetime.combine(datetime_date,datetime.time(hour=0))
    end = start+ datetime.timedelta(hours=23,minutes=59)
    for i in calendar_arbeit.get_events(time_min=start,time_max=end):
        if i is None:
            return False
        else:
            return i


def get_events_month(month:int,query="",year=None):
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


#    for i in calendar_arbeit.get_events(time_start, time_end):
    if query:
        x = calendar_arbeit.get_events( beginn_of_month, end_of_month,query=query)
    else:
        x = calendar_arbeit.get_events( beginn_of_month, end_of_month)

    return list(x)
    
check_events(start,end,"janet")
