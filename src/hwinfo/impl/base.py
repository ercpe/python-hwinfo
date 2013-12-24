# -*- coding: utf-8 -*-

import simplejson

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


class ProcessorInfo(object):

	def __init__(self, info):
		self.data = info

	@property
	def sockets(self):
		return self.data.get('sockets')

	@property
	def processors(self):
		return [ProcessorModelInfo(x['model']) for x in self.data.get('processors', [])]

	@property
	def no_processors(self):
		return len(self.processors)

	def __str__(self):
		return "Sockets: %s, Processors: %s" % (self.sockets, self.processors)


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

	def __repr__(self):
		return "Bus: %s, Device Function: %s, Vendor: %s, Device: %s" % (self.bus, self.devfunc, self.vendor, self.device)
