# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Laurent Bonnet
#
# License: MIT
"""
binpacker module
"""
import ctypes
import math


BITS_PER_BYTE = 8


def pack_size(value: int):
    """
    Returns the number of bytes required to represent a given value.

    :param value: the natural number whose size to get

    :return: The minimal number of bytes required to represent the given integer.

    :raise:
      ValueError: if ``value < 0``.
      TypeError: if ``value`` is not a number.
    """
    if value == 0:
        return 1
    elif value < 0:
        raise ValueError('Expected non-negative integer.')
    return int(math.log(value, 256)) + 1


def pack(value: int, nbits: int = None):
    """
    Packs a given value into an array of 8-bit unsigned integers.

    If ``nbits`` is not present, calculates the minimal number of bits required
    to represent the given ``value``.  The result is little endian.

    :param value: the integer value to pack
    :param nbits: optional number of bits to use to represent the value

    :return:
      An array of ``ctypes.c_uint8`` representing the packed ``value``.

    :raise:
      ValueError: if ``value < 0`` and ``nbits`` is ``None`` or ``nbits <= 0``.
      TypeError: if ``nbits`` or ``value`` are not numbers.
    """
    if nbits is None:
        nbits = pack_size(value) * BITS_PER_BYTE
    elif nbits <= 0:
        raise ValueError('Given number of bits must be greater than 0.')

    buf_size = int(math.ceil(nbits / float(BITS_PER_BYTE)))
    buf = (ctypes.c_uint8 * buf_size)()

    for (idx, _) in enumerate(buf):
        buf[idx] = (value >> (idx * BITS_PER_BYTE)) & 0xFF

    return buf
