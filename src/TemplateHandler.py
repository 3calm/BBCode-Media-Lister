'''
MediaLister
'''

import os,  logging
from Cheetah.Template import Template

class TemplateHandler():

#    logging.basicConfig(level=logging.DEBUG)

    cpath=os.getcwd()
    tfile = 'templates/album_template_1.tmpl'
    tpath = None
    ctemplate = ""

    def __init__(self):
        logging.debug('+ TemplateHandler class loaded.')
        self.tpath = self.getpath(self.cpath, self.tfile)
        logging.debug('+ Final template path: %s' % self.tpath)

    def getpath(self, fpath, file):
        pfile = os.path.join(fpath,file)
        pfile = os.path.normpath(pfile)
        return pfile

    def loadtemplate(self):
        logging.debug('+ loadtemplate() called.')
#        try:
        t = open(self.tpath, 'r')
        ct = t.read()
        self.ctemplate = ct
        logging.debug('! t: ' + str(self.ctemplate))
#        except:
#        logging.debug('+ Failed to load template.')
#        return False

    def printfilledtemplate(self, variabledictionary):
        nameSpace = variabledictionary
        template = Template(self.ctemplate, searchList=[nameSpace])
        print 'returning output'
        print type(template.__str__())
        return template.__str__()