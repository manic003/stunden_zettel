#!/usr/bin/python3
import argparse
import argcomplete
import textwrap

wrapper = textwrap.TextWrapper()

def main(**args):
    print("ARGS=\n\t",args)
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='BillingTimesheetGenerator',
             formatter_class=argparse.RawDescriptionHelpFormatter,
             description='A simple script to import and write googlecalendar events to an libreoffice-calc sheet.',
             epilog = textwrap.dedent('''\

        The program will open libreoffice, and fill  out the sheet, at any  time you
        can edit the sheet by yourself and  quit the program with ctrl-d. (You might
        leave a loop with ctrl-c before) As this script is intended to  be used side
        by side with libreoffice open, so you can control the import  of appoinments
        there is one important note just as any LibreOffice sheet...:

                        'YOU NEED TO SAVE THE SHEET BY YOURSELF!

        TODO If you use the -straigt-mode this is of course not the case.

        author: Max Nicolay
        date:   11/08/2022'''))




    parser.add_argument('-f','--fast', help='Execute in fast mode. The events will be imported straight, there will be no confirmation necessary through cmdline',action="store_true")
    parser.add_argument('-q','--query', help='Events will be filtered by this string. (CaseINsensitiv -> Office = office)',metavar="SearchKeyword",default="Nachhilfe")
    parser.add_argument('-m','--month',type=int, help='The month (1-12) for which the billing timesheet should be generated. Default is last month.',metavar="month",default="-1",choices=range(1,13))


    argcomplete.autocomplete(parser)

    args=parser.parse_args()
    main(**vars(args))
    
