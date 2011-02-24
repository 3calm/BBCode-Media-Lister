#!/usr/bin/env python


from optparse import OptionParser
import Lister
import os, sys

use = "Usage: %prog [options]"
parser = OptionParser(usage = use)
parser.add_option("-d", "--debug", dest="debug", action="store_true", default=False, help="Activate debug mode.")
parser.add_option("-f", "--filename", dest="write", metavar="FILE", help="write output to FILE")
parser.add_option("-t", "--type", dest="type", metavar="TYPE", help="Specify a particular type to limit too.  mp3 for \
                                                                    example.")
parser.add_option("-c", "--colour", dest="colour", default='orange', metavar="FILE", help="write output to FILE")
parser.add_option("-g", "--images", dest="images", action="store_true", default=False, help="Generate images.")
parser.add_option("-i", "--imdb", dest="imdb", action="store_true", default=False, help="IMDB Mode.")
parser.add_option("-p", "--path", dest="path", metavar="PATH", help="Define the path to start from.")

options, args = parser.parse_args()

if options.debug:
    print "Debugging is turned on."
if options.type:
    print "Type set to %" % options.type
if options.path:
    good = os.path.isdir(options.path)
    if good:
        print "Path set to %s" % options.path
    else:
        sys.exit('The path %s does not exist' % options.path)

print "\n3Calm's Media Lister\n=======\n"
lister = Lister.Lister(debug=options.debug, type=options.type, path=options.path, outputfile=options.write)
ltest = lister.walktree(lister.fpath)

if options.write:
    f = open(options.write, 'w')
    out = lister.printtemplate(options.colour)
    f.write(out)
    f.close
    for album in lister.albums:
        f = open(album.title + '.jpg', 'w')
        f.write(str(album.image))
        f.close
    print "\nThe output is in the file %s" % options.write
else:
    print lister.printtemplate(options.colour)
    pass