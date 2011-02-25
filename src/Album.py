'''
MediaLister
'''

import logging
import datetime

class Album():
    '''represents an album'''

    def __init__(self, title, artist, date, format, image, genre):
        self.title = title
        self.artist = artist
        self.date = date
        self.tracks = []
        self.bitrate = 0
        self.length = 0
        self.filesize = 0
        self.format = format
        self.sizeinm = self.calcfilesize()
        self.image = image
        self.genre = genre

    def __setattr__(self, title, value):
        '''title: the title of the album'''
        try:
            self.__dict__[title] = value
        except:
            raise AttributeError
    def __getattr__(self, title):
        try:
            return '+ !qa! ' + self.title
        except:
            raise AttributeError


    def __getattr__(self, length):
        '''length: the length of the Album'''
        try:
            return self.GetInHMS(self.calclength())
        except:
            raise AttributeError


    def __getattr__(self, bitrate):
        '''bitrate: the average numeric bitrate'''
        try:
            return self.calcbitrate()
        except:
            raise AttributeError


    def __getattr__(self, tracks):
        '''The tracks in the album'''
        try:
            self.tracks = sorted(self.tracks, key=lambda track: track.track)
            logging.debug('+ tracks:  ')
        except:
            raise AttributeError


    def __getattr__(self, artist):
        '''The artist'''
        try:
            return 'ass ' + self.artist
        except:
            raise AttributeError


    def __getattr__(self, filesize):
        '''The filesize'''
        try:
            return self.calcfilesize()
        except:
            raise AttributeError


    def addtrack(self, track):
        '''Add a track'''
        self.tracks.append(track)


    def calcbitrate(self):
        '''Calculate the bitrate of the album'''
        tmp = []
        for track in self.tracks:
            if type(track.bitrate) != type(None):
                tmp.append(track.bitrate)
            if len(tmp) != 0:
                self.bitrate = str(int((sum(tmp) / len(tmp))))
        return self.bitrate


    def calclength(self):
        '''Calculate the length of the album'''
        self.length = 0
        for track in self.tracks:
            self.length = self.length + track.length
        return self.GetInHMS(self.length)


    def calcfilesize(self):
        '''Calculate the length of the album'''
        tmpsize = 0
        for track in self.tracks:
            tmpsize += track.filesize
        self.filesize = tmpsize
        return "%.2f" %(self.filesize / (1024*1024.0))

    def getartist(self):
        for track in self.tracks:
            if track.artist != self.artist:
                self.artist = "VA"
                return self.artist
                break
        return self.artist

    def tracksindicts(self):
        '''MAKE A LIST OF DICTS'''
        tmp = []
        for track in self.tracks:
            tmp.append(track.dictrep)
            sortedtracks = sorted(tmp, key=lambda k: k['track'])
        return sortedtracks


    def gettracks(self):
        return sorted(self.tracks, key=lambda track: track.track)

    def GetInHMS(self,seconds):
        'convert secs to hours, mins and secs'
        playtime = "%s" % (datetime.timedelta(seconds=seconds))
        if playtime[0:1] == "0":
            playtime = playtime[2:]
        return "%s" % playtime


    def __str__(self):
        return str(self.title)

    def __repr__(self):
        return self.__str__()