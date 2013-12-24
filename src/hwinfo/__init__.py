# -*- coding: utf-8 -*-

import sys

if sys.platform in ["linux1", "linux2"]:
	from impl.linux import LinuxHWInfo as HWInfo
else:
	raise Exception("Unsupported platform: %s" % sys.platform)