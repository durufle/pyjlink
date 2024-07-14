# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Laurent Bonnet
#
# License: MIT


import pyjlink

try:
    import StringIO
except ImportError:
    import io as StringIO


def main(jlink_serial: int, device: str):
    """
    Main function.

    Args:
      jlink_serial: the J-Link serial number
      device: the target CPU
    """
    buf = StringIO.StringIO()
    jlink = pyjlink.JLink(log=buf.write, detailed_log=buf.write)
    print(f" Is Open ? {jlink.opened()}")
    jlink.open(serial_no=jlink_serial)
    print(f" Is Open ? {jlink.opened()}")
    jlink.close()
    print(f" Is Open ? {jlink.opened()}")


if __name__ == '__main__':
    main(jlink_serial=504502376, device="STM32L552ZE")
