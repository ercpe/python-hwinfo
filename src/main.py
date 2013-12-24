#!/usr/bin/python
# -*- coding: utf-8 -*-

from hwinfo import HWInfo
import pprint

hw = HWInfo()
print hw.processor
#print "Sockets: %s" % hw.processor
#print "Processors: %s" % pprint.pformat(hw.processor.processors)
#print hw.memory
