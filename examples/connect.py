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


def main(jlink_serial: int, device: str):
    """
    Main function.

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
