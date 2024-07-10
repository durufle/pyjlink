# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Laurent Bonnet
#
# License: MIT

from .unlock_kinetis import unlock_kinetis


def unlock(jlink, name) -> bool:
    """
    Unlocks a J-Link's target device.

    :param jlink: the connected J-Link device
    :param name: the MCU name (e.g. Kinetis)

    Supported Names:
      - Kinetis
      - freescale,
      - nxp

    :return:
      True if the device was unlocked, otherwise False.

    :raise:
      NotImplementedError: if no unlock method exists for the MCU.
    """
    if name.lower() in ['kinetis', 'freescale', 'nxp']:
        return unlock_kinetis(jlink)
    raise NotImplementedError('No unlock method for %s' % name)
