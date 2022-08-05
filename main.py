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
        input("Please close libreoffice first! Confirm with Enter")
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
COL_DURATION = "D"

CELL_MONTH_YEAR = "E7"
CELL_PROJECT_NAME = "D7"


## modul functions, use this with care!! better use the  userfunctions below!

def _add_times(day_of_month: int, start: str, end: str, note=""):

    """
    day_of_month : int
    start        : str
    end          : str
    note         : str


    this function simply adds:
        - the String for start (hh:mm)
        - the String for end (hh:mm)
        - the String for note field

        to the template.ods sheet
    """

    c_start = active_sheet.getCellRangeByName(COL_START + str(day_of_month+10))
    c_end = active_sheet.getCellRangeByName(COL_END + str(day_of_month+10))
    c_note = active_sheet.getCellRangeByName(COL_NOTE + str(day_of_month+10))

    if c_start.String != "" :
        input("nicht leer ERROR")
#        print("old=" ,c_note.String)
#        c_note.String = f"{c_start.String}-{c_end.String};"

    c_start.String = start
    c_end.String = end

#    if old_val:
#            active_sheet.getCellRangeByName("D" + str(day_of_month+10)).String = int(old_val+


    if note:
        c_note.String = note


def _add_values(day_of_month: int, start: str, end: str, duration_plus: int):
    """
    only for special case that i have more than one appoinment at a day
        -> the note field will be used to save the times
    TODO SONDERFALL wenn die termine nahtlos ineinadner übergehen wäre das nicht nötig...
    """

    #define cells
    c_start = active_sheet.getCellRangeByName(COL_START + str(day_of_month+10))
    c_end = active_sheet.getCellRangeByName(COL_END + str(day_of_month+10))
    c_note = active_sheet.getCellRangeByName(COL_NOTE + str(day_of_month+10))
    c_duration = active_sheet.getCellRangeByName(COL_DURATION + str(day_of_month+10))

    #append time note to notes field
    c_note.String =  c_note.String + f"{start}-{end};"

    # if there's already an appoinment, add duration,
    if c_start.String != "" :
        c_duration.String = str(round( float(c_duration.String.replace(',', ''))  +  duration_plus,2) )
        c_start.String = "siehe"
        c_end.String = "rechts"

    else:
        c_duration.String = str( duration_plus )
        c_start.String = start
        c_end.String = end


#    if old_val:
#            active_sheet.getCellRangeByName("D" + str(day_of_month+10)).String = int(old_val+





def _add_from_gcal(month:int , query=""):
    t = dt.today()

    print(f'Adding Appoinments for {month}/{t.strftime("%y")}')
    events = get_events_month(month,query,order_by="startTime")

    # save all events in dict, in case there is more than one appoinment per day 
    day_dict = dict()
    for i in events:
        print( f"{i.start.day}.{i.start.month} {i.start.hour}:{i.start.minute} - {i.end.hour}:{i.end.minute}\t{i.summary}")

        # if key exits append appointment to list
        if f"{i.start.day}.{i.start.month}" in day_dict.keys():
            day_dict[f"{i.start.day}.{i.start.month}"].append(i)

        # first appoinment goes into list
        else:
            day_dict[f"{i.start.day}.{i.start.month}"] = list()
            day_dict[f"{i.start.day}.{i.start.month}"].append(i)

    # for all days iterate through the appoinment list
    for i in day_dict.values():
        input("import next appoinment  with enter...\n")
        if len(i) > 1:
            for j in i:
                _add_values(day_of_month=j.start.day, start=f"{j.start.hour}:{j.start.minute}",end= f"{j.end.hour}:{j.end.minute}", duration_plus= (j.end -j.start).total_seconds()/3600 )

        # if just one appoinment in list(= just one appoinment at this day), add just the times to sheet, and let libreoffice calculate the duration field 
        else:
            for j in i:
                _add_times(day_of_month=j.start.day, start=f"{j.start.hour}:{j.start.minute}",end= f"{j.end.hour}:{j.end.minute}" ,note=j.summary)



#        print( f"{i.start.day}.{,i.start.month} {i.start.hour}:{i.start.minute} - {i.end.hour}:{i.end.minute}\t{i.summary}")

#        if f"{i.start.day}.{i.start.month}" in day_dict.keys():
#            day_dict[f"{i.start.day}.{i.start.month}"][0] += (i.end -i.start).total_seconds()/3600
#
#        else:
#            day_dict[f"{i.start.day}.{i.start.month}"] = list()
#            day_dict[f"{i.start.day}.{i.start.month}"][0] = (i.end -i.start).total_seconds()/3600
#            day_dict[f"{i.start.day}.{i.start.month}"][1]= list()
#            day_dict[f"{i.start.day}.{i.start.month}"][1]

#    print(day_dict)
#        time.sleep(0.5)







## user functions

def add_from_gcal(query="Nachhilfe"):
    t= dt.today()
    last_month = dt(t.year,t.month,1) - timedelta(days=1)
    text1= f'Add appoinments for last month {last_month.strftime("%h%m")}  [y/n] default:yes'
    choice= input(text1)
    choice= choice.lower()
    month = last_month

    # if user wants a differnt month.. 
    # TODO add special case user wants a month from an old year (unlikely)
    if (choice=="n" or choice == "no"):
        month = input("Please enter the month as integer:")
        _add_from_gcal(int(month),query)

    else:
        _add_from_gcal(month.month,query)




add_from_gcal()
