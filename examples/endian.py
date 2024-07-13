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


def main(device: str):
    """
    Main function.

    :param device: the target CPU

    :raise:
      JLinkException: on error
    """
    buf = StringIO.StringIO()
    jlink = pyjlink.JLink(log=buf.write, detailed_log=buf.write)
    jlink.open()

    jlink.set_tif(pyjlink.enums.JLinkInterfaces.SWD)
    jlink.connect(device, verbose=True)

    # Figure out our original endian-ess first.
    big_endian = jlink.set_little_endian()
    if big_endian:
        jlink.set_big_endian()

    print('Target Endian Mode: %s Endian' % ('Big' if big_endian else 'Little'))


if __name__ == '__main__':
    main("CY8C6XX7_CM4")
