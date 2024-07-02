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

    print(f'ARM Id                  : {hex(jlink.core_id()).upper()}')
    print(f'CPU Id                  : {hex(jlink.core_cpu()).upper()}')
    print(f'Core Name               : {jlink.core_name()}')
    print(f'Device Family           : {jlink.device_family()}')


if __name__ == '__main__':
    exit(main(504502376, "STM32L552ZE"))
