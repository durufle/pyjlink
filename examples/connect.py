# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Laurent Bonnet
#
# License: MIT

"""
Connection examples
"""
import pyjlink

try:
    import StringIO
except ImportError:
    import io as StringIO


def main(device: str):
    """
    Main function.

    :param device: the target CPU

    :raise:
      JLinkException: on error
    """
    buf = StringIO.StringIO()
    jlink = pyjlink.JLink(log=buf.write, detailed_log=buf.write)
    print("-> Try to connect without open...")
    try:
        jlink.connect('device', verbose=True)
    except pyjlink.errors.JLinkException as e:
        print(e)

    print("-> Open then Try to connect...")
    jlink.open()
    jlink.set_tif(pyjlink.enums.JLinkInterfaces.SWD)
    if jlink.opened():
        print(f"The jlink is opened.")
    try:
        jlink.connect(device)
        print(f"Is connected ? : {jlink.connected()}")
        print(f"Is halted ?    : {jlink.halted()}")
    except pyjlink.errors.JLinkException as e:
        print(e)



# CORTEX-A35
if __name__ == '__main__':
    main(device="CORTEX-A35")
