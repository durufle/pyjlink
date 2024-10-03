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


def main(device: str):
    """
    Prints the core's information.

    :param device: the target CPU

    :raises:
      JLinkException: on error
    """
    buf = StringIO.StringIO()
    jlink = pyjlink.JLink(log=buf.write, detailed_log=buf.write)
    jlink.open()

    # Use Serial Wire Debug as the target interface.
    jlink.set_tif(pyjlink.enums.JLinkInterfaces.SWD)
    jlink.connect(device, verbose=True)

    print(f'ARM Id                          : {hex(jlink.core_id())}')
    print(f'CPU Id                          : {hex(jlink.core_cpu())}')
    print(f'Core Name                       : {jlink.core_name()}')
    print(f'Device Family                   : {jlink.device_family()}')

    address = 0x54000E20

    # print(f'Read 16 bytes a address {address}        : {list(map(hex, jlink.memory_read8(address, 16)))}')
    # print(f'Read  8 half-word a address {address}    : {list(map(hex, jlink.memory_read16(address, 8)))}')
    print(f'Read  4 word a address {address}         : {list(map(hex, jlink.memory_read32(address, 1)))}')
    # print(f'Read  2 double a address {address}       : {list(map(hex, jlink.memory_read64(address, 2)))}')


# NRF5340_XXAA_APP, CY8C6XX7_CM4, STM32L552ZE

if __name__ == '__main__':
    exit(main("CORTEX-A35"))
