#!/usr/bin/python3

import getopt, sys
import uno

from os import getcwd
from os.path import splitext


def main():
    retVal = 0
    doc = None
    stdout = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:",
            ["help", "connection-string=" , "html", "pdf", "stdout" ])
        url = "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext"
        filterName = "Text (Encoded)"
        extension  = "txt"
        o  =a  = None
        for o, a in opts:
            if o in ("-h", "--help"):
                usage()
                sys.exit()
            if o in ("-c", "--connection-string" ):
                print("huhu=" ,a)
#                url = "uno:" + a + ";urp;StarOffice.ComponentContext"
            if o == "--html":
                filterName = "HTML (StarWriter)"
                extension  = "html"
            if o == "--pdf":
                filterName = "writer_pdf_Export"
                extension  = "pdf"


        if o == "--stdout":
            stdout = True

        if not len( args ):
            usage()
            sys.exit(retVal)

        print("FILTER===", filterName) 

    except getopt.GetoptError as e:
        sys.stderr.write( str(e) + "\n" )
        usage()
        retVal = 1

    sys.exit(retVal)

def usage():
    sys.stderr.write( "usage: ooextract.py --help | --stdout\n"+
                  "       [-c <connection-string> | --connection-string=<connection-string>\n"+
          "       [--html|--pdf]\n"+
          "       [--stdout]\n"+
                  "       file1 file2 ...\n"+
                  "\n" +
                  "Extracts plain text from documents and prints it to a file (unless --stdout is specified).\n" +
                  "Requires an OpenOffice.org instance to be running. The script and the\n"+
                  "running OpenOffice.org instance must be able to access the file with\n"+
                  "by the same system path. [ To have a listening OpenOffice.org instance, just run:\n"+
          "openoffice \"-accept=socket,host=localhost,port=2002;urp;\" \n"
                  "\n"+
          "--stdout \n" +
          "         Redirect output to stdout. Avoids writing to a file directly\n" + 
                  "-c <connection-string> | --connection-string=<connection-string>\n" +
                  "        The connection-string part of a uno url to where the\n" +
                  "        the script should connect to in order to do the conversion.\n" +
                  "        The strings defaults to socket,host=localhost,port=2002\n"
                  "--html \n"
                  "        Instead of the text filter, the writer html filter is used\n"
                  "--pdf \n"
                  "        Instead of the text filter, the pdf filter is used\n"
                  )

main()    
