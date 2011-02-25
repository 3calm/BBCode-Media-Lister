'''
MediaLister
'''

from mutagen.mp3 import MP3
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
            self.track = self.audio.tags["TRCK"].text
            self.title = self.audio.tags["TIT2"]
            self.album = self.audio["TALB"].text
            self.artist = self.audio["TPE1"].text
            self.date = self.audio.tags["TDRC"]
            self.genre = self.audio.tags["TCON"]
        except:
            '''FLAC'''
            self.track = self.audio.tags["tracknumber"]
            self.title = self.audio.tags["title"]
            self.artist = self.audio.tags["artist"]
            self.album = self.audio.tags["album"]
            self.date = self.audio.tags["date"]
            self.genre = self.audio.tags["genre"]
        
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
        if len(track) < 2:
            track = str(0) + str(track)
        return track


    def __str__(self):
        return "%s. %s"%(self.track, self.title)


    def __repr__(self):
        return self.__str__()