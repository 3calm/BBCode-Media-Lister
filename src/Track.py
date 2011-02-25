'''
MediaLister
'''

#from mutagen.mp3 import MP3
from mp3 import MP3
from mutagen.flac import FLAC
import os

class Track(dict):
    """represents a track in an album"""

    def __init__(self, apath):

        if os.path.splitext(apath)[1].lower() == '.flac':
            self.audio = FLAC(apath)
        elif os.path.splitext(apath)[1].lower() == '.mp3':
            self.audio = MP3(apath)
        try:
            '''MP3'''
            self.track = self.audio.tags["TRCK"][0]
            self.title = self.audio.tags["TIT2"][0]
            self.album = self.audio["TALB"][0]
            self.artist = self.audio["TPE1"][0]
            self.date = self.audio.tags["TDRC"][0]
            self.genre = self.audio.tags["TCON"][0]
            try:
                self.preset = self.audio.info.preset
            except:
                self.preset = ""
        except:
            '''FLAC'''
            self.track = self.audio.tags["tracknumber"][0]
            self.title = self.audio.tags["title"][0]
            self.artist = self.audio.tags["artist"][0]
            self.album = self.audio.tags["album"][0]
            self.date = self.audio.tags["date"][0]
            self.genre = self.audio.tags["genre"][0]
        
        self.track = self.tracknumber(self.track)
        self.length = int(self.audio.info.length)
        self.filesize = os.path.getsize(apath)
        try:
            self.bitrate = int(self.audio.info.bitrate/1000) # should be 1000, not 1024! (cheers raqqa)
        except:
            self.bitrate = 0


    def getkbps(self):
        return self.bitrate


    def tracknumber(self, track):
        '''Flip the track to int for sorting'''
        try:
            if track.find("/") != -1:
                return str(track.split("/")[0])
        except:
            pass
        #if len(track) < 2:
        if track < 10:
            track = str(0) + str(track)
        return track


    def __str__(self):
        return "%d. %s"%(self.track, self.title)


    def __repr__(self):
        return self.__str__()