import os
import time
import uno # get the uno component context from the PyUNO runtime
import datetime as dt
from gcal import *
import atexit


import signal
import sys



def clean_exit():
    try:
        input("Please close libreoffice first!")
    except EOFError:
        print(" ")

        
atexit.register(clean_exit)

def signal_handler(sig, frame):
    print("Please use ctrl-d to exit!")


signal.signal(signal.SIGINT, signal_handler)
#signal.pause()





ODS_TEMPLATE = "ods_files/template/template.ods"

choice= input("Run libreoffice? [y/n] default yes: ")
if not (choice == "n" or choice=="no"):
# open sheet in libreoffice...
    cmd=f'soffice {ODS_TEMPLATE} --calc --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"'
    os.popen(cmd) # todo... besser iwie forken oder so? kp


input("LibreOffice is opening 'template.ods', continue with enter")

localContext = uno.getComponentContext() # create the UnoUrlResolver
resolver = localContext.ServiceManager.createInstanceWithContext(
				"com.sun.star.bridge.UnoUrlResolver", localContext ) # connect to the running office
ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
smgr = ctx.ServiceManager # get the central desktop object
desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx) # access the current writer document
model = desktop.getCurrentComponent()

# access the active sheet
active_sheet = model.CurrentController.ActiveSheet

## exampels..
# access cell C4
#cell1 = active_sheet.getCellRangeByName("C4")
# set text inside
#cell1.String = "Hello world"
# other example with a value
#cell2 = active_sheet.getCellRangeByName("E6")
#cell2.Value = cell2.Value + 1


## input zeiten der tage geht von Zeile 11 = 1 bis 41 = 31 
COL_START = "B"
COL_END = "C"
COL_NOTE = "E"

CELL_MONTH_YEAR = "E7"
CELL_PROJECT_NAME = "D7"


## modul functions           use with care!! better use user functions below!

def _add_times(day_of_month: int, start: str, end: str, note=""):

    c_start = active_sheet.getCellRangeByName(COL_START + str(day_of_month+10))
    c_end = active_sheet.getCellRangeByName(COL_END + str(day_of_month+10))

    c_start.String = start
    c_end.String = end
    if note:
        c_note = active_sheet.getCellRangeByName(COL_NOTE + str(day_of_month+10))
        c_note.String = note



def _add_from_gcal(month:int , query=""):
    t = dt.today()
    
    print(f'Adding Appoinments for {month}/{t.strftime("%y")}')
    events = get_events_month(month,query)
    for i in events:
        print( i.start.day," " ,i.start.month, f"{i.start.hour}:{i.start.minute}", f"{i.end.hour}:{i.end.minute}",i.summary)

        _add_times(i.start.day, f"{i.start.hour}:{i.start.minute}", f"{i.end.hour}:{i.end.minute}",i.summary)
        time.sleep(0.5)







## user functions

def add_from_gcal(query=""):
    t= dt.today()
    last_month = dt(t.year,t.month,1) - timedelta(days=1)
    text1= f'Add appoinments for last month {last_month.strftime("%h%m")}  [y/n] default:yes'
    choice= input(text1)
    choice= choice.lower()
    month = last_month

    if (choice=="n" or choice == "no"):
        month = input("Please enter the month as integer:")
        _add_from_gcal(month,query)

    else:
        _add_from_gcal(month.month,query)
