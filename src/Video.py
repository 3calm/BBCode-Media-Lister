'''
MediaLister
'''
import kaa.metadata
import os
from imdb import IMDb
import logging

class Video():
    '''represents an album'''

    def __init__(self, videofile):
        self.md = kaa.metadata.parse(videofile)
        self.length = self.GetInHMS(self.md.length)
        self.filesize = os.path.getsize(videofile)
        self.fsik = self.filesize
        print
        self.dimensions = '%s X %s' % (str(self.md.video[0].width), str(self.md.video[0].height))
        self.getimdb()
        self.imdb = None


    def GetInHMS(self,seconds):
        'convert secs to mins and secs'
        seconds = int(seconds)
        hours = seconds / 3600
        bminutes = seconds / 60
        seconds -= 3600*hours
        minutes = seconds / 60
        seconds -= 60*minutes
        return '%02s:%02s' % (bminutes, seconds)

    def getimdb(self):
        '''try to get the imdb data'''
        ia = IMDb()
        try:
            if len(self.md.comment[2:9]) == 7:
                print 'Getting IMDB id %s' % self.md.comment[2:9]
                imdb = ia.get_movie(self.md.comment[2:9])
                self.imdb = imdb
                print 'Retrieved IMDB Info for "%s"' % self.imdb
        except:
            print 'Could not retrieve IMDB'


    def __str__(self):
        return str(self.md.type)

    def __repr__(self):
        return self.__str__()