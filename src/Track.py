'''
MediaLister
'''

class Track(dict):
    """represents a track in an album"""

    def __init__(self, audiofile, filesize):
        
        try:
            '''MP3'''
            self.track = audiofile.tags["TRCK"].text[0]
            self.title = audiofile.tags["TIT2"][0]
            self.album = audiofile["TALB"].text[0]
            self.artist = audiofile["TPE1"].text[0]
            self.date = audiofile.tags["TDRC"][0]
        except:
            '''FLAC'''
            self.track = audiofile.tags["tracknumber"][0]
            self.title = audiofile.tags["title"][0]
            self.artist = audiofile.tags["artist"][0]
            self.album = audiofile.tags["album"][0]
            self.date = audiofile.tags["date"][0]

        self.track = self.tracknumber(self.track)
        self.length = int(audiofile.info.length)
        self.filesize = filesize
        try:
            self.bitrate = audiofile.info.bitrate
        except:
            self.bitrate = 0


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
        return "%s. %s"%(self.track, self.title)


    def __repr__(self):
        return self.__str__()