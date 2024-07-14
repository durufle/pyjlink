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
import sys


def main( device: str):
    """
    Prints the core's information.

    :param device: the target CPU

    :return:
      Always returns ``0``.

    :raise:
      JLinkException: on error
    """
    buf = StringIO.StringIO()
    jlink = pyjlink.JLink(log=buf.write, detailed_log=buf.write)
    jlink.open()

    jlink.set_tif(pyjlink.enums.JLinkInterfaces.JTAG)
    jlink.connect(device, verbose=True)
    jlink.set_log_file("./probe.log")
    print(f"Firmware version        : {jlink.firmware_version}")
    print(f"Compatible firmware     : {jlink.compatible_firmware_version}")
    print(f"Is firmware outdated ?  : {jlink.firmware_outdated()}")
    print(f"Is firmware newer ?     : {jlink.firmware_newer()}")
    print(f"hardware version        : {jlink.hardware_version}")
    print(f"probe features          : {jlink.features}")
    print(f"probe name              : {jlink.product_name}")
    print(f"probe serial number     : {jlink.serial_number}")
    print(f"probe connected info    : {jlink.connected_emulators()}")
    oem = jlink.oem
    if oem:
        print(f"probe oem               : {jlink.oem}")

    print(f"current jtag speed      : {jlink.speed}")
    print(f"jtag speed  info        : {jlink.speed_info}")
    print(f"supported tif           : {hex(jlink.supported_tif()).upper()}")
    print(f"current tif             : {jlink.tif}")
    print(f"licenses                : {jlink.licenses}")
    print(f"Selected device         : {jlink.index}")


if __name__ == '__main__':
    exit(main("CY8C5868XXXLP"))

