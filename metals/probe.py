#! /usr/bin/env python3

import os, os.path
import sys

try:
	"""
	If used in a package, package logging functions are used instead of stderr.
	"""
	from . import debug, info, warning, error, fatal
except:
	def error(*args, **kwargs):
		print(*args, file=sys.stderr, **kwargs)
	debug = info = warning = fatal = error

try:
	from pymediainfo import MediaInfo
except ImportError:
	fatal("pymediainfo not found")
	fatal("pip install --user git+git://github.com/sbraz/pymediainfo")
	sys.exit(1)


def probe(arg, **kwargs):
	if not os.path.exists(arg):
		fatal("'{}' not found".format(arg))
		return
	mi = MediaInfo.parse(arg, **kwargs)
	results = [ ('number of tracks', len(mi.tracks)) ]
	y = results.append
	for track in mi.tracks:
		if track.track_type == 'General':
			if len(mi.tracks) == 1:
				return
			y(("bandwidth kb",	track.overall_bit_rate/1e3))
			y(("container",		track.format))
			y(("duration",		track.duration))
			y(("file size",		track.file_size))
		elif track.track_type == 'Audio':
			y(("audio bandwidth kb",	track.bit_rate/1e3))
			y(("audio channels",		track.channel_s))
			y(("audio codec",			track.codec))
		elif track.track_type == 'Video':
			y(("height",				track.height))
			y(("width",					track.width))
			y(("video bandwidth Mb",	track.bit_rate/1e6))
			y(("video codec",			track.codec))
			y(("video framerate",		track.frame_rate))
	return results


def probe_many(args, map=map):
	results = {}
	for filename, minfo in zip(args, map(probe, args)):
		if minfo: results[filename] = minfo
		else: error("'{}' failed".format(filename))
	return results
