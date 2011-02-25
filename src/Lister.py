'''
MediaLister
'''

import os, logging

import Track, Album

try:
    import Video
except ImportError:
    videoenabled = False

class Lister():
    '''Class for printing track lists'''

    def __init__(self, debug=False, type=None, path=None, outputfile=None, big=None):
        '''Initialize stuff we need'''
        self.albums = []
        self.videos = []
        self.upaths = []
        self.fpath = None
        self.type = None
        self.debug = debug
        self.opath = outputfile
        self.big = big
        self.format = ""
        self.types = {
            'mp3' : '.mp3',
            'FLAC' : '.flac',

        }
        if path == "":
            self.fpath = os.getcwd()
        else:
            self.fpath = path
        if type != None:
            self.type = (type, self.types[type])
        if self.debug == True:
            '''Log everything, and send it to stderr.'''
            logging.basicConfig(level=logging.DEBUG)

    def walktree(self, fpath):
        '''Walk the directory tree recursively'''
        ''' Go through the directorie '''
        for (wpath, dirs, files) in os.walk(self.fpath):
            totalnumfiles = len(files)
            if totalnumfiles > 0:
                '''Prune all files that are not of the type we want'''
                if self.type != None:
                    files = self.prune(files)
                '''go through the remaining files'''
                for ffile in files:
                    fpath = os.path.join(wpath,ffile)
                    fpath = os.path.normpath(fpath)
                    '''determine the file type'''
                    if os.path.isfile(fpath):
                        size = os.path.getsize(fpath)
                        mobj = self.chooseprocessor(fpath, size)
                        if mobj.__class__ == Track.Track:
                            '''get the album'''
                            album = self.getalbum(mobj)
                            '''add the track to the album'''
                            album.tracks.append(mobj)
                        #elif mobj.__class__ == Video.Video and videoenabled:
                        if videoenabled:
                            self.videos.append(mobj)
                            pass
                        else:
                            return False

    def prune(self, files):
        '''remove files that dont mat te specified type'''
        for ffile in files:
            if self.type != None:
                test = os.path.splitext(ffile)[1].lower() == self.type[1]
            if test != True:
                files.remove(ffile)
            else:
                break
        return files


    def getalbum(self, track):
        '''obtain the album'''
        for album in self.albums:
            if album.title == track.album:
                return album
        '''create the album'''
        album = Album.Album(track.album, track.artist, track.date, self.format, "",
                            track.genre)
        '''add te track to the albumtrack = Track.Track(fpath)'''
        self.albums.append(album)
        '''obtain the album'''
        
        for album in self.albums:
            if album.title == track.album:
                return album
        pass
         

    def addalbum(self,album):
        try:
            i = self.albums.index(album.title)
            return True
        except ValueError:
            self.albums.append(album)

            return False
        except:
            return False

    def chooseprocessor(self,fpath, size):
        '''choose the class to use'''
        
        if os.path.splitext(fpath)[1].lower() == '.mp3':
            self.format = "MP3"
            track = Track.Track(fpath)
            return track
        elif os.path.splitext(fpath)[1].lower() == '.flac':
            self.format = "FLAC"
            track = Track.Track(fpath)
            return track
        elif os.path.splitext(fpath)[1].lower() == '.avi' and videoenabled:
            self.format = "AVI"
            video = Video.Video(fpath)
            return video
        else:
            return False

    def getsize(self, fpath):
        '''get file size'''
        return os.path.getsize(fpath)

    def printtemplate(self, colour, afile, vfile):
        from TemplateHandler import TemplateHandler
        t = TemplateHandler(afile,vfile)
        t.loadtemplate()
        
        vd = {
            'albums' : self.albums,
            'videos' : self.videos,
            'colour' : colour
            }
        logging.debug('! vd: %s' % str(vd))
        return t.printfilledtemplate(vd)
