#!/usr/bin/env python

from verman import Version
pir_version = Version("pir", 0, 1, 1, releaselevel="dev", init_file=__file__)
__version__ = pir_version.mmm
