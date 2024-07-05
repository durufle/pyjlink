# -*- coding: utf-8 *-*
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
# Example Endianness.
#
# This module demonstrates getting the endianess of the target.
#
# Usage: endian.py jlink_serial_number device
# Author: Ford Peprah
# Date: October 11th, 2016
# Copyright: 2016 Square, Inc.

import pyjlink

try:
    import StringIO
except ImportError:
    import io as StringIO


def main(jlink_serial: int, device: str):
    """Main function.

    Args:
      jlink_serial: the J-Link serial number
      device: the target CPU

    Returns:
      ``None``

    Raises:
      JLinkException: on error
    """
    jlink = pyjlink.JLink()
    print("-> Try to connect without open...")
    try:
        jlink.connect('device', verbose=True)
    except pyjlink.errors.JLinkException as e:
        print(e)

    print("-> Open then Try to connect...")
    jlink.open()
    try:
        jlink.connect(device)
    except pyjlink.errors.JLinkException as e:
        print(e)
    print(f"Is connected ? : {jlink.connected()}")
    print(f"Is halted ?    : {jlink.halted()}")


if __name__ == '__main__':
    main(jlink_serial=504502376, device="CY8C5868XXXLP")
