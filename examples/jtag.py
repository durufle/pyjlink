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


def main(serial: int, device: str):
    """
    Main function.

    Args:
      serial: the J-Link serial number
      device: the target CPU
    """
    buf = StringIO.StringIO()
    jlink = pyjlink.JLink(log=buf.write, detailed_log=buf.write)
    jlink.open()
    jlink.set_speed(4000)
    print(f"speed info      : {jlink.speed_info}")
    print(f"device id       : {jlink.jtag_device_id(0)}")
    print(f"device info     : {jlink.jtag_device_info(0)}")

    jlink.close()


if __name__ == '__main__':
    main(serial=504502376, device="CY8C6XX7_CM4")
