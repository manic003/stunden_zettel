from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from datetime import datetime as dt

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


def get_events_month(month:int,query=""):
    t = dt.today()
#    for i in calendar_arbeit.get_events(time_start, time_end):
    if query:
        x = calendar_arbeit.get_events(dt(t.year,month,1,0,0),t,query=query)
    else:
        x = calendar_arbeit.get_events(dt(t.year,month,1,0,0),t)

    return list(x)
    
check_events(start,end,"janet")
