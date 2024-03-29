#!/usr/bin/python3

import os
import time
import uno # get the uno component context from the PyUNO runtime
import datetime as dt
from gcal import *
import atexit
import signal
import sys
import argument_parser as arg_parser

args = arg_parser.args
ODS_TEMPLATE = "ods_files/template/template.ods"  # path to libreoffice calc file
# relevant columns and cells of the sheet
COL_START = "B"
COL_END = "C"
COL_NOTE = "E"
COL_DURATION = "D"
CELL_MONTH_YEAR = "E7"
CELL_PROJECT_NAME = "D7"

## customize cmdline
BRIGHT_FONT = "\033[1;1m"
NORMAL_FONT = "\033[1;0m"
Red    = "\u001b[31m"
Green  = "\u001b[32m"
Yellow = "\u001b[33m"
Reset  = "\u001b[0m"

Bold = "\u001b[1m"
Underline = "\u001b[4m"
Reversed  = "\u001b[7m"

ClearScreen = "\u001b[2J"
#ClearScreen = "\u001b[{n}J"
#        n=0 clears from cursor until end of screen,
#        n=1 clears from cursor to beginning of screen
#        n=2 clears entire screen

ClearLine = "\u001b2K"
#ClearLine = "\u001b[{n}K"
#        n=0 clears from cursor to end of line
#        n=1 clears from cursor to start of line
#        n=2 clears entire line

Y_N_CHOICE =  f"{Yellow} [y/n] default yes:   {Reset}"

def clean_exit():
    try:
        input("Please close libreoffice first! Confirm with Enter")
    except EOFError:
        print(" ")


def signal_handler(sig, frame):
    print("Please use ctrl-d to exit!")


atexit.register(clean_exit)
signal.signal(signal.SIGINT, signal_handler)

print(ClearScreen)

if not args.fast:

    text = f"Run libreoffice? {Y_N_CHOICE}"
    choice= input(text)
else:
    choice = "yes"

if not (choice == "n" or choice=="no"):
# open sheet in libreoffice...
    cmd=f'soffice {ODS_TEMPLATE} --calc --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"'
    os.popen(cmd) # todo... besser iwie forken oder so? kp
    input("confirm with Enter if libreoffice is ready..")

    localContext = uno.getComponentContext() # create the UnoUrlResolver
    resolver = localContext.ServiceManager.createInstanceWithContext(
    				"com.sun.star.bridge.UnoUrlResolver", localContext ) # connect to the running office
    ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
    smgr = ctx.ServiceManager # get the central desktop object
    desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx) # access the current writer document
    model = desktop.getCurrentComponent()

    # access the active sheet
    active_sheet = model.CurrentController.ActiveSheet



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
        input("ERROR nicht behandelter FALL!! Das Skript überschreibt jetzt Werte die nicht berücksichtigt werden!!!")

    c_start.String = start
    c_end.String = end

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

    # if there's already an appoinment, add duration,
    if c_start.String != "" :
        c_duration.Value = round( c_duration.Value  +  duration_plus,2)
        c_start.String = "siehe"
        c_end.String = "rechts"


        #append time note to notes field
        c_note.String =  c_note.String + f";{start}-{end}"

    else:
        c_duration.Value =  duration_plus
        c_start.String = start
        c_end.String = end
        #append time note to notes field
        c_note.String = f"{start}-{end}"


def _add_from_gcal(month:int , query=""):
    t = dt.today()

    print(f'Adding Appoinments for {month}/{t.strftime("%y")}')
    events = get_events_month(month,query,order_by="startTime")

    # save all events in dict, in case there is more than one appoinment per day 
    day_dict = dict()
    for i in events:

        # if key exits append appointment to list
        if f"{i.start.day}.{i.start.month}" in day_dict.keys():
            day_dict[f"{i.start.day}.{i.start.month}"].append(i)

        # first appoinment goes into list
        else:
            day_dict[f"{i.start.day}.{i.start.month}"] = list()
            day_dict[f"{i.start.day}.{i.start.month}"].append(i)

    # for all days iterate through the appoinment list
    for i in day_dict.values():
        if len(i) > 1:
            for j in i:
                text= f"   {Reversed}{j.start.day:02}.{j.start.month:02} {j.start.hour:02}:{j.start.minute:02}-{j.end.hour:02}:{j.end.minute:02} {j.summary}{Reset}\t -> add? {Y_N_CHOICE}"
                if not args.fast:
                    choice = input(text)
                    choice = choice.lower()
                else:
                    choice = "yes"
                    print("added: ",text.split("->")[0], "\n")

                if not (choice == "no" or choice == "n"):
                    _add_values(day_of_month=j.start.day, start=f"{j.start.hour:02}:{j.start.minute:02}",end= f"{j.end.hour:02}:{j.end.minute:02}", duration_plus= (j.end -j.start).total_seconds()/3600 )
                else:
                    print("skipped this appoinment ")

        # if just one appoinment in list(= just one appoinment at this day), add just the times to sheet, and let libreoffice calculate the duration field 
        else:
            for j in i:
                text= f"   {Reversed}{j.start.day:02}.{j.start.month:02} {j.start.hour:02}:{j.start.minute:02}-{j.end.hour:02}:{j.end.minute:02} {j.summary}{Reset}\t -> add? {Y_N_CHOICE}"
                if not args.fast:
                    choice = input(text)
                    choice = choice.lower()
                else:
                    choice = "yes"
                    print("added: ",text.split("->")[0], "\n")

                if not (choice == "no" or choice == "n"):
                    _add_times(day_of_month=j.start.day, start=f"{j.start.hour:02}:{j.start.minute:02}",end= f"{j.end.hour:02}:{j.end.minute:02}" ,note=j.summary)

                else:
                    print("skipped this appoinment ")
        print("")

## user functions

def add_from_gcal(query="Nachhilfe",month="default"):
    if month == -1:
        month = "default"

    t= dt.today()
    last_month = dt(t.year,t.month,1) - timedelta(days=1)
    if month == "default":
        text1= f'Add appoinments for last month {last_month.strftime("%h%m")}? {Y_N_CHOICE}'
        choice= input(text1)
        choice= choice.lower()
        month = last_month

    else:
        choice = "n"

    # if user wants a differnt month.. 
    # TODO add special case user wants a month from an old year (unlikely)
    if (choice=="n" or choice == "no"):
        if month== "default":
            month = input("Please enter the month as integer: ")

        _add_from_gcal(int(month),query)
        active_sheet.getCellRangeByName(CELL_MONTH_YEAR).String = f"{int(month):02}/{t.year}"

    else:
        _add_from_gcal(month.month,query)
        active_sheet.getCellRangeByName(CELL_MONTH_YEAR).String = f"{month.month:02}/{t.year}"




add_from_gcal(query=args.query,month=args.month)

print("\n => type 'add_from_gcal()' if you want to load more events")
