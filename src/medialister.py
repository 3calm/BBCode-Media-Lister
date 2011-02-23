#!/usr/bin/env python

import os
from optparse import OptionParser
import Lister

use = "Usage: %prog [options]"
parser = OptionParser(usage = use)

parser.add_option("-d", "--debug", dest="debug", action="store_true", default=False, help="Activate debug mode.")
parser.add_option("-f", "--filename", dest="write", metavar="FILE", help="write output to FILE")
parser.add_option("-t", "--type", dest="type", metavar="TYPE", help="Specify a particular type to limit too.  mp3 for \
                                                                    example.")
parser.add_option("-p", "--path", dest="path", metavar="PATH", help="Define the path to start from.")

options, args = parser.parse_args()

if options.debug:
    print "Debug mode activated."
if options.type:
    print "Specific filetype defined - %s" % options.type
if options.path:
    print "Path set to %s" % options.path
if options.write:
    print "Output file defined: %s" % options.write

lister = Lister.Lister(debug=options.debug, type=options.type, path=options.path, outputfile=options.write)
ltest = lister.walktree(lister.fpath)
if options.write:
    f = open(options.write, 'w')
    out = lister.printtemplate(lister.albums)
    f.write(out)
    f.close
else:
#    lister.printtemplate(lister.albums)
    pass