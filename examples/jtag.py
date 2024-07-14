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
from array import array


def main():
    """
    Main function.
    """
    buf = StringIO.StringIO()
    jlink = pyjlink.JLink(log=buf.write, detailed_log=buf.write)
    jlink.open()
    jlink.set_speed(4000)
    print(f"speed info      : {jlink.speed_info}")
    # print(f"device id       : {hex(jlink.jtag_device_id(0))}")
    # print(f"device info     : {jlink.jtag_device_info(0)}")

    data = array('B', [0,0,0,0])
    position = jlink.jtag_store_data(data, 32)
    print(f"device read     : position = {position}, value = {hex(jlink.jtag_get_u32(position))}")
    # jlink.close()


if __name__ == '__main__':
    main()
