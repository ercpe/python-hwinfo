# -*- coding: utf-8 -*-
from hwinfo.impl.base import BaseHWInfo, ProcessorInfo, PCIDeviceInfo
import re

MEM_INFO_RE = re.compile("^(.*):\s+(\d+)\s?([kBGM]*)")


class LinuxHWInfo(BaseHWInfo):

	def __init__(self):
		super(BaseHWInfo, self).__init__()
		self._devices = []

	@property
	def memory(self):
		with open('/proc/meminfo', 'r') as f:
			for line in [x.strip() for x in f.readlines()]:
				match = MEM_INFO_RE.match(line)
				if match:
					key, value, unit = match.groups()
					if key == "MemTotal":
						return self.get_value(long(value), unit.strip())

	@property
	def processor(self):
		# this is a naive implementation and may break on other archs...

		with open('/proc/cpuinfo', 'r') as f:
			cpus = []

			current = {}
			for line in [x.strip() for x in f.readlines()]:
				#print line

				if not line:
					if current:
						cpus.append(current)
						current = {}
					continue

				key = line[:line.index(':')].strip()
				value = line[line.index(':')+1:].strip()
				current[key] = value

			if current:
				cpus.append(current)

		data = {}

		physicals = list(set([int(d.get('physical id', 0)) for d in cpus]))
		data['sockets'] = len(physicals)
		data['processors'] = []

		for phy_id in physicals:
			proc_info = {}

			virt_processors = [d for d in cpus if int(d.get('physical id', -1)) == phy_id]

			proc_info['model'] = virt_processors[0]
			del proc_info['model']['core id']

			core_ids = list(set([int(d.get('core id', 0)) for d in virt_processors]))
			proc_info['no_cores'] = len(core_ids)

			data['processors'].append(proc_info)

		return ProcessorInfo(data)

	@property
	def devices(self):
		"""
		Returns a list of PCIDeviceInfo objects with the data from /proc/bus/pci/devices
		"""
		if not self._devices:
			devs = []
			with open('/proc/bus/pci/devices', 'r') as f:
				for line in [x.strip() for x in f.readlines()]:
					parts = line.split('\t')

					driver = None
					if len(parts) == 18:
						driver = parts[17]

					bus_devfunc = parts[0]
					vendor_device = parts[1]

					bus = bus_devfunc[0:2]
					devfunc = bus_devfunc[2:]

					vendor = vendor_device[0:4]
					device = vendor_device[4:]

					devs.append(PCIDeviceInfo(bus=bus, devfunc=devfunc, vendor=vendor, device=device, driver=driver))

			self._devices = devs

		return self._devices
