#!/usr/bin/python
# -*- coding: utf-8 -*-

from hwinfo import HWInfo
import pprint

hw = HWInfo()

for dev in hw.devices:
	print dev

#print hw.processor
#print "Sockets: %s" % hw.processor
#print "Processors: %s" % pprint.pformat(hw.processor.processors)
#print hw.memory

#print "devices:"
#for dev in hw.devices:
#	print dev, dev.driver