#! /usr/bin/env python3

import os, os.path
import sys


from .probe import probe_many
from .SimpleTable import Table


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
	import multiprocessing
	
	args = args or sys.argv[1:]
	"""
	You can customize the columns and their display like so:

	                      column name,   format string, format kwargs
	                      column name,     (optional)    (optional)

					  [  'container',									# No format stuff
					    ('bandwidth kb', '{:,.0f}"),					# Format is ,.0f
					    ('video codec',  '{:^{width}}', "{'width': 4}", # Format is centered, width forced to 4
	"""
	with multiprocessing.Pool() as pool:
		if not sys.flags.interactive:
			map = pool.map
		table = get_table([  'container',
							('bandwidth kb', '{:,.0f}'),
							 'height',
							 'width',
							 'video codec',
							 'audio codec' ], probe_many(args, map=map))
		table.sort(key=lambda row: -row[4])
	print(table)


if __name__ == '__main__':
	sys.exit(main())
