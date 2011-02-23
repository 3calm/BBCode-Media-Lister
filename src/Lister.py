'''
MediaLister
'''

import os, logging

from mutagen.mp3 import MP3
from mutagen.flac import FLAC

import Track, Album

class Lister():
    '''Class for printing track lists'''

    '''Log everything, and send it to stderr.'''
#    logging.basicConfig(level=logging.DEBUG)




    def __init__(self, debug=False, type=None, path=None, outputfile=None):
        '''Initialize stuff we need'''
        self.albums = []
        self.upaths = []
        self.fpath = None
        self.type = None
        self.debug = debug
        self.opath = outputfile

        if path == "":
            self.fpath = os.getcwd()
        else:
            self.fpath = path
        self.types = {
            'mp3':'.mp3'
        }
        if type != None:
            self.type = (type, self.types[type])


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
                        track = self.chooseprocessor(fpath, size)
                        if track != False:
                            '''get the album'''

                            album = self.getalbum(track)

                            

                            '''add the track to the album'''

                            album.tracks.append(track)

                            album = 0
#
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
            if album.title == track.album[0]:
                return album
        '''create the album'''
        album = Album.Album(track.album[0], track.artist[0], track.date[0])
        '''add te track to the album'''
        self.albums.append(album)
        '''obtain the album'''
        for album in self.albums:
            if album.title == track.album[0]:
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

            audioproc = MP3(fpath)
        elif os.path.splitext(fpath)[1].lower() == '.fla':
            
            audioproc = FLAC(fpath)
        else:

            return False
        otrack = Track.Track(audioproc, size)
        return otrack


    def getsize(self, fpath):
        '''get file size'''
        return os.path.getsize(fpath)


    def printtemplate(self, albums):
        from TemplateHandler import TemplateHandler
        t = TemplateHandler()
        t.loadtemplate()
        print self.albums[0].gettracks()
        vd = {
            'albums' : self.albums,
            }
        logging.debug('! vd: %s' % str(vd))
        t.printfilledtemplate(vd)
