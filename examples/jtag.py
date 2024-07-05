# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Laurent Bonnet
#
# License: MIT

"""
basic jtag api example
"""

import pyjlink

try:
    import StringIO
except ImportError:
    import io as StringIO
import sys


def main(jlink_serial: int, device: str):
    """
    Main function.

    Args:
      jlink_serial: the J-Link serial number
      device: the target CPU
    """
    buf = StringIO.StringIO()
    jlink = pyjlink.JLink(log=buf.write, detailed_log=buf.write)
    jlink.open(serial_no=jlink_serial)
    jlink.connect(device)

    jlink.close()


if __name__ == '__main__':
    main(jlink_serial=504502376, device="CY8C6XX6_CM4")
