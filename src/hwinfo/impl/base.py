# -*- coding: utf-8 -*-
import simplejson
import os


class BaseHWInfo(object):

	def get_value(self, value, unit):
		if not unit:
			return value

		multi = 1
		for c in unit.lower():
			if c == 'k':
				multi = 1024
			elif c == 'm':
				multi = 1024 * 1024
			elif c == 'g':
				multi = 1024 * 1024 * 1024
			elif c == 't':
				multi = 1024 * 1024 * 1024 * 1024

		return value * multi

	@property
	def memory(self):
		pass

	@property
	def processor(self):
		pass

	@property
	def devices(self):
		pass

	def executable_exists(self, program):
		def is_exe(fpath):
			return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

		for path in os.environ["PATH"].split(os.pathsep):
			path = path.strip('"')
			exe_file = os.path.join(path, program)
			if is_exe(exe_file):
				return True

		return False

	def as_json(self):
		def serialize_default(o):
			if isinstance(o, set):
				return list(o)

			d = o.__dict__
			#for x in dir(self):
			#	print x, getattr(self, x)
			#print [p for p in dir(self) if isinstance(getattr(self,p),property)]
			[p for p in dir(self) if not isinstance(getattr(self,p),property)]
			#for prop in [p for p in dir(self) if not isinstance(getattr(self,p),property)]:
			#	print prop
				#pass
			return d

#		for property, value in vars(self).iteritems():
#			print property, value
		print simplejson.dumps(self, default=serialize_default)


class ProcessorInfo(object):

	def __init__(self, info):
		self.data = info

	def __getattr__(self, item):
		return self.data.get(item, None)

	@property
	def processors(self):
		return [ProcessorModelInfo(x['model']) for x in self.data.get('processors', [])]

	@property
	def no_processors(self):
		return len(self.processors)

	def __str__(self):
		return "Arch: %s, Sockets: %s, Cores: %s, Threads: %s, Processors: %s" % \
				(self.arch, self.sockets, self.cores, self.threads, self.processors)


class ProcessorModelInfo(object):

	def __init__(self, data):
		self.data = data

	@property
	def model_name(self):
		return self.data.get('model name')

	def __repr__(self):
		return self.model_name

	def __str__(self):
		return self.__repr__()


class PCIDeviceInfo(object):

	def __init__(self, **kwargs):
		self.data = kwargs

	def __getattr__(self, item):
		return self.data.get(item, None)

	@property
	def slot(self):
		if not self.devfunc:
			return None
		return (int(self.devfunc, 16) >> 3) & 0x1f

	@property
	def function(self):
		if not self.devfunc:
			return None

		return int(self.devfunc, 16) & 0x07

	def __repr__(self):
		return "Bus: %s, Device Function: %s, Vendor: %s, Device: %s" % (self.bus, self.devfunc, self.vendor, self.device)
