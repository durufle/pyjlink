# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Laurent Bonnet
#
# License: MIT

"""
basic endian-ess api example
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

    Returns:
      ``None``

    Raises:
      JLinkException: on error
    """
    buf = StringIO.StringIO()
    jlink = pyjlink.JLink(log=buf.write, detailed_log=buf.write)
    jlink.open(serial_no=jlink_serial)

    jlink.set_tif(pyjlink.enums.JLinkInterfaces.SWD)
    jlink.connect(device, verbose=True)

    # Figure out our original endian-ess first.
    big_endian = jlink.set_little_endian()
    if big_endian:
        jlink.set_big_endian()

    print('Target Endian Mode: %s Endian' % ('Big' if big_endian else 'Little'))


if __name__ == '__main__':
    main(504502376, "CY8C5868XXXLP")
