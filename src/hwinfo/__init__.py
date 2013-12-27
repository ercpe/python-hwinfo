# -*- coding: utf-8 -*-

import sys

if sys.platform == "linux2":
	from impl.linux import LinuxHWInfo as HWInfo
else:
	raise Exception("Unsupported platform: %s" % sys.platform)