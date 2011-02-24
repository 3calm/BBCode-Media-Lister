'''
MediaLister
'''

import kaa.metadata
import os

class Track(dict):
    """represents a track in an album"""

    def __init__(self, apath):
        
        try:
            self.md = kaa.metadata.parse(apath)
        except:
            '''Couldnt parse file'''
            print 'couldnt parse file'

        self.track = self.tracknumber(self.md.trackno)
        self.length = int(self.md.length)
        self.filesize = os.path.getsize(apath)
        try:
            self.bitrate = self.md.bitrate
        except:
            self.bitrate = 0


    def getkbps(self):
        return int(self.bitrate/1024)


    def tracknumber(self, track):
        '''Flip the track to int for sorting'''
        try:
            if track.find("/") != -1:
                return str(track.split("/")[0])
        except:
            pass
        if len(track) < 2:
            track = str(0) + str(track)
        return track


    def __str__(self):
        return "%s. %s"%(self.track, self.md.title)


    def __repr__(self):
        return self.__str__()