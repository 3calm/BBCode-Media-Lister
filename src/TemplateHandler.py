'''
MediaLister
'''

import os,  logging
from Cheetah.Template import Template

class TemplateHandler():



    
    def __init__(self, afile, vfile):
        self.cpath = os.getcwd()
        self.apath = os.path.join(self.cpath, 'templates/'+afile)
        self.vpath = os.path.join(self.cpath, 'templates/'+vfile)
        logging.debug('+ TemplateHandler class loaded.')
#        self.tpath = self.getpath(self.cpath, self.tfile)
#        logging.debug('+ Final template path: %s' % self.tpath)


    def getpath(self, fpath, file):
        pfile = os.path.join(fpath,file)
        pfile = os.path.normpath(pfile)
        return pfile


    def loadtemplate(self):
        logging.debug('+ loadtemplate() called.')
        at = open(self.apath, 'r')
        at = at.read()
        vt = open(self.vpath, 'r')
        vt = vt.read()
        self.atemplate = at
        self.vtemplate = vt


    def printfilledtemplate(self, variabledictionary):
        nameSpace = variabledictionary
        atemplate = Template(self.atemplate, searchList=[nameSpace])
        vtemplate = Template(self.vtemplate, searchList=[nameSpace])
        return atemplate.__str__() + '\n\n\n----Video----\n\n\n' + vtemplate.__str__()