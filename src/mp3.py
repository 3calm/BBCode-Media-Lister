# MP3 stream header information support for Mutagen.
# Copyright 2006 Joe Wreschnig
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of version 2 of the GNU General Public License as
# published by the Free Software Foundation.

"""MPEG audio stream information and tags."""

import os
import struct

from mutagen.id3 import ID3FileType, BitPaddedInt, delete

class error(RuntimeError): pass
class HeaderNotFoundError(error, IOError): pass
class InvalidMPEGHeader(error, IOError): pass

# Mode values.
STEREO, JOINTSTEREO, DUALCHANNEL, MONO = range(4)

class MPEGInfo(object):
	"""MPEG audio stream information

	Parse information about an MPEG audio file. This also reads the
	Xing VBR header format.

	This code was implemented based on the format documentation at
	http://www.dv.co.yu/mpgscript/mpeghdr.htm.

	Useful attributes:
	length -- audio length, in seconds
	bitrate -- audio bitrate, in bits per second
	sketchy -- if true, the file may not be valid MPEG audio

	Useless attributes:
	version -- MPEG version (1, 2, 2.5)
	layer -- 1, 2, or 3
	mode -- One of STEREO, JOINTSTEREO, DUALCHANNEL, or MONO (0-3)
	protected -- whether or not the file is "protected"
	padding -- whether or not audio frames are padded
	sample_rate -- audio sample rate, in Hz
	"""

	# Map (version, layer) tuples to bitrates.
	__BITRATE = {
		(1, 1): range(0, 480, 32),
		(1, 2): [0, 32, 48, 56, 64, 80, 96, 112,128,160,192,224,256,320,384],
		(1, 3): [0, 32, 40, 48, 56, 64, 80, 96, 112,128,160,192,224,256,320],
		(2, 1): [0, 32, 48, 56, 64, 80, 96, 112,128,144,160,176,192,224,256],
		(2, 2): [0,  8, 16, 24, 32, 40, 48,  56, 64, 80, 96,112,128,144,160],
		}
		
	__BITRATE[(2, 3)] = __BITRATE[(2, 2)]
	for i in range(1, 4): __BITRATE[(2.5, i)] = __BITRATE[(2, i)]

	# Map version to sample rates.
	__RATES = {
		1: [44100, 48000, 32000],
		2: [22050, 24000, 16000],
		2.5: [11025, 12000, 8000]
		}

	sketchy = False
	preset = None
	vbr = False
	lameversion = None

	def __init__(self, fileobj, offset=None):
		"""Parse MPEG stream information from a file-like object.

		If an offset argument is given, it is used to start looking
		for stream information and Xing headers; otherwise, ID3v2 tags
		will be skipped automatically. A correct offset can make
		loading files significantly faster.
		"""

		try: size = os.path.getsize(fileobj.name)
		except (IOError, OSError, AttributeError):
			fileobj.seek(0, 2)
			size = fileobj.tell()

		# If we don't get an offset, try to skip an ID3v2 tag.
		if offset is None:
			fileobj.seek(0, 0)
			idata = fileobj.read(10)
			try: id3, insize = struct.unpack('>3sxxx4s', idata)
			except struct.error: id3, insize = '', 0
			insize = BitPaddedInt(insize)
			if id3 == 'ID3' and insize > 0:
				offset = insize
			else: offset = 0

		# Try to find two valid headers (meaning, very likely MPEG data)
		# at the given offset, 30% through the file, 60% through the file,
		# and 90% through the file.
		for i in [offset, 0.3 * size, 0.6 * size, 0.9 * size]:
			try: self.__try(fileobj, int(i), size - offset)
			except error, e: pass
			else: break
		# If we can't find any two consecutive frames, try to find just
		# one frame back at the original offset given.
		else:
			self.__try(fileobj, offset, size - offset, False)
			self.sketchy = True

	def __try(self, fileobj, offset, real_size, check_second=True):
		# This is going to be one really long function; bear with it,
		# because there's not really a sane point to cut it up.
		fileobj.seek(offset, 0)

		# We "know" we have an MPEG file if we find two frames that look like
		# valid MPEG data. If we can't find them in 32k of reads, something
		# is horribly wrong (the longest frame can only be about 4k). This
		# is assuming the offset didn't lie.
		data = fileobj.read(32768)

		frame_1 = data.find("\xff")
		while 0 <= frame_1 <= len(data) - 4:
			frame_data = struct.unpack(">I", data[frame_1:frame_1 + 4])[0]
			if (frame_data >> 16) & 0xE0 != 0xE0:
				frame_1 = data.find("\xff", frame_1 + 2)
			else:
				version = (frame_data >> 19) & 0x3
				layer = (frame_data >> 17) & 0x3
				protection = (frame_data >> 16) & 0x1
				bitrate = (frame_data >> 12) & 0xF
				sample_rate = (frame_data >> 10) & 0x3
				padding = (frame_data >> 9) & 0x1
				private = (frame_data >> 8) & 0x1
				self.mode = (frame_data >> 6) & 0x3
				mode_extension = (frame_data >> 4) & 0x3
				copyright = (frame_data >> 3) & 0x1
				original = (frame_data >> 2) & 0x1
				emphasis = (frame_data >> 0) & 0x3
				if (version == 1 or layer == 0 or sample_rate == 0x3 or
					bitrate == 0 or bitrate == 0xF):
					frame_1 = data.find("\xff", frame_1 + 2)
				else: break
		else:
			raise HeaderNotFoundError("can't sync to an MPEG frame")

		# There is a serious problem here, which is that many flags
		# in an MPEG header are backwards.
		self.version = [2.5, None, 2, 1][version]
		self.layer = 4 - layer
		self.protected = not protection
		self.padding = bool(padding)

		self.bitrate = self.__BITRATE[(self.version, self.layer)][bitrate]
		self.bitrate *= 1000
		self.sample_rate = self.__RATES[self.version][sample_rate]

		if self.layer == 1:
			frame_length = (12 * self.bitrate / self.sample_rate + padding) * 4
			frame_size = 384
		else:
			frame_length = 144 * self.bitrate / self.sample_rate + padding
			frame_size = 1152

		if check_second:
			possible = frame_1 + frame_length
			if possible > len(data) + 4:
				raise HeaderNotFoundError("can't sync to second MPEG frame")
			frame_data = struct.unpack(">H", data[possible:possible + 2])[0]
			if frame_data & 0xFFE0 != 0xFFE0:
				raise HeaderNotFoundError("can't sync to second MPEG frame")

		frame_count = real_size / float(frame_length)
		samples = frame_size * frame_count
		self.length = samples / self.sample_rate

		# Try to find/parse the Xing header, which trumps the above length
		# and bitrate calculation.
		fileobj.seek(offset, 0)
		data = fileobj.read(32768)
		try:
			xing = data[:-4].index("Xing")
		except ValueError: pass
		else:
			self.preset = self.get_preset(data[xing:])
			self.vbr = True
			# If a Xing header was found, this is definitely MPEG audio.
			self.sketchy = False
			flags = struct.unpack('>I', data[xing + 4:xing + 8])[0]
			if flags & 0x1:
				frame_count = struct.unpack('>I', data[xing + 8:xing + 12])[0]
				samples = frame_size * frame_count
				self.length = (samples / self.sample_rate) or self.length
			if flags & 0x2:
				bytes = struct.unpack('>I', data[xing + 12:xing + 16])[0]
				self.bitrate = int((bytes * 8) // self.length)
		
	def pprint(self):
		s = "MPEG %s layer %d, %d bps, %s Hz, %.2f seconds" % (
			self.version, self.layer, self.bitrate, self.sample_rate,
			self.length)
		if self.sketchy: s += " (sketchy)"
		return s

	def get_preset(self, data):
		pattern = ">4s3l100xL9s2B8x2B5xH"
		pattern_size = struct.calcsize(pattern)
		mp3header = struct.unpack(pattern, data[0:pattern_size])
		if mp3header[5][:4] == "LAME":
			self.lameversion = str(mp3header[5][:8])
			try:
				version = float(mp3header[5][4:8])
			except ValueError:
				version = -1
			vbrmethod = mp3header[6] & 15
			lowpass = mp3header[7]
			ath = mp3header[8] & 15
			preset = mp3header[10] & 2047
			if preset > 0:
				if preset == 320:
					return "-b 320"
				if preset in (410, 420, 430, 440, 450, 460, 470, 480, 490, 500):
					if vbrmethod == 4:
						return "-V %d --vbr-new" % ((500 - preset) / 10)
					return "-V %d" % ((500 - preset) / 10)
				# deprecated values?
				if preset == 1000: return "--r3mix"
				if preset == 1001: return "--alt-preset standard"
				if preset == 1002: return "--alt-preset extreme"
				if preset == 1003: return "--alt-preset insane"
				if preset == 1004: return "--alt-preset fast standard"
				if preset == 1005: return "--alt-preset fast extreme"
				if preset == 1006: return "--alt-preset medium"
				if preset == 1007: return "--alt-preset fast medium"
			if version < 3.90 and version > 0:  #lame version
				if vbrmethod == 8:  #unknown
					if lowpass in (97, 98):
						if ath == 0:
							return "--r3mix"
			if version >= 3.90 and version < 3.97:  #lame version
				if vbrmethod == 3:  #vbr-old / vbr-rh
					if lowpass in (195, 196):
						if ath in (2, 4):
							return "--alt-preset extreme"
					if lowpass == 190:
						if ath == 4:
							return "--alt-preset standard"
					if lowpass == 180:
						if ath == 4:
							return "--alt-preset medium"
				if vbrmethod == 4:  #vbr-mtrh
					if lowpass in (195, 196):
						if ath in (2, 4):
							return "--alt-preset fast extreme"
						if ath == 3:
							return "--r3mix"
					if lowpass == 190:
						if ath == 4:
							return "--alt-preset fast standard"
					if lowpass == 180:
						if ath == 4:
							return "--alt-preset fast medium"
				if vbrmethod in (1, 2):  #abr
					if lowpass in (205, 206):
						if ath in (2, 4):
							return "--alt-preset insane"
		return None

class MP3(ID3FileType):
	"""An MPEG audio (usually MPEG-1 Layer 3) file."""

	_Info = MPEGInfo
	_mimes = ["audio/mp3", "audio/x-mp3", "audio/mpeg", "audio/mpg",
			  "audio/x-mpeg"]

	def score(filename, fileobj, header):
		filename = filename.lower()
		return (header.startswith("ID3") * 2 + filename.endswith(".mp3") +
				filename.endswith(".mp2") + filename.endswith(".mpg") +
				filename.endswith(".mpeg"))
	score = staticmethod(score)

Open = MP3