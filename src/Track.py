'''
MediaLister
'''

class Track(dict):
    """represents a track in an album"""

    '''Log everything, and send it to stderr.'''
#    logging.basicConfig(level=logging.DEBUG)


    def __init__(self, mp3, filesize):
        self.track = mp3.tags["TRCK"].text
        self.track = self.tracknumber(self.track[0])
        self.title = mp3.tags["TIT2"]
        self.length = int(mp3.info.length)
        self.bitrate = mp3.info.bitrate
        self.album = mp3["TALB"].text
        self.artist = mp3["TPE1"].text
        self.date = mp3.tags["TDRC"]
        self.filesize = filesize


    def __setattr__(self, track, value):
        """track: the numeric track"""
        try:
            self.__dict__[track] = value
        except:
            raise AttributeError
    def __getattr__(self, track):
        try:
            return self.track
        except:
            raise AttributeError



    def __setattr__(self, title, value):
        """title: the title of the track"""
        try:
            self.__dict__[title] = value
        except:
            raise AttributeError
    def __getattr__(self, title):
        try:
            return self.title
        except:
            raise AttributeError


    def __setattr__(self, length, value):
        """length: the length of the track"""
        try:
            self.__dict__[length] = value
        except:
            raise AttributeError
    def __getattr__(self, length):
        try:
            return self.length
        except:
            raise AttributeError


    def __setattr__(self, bitrate, value):
        """bitrate: the numeric bitrate"""
        try:
            self.__dict__[bitrate] = value
        except:
            raise AttributeError
    def __getattr__(self, bitrate):
        try:
            return self.bitrate
        except:
            raise AttributeError


    def __getattr__(self, displength):
        """displength: display length"""
        try:
            return str(self.length)
        except:
            raise AttributeError


    def __getattr__(self, dictrep):
        """dictrep: get a dictionary representation"""
        try:
            return {'track': self.track,
                    'title': self.title,
                    'artist': self.artist,
                    'length': self.length,
                    'filesize': self.filesize
                    }
        except:
            raise AttributeError

    def getkbps(self):
        return int(self.bitrate/1024)

    def tracknumber(self, track):
        '''Flip the track to int for sorting'''

        try:
            if track.find("/") != -1:
                return str(track.split("/")[0])
        except:
            raise Exception
        if str(track)[0] != 0:
            track = str(0) + str(track)
        return track


    def __str__(self):
        return "%s. %s"%(self.track, self.title)


    def __repr__(self):
        return self.__str__()