'''
MediaLister
'''

import logging
#import

class Album():
    '''represents an album'''
    
#    logging.basicConfig(level=logging.DEBUG)

    def __init__(self, title, artist, date):
        self.title = title
        self.artist = artist
        self.date = date
        self.tracks = []
        self.bitrate = 0
        self.length = 0
        self.filesize = 0

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


#    def getdict(self):
#
#        rdict = {
#
#                'title': 'ass ' + self.title,
#                'artist': 'ass '+self.artist,
#                'date' : self.date,
#                'bitrate' : self.calcbitrate(),
#                'size' : int(self.calcfilesize()),
#                'albumlength' : self.GetInHMS(self.calclength())
#
#                }
#        logging.debug('rdict: %s' % str(rdict))
#        return rdict

    def calcbitrate(self):
        '''Calculate the bitrate of the album'''
        tmp = []
        for track in self.tracks:
            tmp.append(track.bitrate)
            self.bitrate = str(int((sum(tmp) / len(tmp)) / 1028))
        return self.bitrate


    def calclength(self):
        '''Calculate the length of the album'''
        self.length = 0
        for track in self.tracks:
            self.length = self.length + track.length
        return self.length


    def calcfilesize(self):
        '''Calculate the length of the album'''

        for track in self.tracks:
            self.filesize = self.filesize + track.filesize
        return self.filesize / 1024 / 1024


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
        'convert secs to mins and secs'
        seconds = int(seconds)
        hours = seconds / 3600
        seconds -= 3600*hours
        minutes = seconds / 60
        seconds -= 60*minutes
        return '%02s' % ( seconds)


    def __str__(self):
        return str(self.title)

    def __repr__(self):
        return self.__str__()