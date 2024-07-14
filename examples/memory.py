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
    Prints the core's information.

    Args:
      jlink_serial (str): the J-Link serial number
      device (str): the target CPU

    Returns:
      Always returns ``0``.

    Raises:
      JLinkException: on error
    """
    buf = StringIO.StringIO()
    jlink = pyjlink.JLink(log=buf.write, detailed_log=buf.write)
    jlink.open(serial_no=jlink_serial)

    # Use Serial Wire Debug as the target interface.
    jlink.set_tif(pyjlink.enums.JLinkInterfaces.SWD)
    jlink.connect(device, verbose=True)

    print(f'ARM Id                          : {hex(jlink.core_id())}')
    print(f'CPU Id                          : {hex(jlink.core_cpu())}')
    print(f'Core Name                       : {jlink.core_name()}')
    print(f'Device Family                   : {jlink.device_family()}')

    print(f'Read 16 bytes a address 0       : {list(map(hex,jlink.memory_read8(0,16)))}')
    print(f'Read  8 half-word a address 0   : {list(map(hex,jlink.memory_read16(0,8)))}')
    print(f'Read  4 word a address 0        : {list(map(hex,jlink.memory_read32(0,4)))}')
    print(f'Read  2 double a address 0      : {list(map(hex,jlink.memory_read64(0,2)))}')


if __name__ == '__main__':
    exit(main(504502376, "CY8C6XX7_CM4"))
