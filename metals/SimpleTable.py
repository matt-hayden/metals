
from collections import namedtuple

try:
	"""
	If used in a package, package logging functions are used instead of stderr.
	"""
	from . import debug, info, warning, error, fatal
except:
	def error(*args, **kwargs):
		print(*args, file=sys.stderr, **kwargs)
	debug = info = warning = fatal = error

class Field:
	def __init__(self, name, format_string='{:{width}}', format_kwargs=None):
		self.name = name
		self.format_string = format_string
		self.format_kwargs = format_kwargs or {'width': ''}
	def __call__(self, value, **overrides):
		if value is None:
			return "None"
		kwargs = dict(self.format_kwargs)
		if overrides:
			kwargs.update(overrides)
		return self.format_string.format(value, **kwargs)

class Table:
	def __init__(self, iterable, fields=None):
		self.factory = list
		if fields:
			self.fields = [ Field(f) if isinstance(f, str) else Field(*f) for f in fields ]
			class Row(namedtuple('Row', [ f.name for f in self.fields ], rename=True)):
				def __repr__(self): return repr( [ str(e) for e in self ] )
			def Row_maker(arg): return Row(*arg)
			self.factory = Row_maker
		else:
			self.fields = None
		self.rows = list(map(self.factory, iterable))
		if not self.fields:
			ncols = len(self.rows[0])
			self.fields = [ Field("F{:{width}d}".format(i, width=1 if (ncols < 11) else 3)) for i in range(ncols) ]
		self.detect_column_widths()
	def __iter__(self):
		return iter(self.rows)
	@property
	def columns(self): # transpose
		return zip(*self.rows)
	def format_row(self, row, **kwargs):
		for i, v in enumerate(row):
			yield self.fields[i](v, **kwargs)
	def detect_column_widths(self, sample=1024):
		def _get_rows_as_text(sample):
			for row in self.rows[:sample]:
				yield self.format_row(row)
		cols = zip(*_get_rows_as_text(sample))
		widths = [ max(len(v) for v in c) for c in cols ]
		for w, f in zip(widths, self.fields):
			if (f.format_kwargs.get('width', 0) or 0) < 1:
				f.format_kwargs['width'] = w
		return widths
	def get_lines(self, header=True, sep=" "):
		if header:
			header = []
			for f in self.fields:
				if 'width' in f.format_kwargs:
					w = f.format_kwargs['width']
					header.append("{:^{width}}".format(f.name[:w], width=w))
				else:
					header.append(f.name)
			yield sep.join(header)
		for row in self.rows:
			yield sep.join(self.format_row(row))
	def __repr__(self):
		return '\n'.join(self.get_lines())+'\n'
	def sort(self, *args, **kwargs):
		if args and kwargs:
			raise NotImplementedError()
		if not args:
			self.rows.sort(**kwargs)
		else: # TODO
			raise NotImplementedError()
			
