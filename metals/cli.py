#! /usr/bin/env python3

import os, os.path
import sys

from SimpleTable import Table

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

try:
	import multiprocessing
	pool = multiprocessing.Pool()
	map = pool.map
except:
	debug("multiprocessing not used")


def probe(*args, **kwargs):
	mi = MediaInfo.parse(*args, **kwargs)
	results = [ ('number of tracks', len(mi.tracks)) ]
	y = results.append
	for track in mi.tracks:
		if track.track_type == 'General':
			if len(mi.tracks) == 1:
				return None
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

def probe_many(args, **kwargs):
	return dict(zip(args, map(probe, args)))


def get_table(columns, lookup, **kwargs):
	ncols = len(columns)
	cns = [ cd if isinstance(cd, str) else cd[0] for cd in columns ]

	def to_row(arg):
		filename, attrs = arg
		row = [None]*ncols
		if attrs:
			attrs = dict(attrs)
			for i, cn in enumerate(cns):
				row[i] = attrs.pop(cn, "")
		return [filename]+row
	return Table(map(to_row, lookup.items()), fields=['filename']+columns)


def main(args=None):
	args = args or sys.argv[1:]
	"""
	You can customize the columns and their display like so:

	                      column name,   format string, format kwargs
	                      column name,     (optional)    (optional)

					  [  'container',									# No format stuff
					    ('bandwidth kb', '{:,.0f}"),					# Format is ,.0f
					    ('video codec',  '{:^{width}}', "{'width': 4}", # Format is centered, width forced to 4
	"""
	table = get_table([  'container',
	                    ('bandwidth kb', '{:,.0f}'),
						 'height',
						 'width',
						 'video codec',
						 'audio codec' ], probe_many(args))
	table.sort(key=lambda row: -row[4])


if __name__ == '__main__':
	sys.exit(main())
