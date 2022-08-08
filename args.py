#!/usr/bin/python3
import argparse
import argcomplete
#parser = argparse.ArgumentParser(description='Process some integers.')
#parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                    help='an integer for the accumulator')
#parser.add_argument('--sum', dest='accumulate', action='store_const',
#                    const=sum, default=max,
#                    help='sum the integers (default: find the max)')
#
#args = parser.parse_args()
#print(args.accumulate(args.integers))



def main(**args):
    pass

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='BillingTimesheetGenerator',
                                    description='A simple script to import and write googlecalendar events to an libreoffice-calc sheet.',
                                    epilog = '\tThe program will open libreoffice, and fill out the sheet, at any'+
                                             '\n\ttime you can edit the sheet by yourself and quit the program with ctrl-d.'
                                    +'\n\tYOU NEED TO SAVE THE SHEET BY YOURSELF!\n\n\tauthor: max nicolay\n\tdate:09-08-2022',
    )

    #                                formatter_class= argparse.RawTextHelpFormatter
    #                     )


    parser.add_argument('-f','--fast', help='Execute in fast mode. The events will be imported straight, there will be no confirmation necessary through cmdline')
    parser.add_argument('-q=','--query=', help='Events will be filtered by this string. (CaseINsensitiv -> Office = office)',metavar="SearchKeyword",default="Nachhilfe")
    parser.add_argument('-m=','--month=',type=int, help='The month (1-12) for which the billing timesheet should be generated. Default is last month.',metavar="month",default="-1")


    argcomplete.autocomplete(parser)

    args=parser.parse_args()
    main(**vars(args))
