# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Laurent Bonnet
#
# License: MIT

"""
basic core example
"""

import pyjlink

try:
    import StringIO
except ImportError:
    import io as StringIO


def main(device: str):
    """
    Prints the core's information.

    :param device: the target CPU (e.g. STM32L552ZE, CY8C6XX7_CM4)

    :return:
      Always returns ``0``.

    :raise:
      JLinkException: on error
    """
    buf = StringIO.StringIO()
    jlink = pyjlink.JLink(log=buf.write, detailed_log=buf.write)
    jlink.open()

    # Use Serial Wire Debug as the target interface.
    jlink.set_tif(pyjlink.enums.JLinkInterfaces.SWD)
    jlink.connect(device, verbose=True)

    print(f'ARM Id                  : {hex(jlink.core_id()).upper()}')
    print(f'CPU Id                  : {hex(jlink.core_cpu()).upper()}')
    print(f'Core Name               : {jlink.core_name()}')
    print(f'Device Family           : {jlink.device_family()}')

    print(f"etm supported           : {jlink.etm_supported}")
    print("Register list...")

    regs = []
    indexes = jlink.register_list()
    for i in indexes:
        regs.append(jlink.register_name(i))
    print(f"Register :  {regs}")


# NRF5340_XXAA_APP, CY8C6XX7_CM4, STM32L552ZE

if __name__ == '__main__':
    exit(main("CORTEX-A35"))
