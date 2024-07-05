# -*- coding: utf-8 -*-
# Copyright 2017 Square, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Example core information printer.
#
# This module prints the core's information.
#
# Usage: core.py jlink_serial_number device
# Author: Ford Peprah
# Date: October 1st, 2016
# Copyright: 2016 Square, Inc.

import pyjlink

try:
    import StringIO
except ImportError:
    import io as StringIO
import sys


def main(jlink_serial: int, device: str):
    """Prints the core's information.

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
    # Set a log file
    jlink.set_log_file("./probe.log")
    print(f"Firmware version        : {jlink.firmware_version}")
    print(f"Compatible firmware     : {jlink.compatible_firmware_version}")
    print(f"Is firmware outdated ?  : {jlink.firmware_outdated}")
    print(f"Is firmware newer ?     : {jlink.firmware_newer}")
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
    exit(main(504502376, "CY8C5868XXXLP"))
