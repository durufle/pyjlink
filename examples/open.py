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
    Main function.

    :param device: the target CPU
    """
    buf = StringIO.StringIO()
    jlink = pyjlink.JLink(log=buf.write, detailed_log=buf.write)
    print(f" Is Open ? {jlink.opened()}")
    jlink.open()
    print(f" Is Open ? {jlink.opened()}")
    jlink.close()
    print(f" Is Open ? {jlink.opened()}")


# NRF5340_XXAA_APP, CY8C6XX7_CM4, STM32L552ZE

if __name__ == '__main__':
    main(device="CY8C6XX7_CM4")
