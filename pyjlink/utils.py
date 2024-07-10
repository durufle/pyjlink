# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Laurent Bonnet
#
# License: MIT
"""
utils module
"""

import platform
import sys
from . import enums


class Utils:
    """
    Utils class
    """
    @staticmethod
    def is_integer(val):
        """
        Returns whether the given value is an integer.

        :param val : value to check

        :return:
          ``True`` if the given value is an integer, otherwise ``False``.
        """
        try:
            val += 1
        except TypeError:
            return False
        return True

    @staticmethod
    def is_natural(val) -> bool:
        """
        Returns whether the given value is a natural number.

        :param val : value to check

        :return:
          ``True`` if the given value is a natural number, otherwise ``False``.
        """
        return Utils.is_integer(val) and (val >= 0)

    @staticmethod
    def is_os_64bit() -> bool:
        """
        Returns whether the current running platform is 64bit.

        :return:
          True if the platform is 64bit, otherwise False.
        """
        return platform.machine().endswith('64')

    @staticmethod
    def noop(*args, **kwargs):
        """
        No-op.  Does nothing.

        :param kwargs: keyword arguments dictionary
        """
        pass

    @staticmethod
    def unsecure_hook_dialog(title: str, msg: str, flags: int):
        """
        No-op that ignores the dialog.

        Args:
        :param title: title of the unsecure dialog
        :param msg: text of the unsecure dialog
        :param flags: flags specifying which values can be returned

        :return:
          ``enums.JLinkFlags.DLG_BUTTON_NO``
        """
        return enums.JLinkFlags.DLG_BUTTON_NO

    @staticmethod
    def progress_bar(iteration: int,
                     total: int,
                     prefix=None,
                     suffix=None,
                     decs=1,
                     length=100):
        """
        Creates a console progress bar.

        This should be called in a loop to create a progress bar.

        See `StackOverflow <http://stackoverflow.com/questions/3173320/>`__.

        :param iteration: current iteration
        :param total: total iterations
        :param prefix: prefix string
        :param suffix: suffix string
        :param decs: positive number of decimals in percent complete
        :param length: character length of the bar

        :note:
          This function assumes that nothing else is printed to the console in the interim.
        """
        if prefix is None:
            prefix = ''

        if suffix is None:
            suffix = ''

        format_str = '{0:.' + str(decs) + 'f}'
        percents = format_str.format(100 * (iteration / float(total)))
        filled_length = int(round(length * iteration / float(total)))
        bar = '█' * filled_length + '-' * (length - filled_length)

        prefix, suffix = prefix.strip(), suffix.strip()

        sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix))
        sys.stdout.flush()

        if iteration == total:
            sys.stdout.write('\n')
            sys.stdout.flush()

    @staticmethod
    def flash_progress_callback(action: str, progress_string: str, percentage: int):
        """
        Callback that can be used with ``JLink.flash()``.

        This callback generates a progress bar in the console to show the progress
        of each of the steps of the flash.

        :param action: the current action being invoked
        :param progress_string: the current step in the progress
        :param percentage: the percent to which the current step has been done

        :note:
        This function ignores the compare action.
        """
        if action.lower() != 'compare':
            Utils.progress_bar(min(100, percentage), 100, prefix=action)

    @staticmethod
    def calculate_parity(n):
        """
        Calculates and returns the parity of a number.

        The parity of a number is ``1`` if the number has an odd number of ones
        in its binary representation, otherwise ``0``.

        :param n: the number whose parity to calculate

        :return:
          ``1`` if the number has an odd number of ones, otherwise ``0``.

        :raise:
          ValueError: if ``n`` is less than ``0``.
        """
        if not Utils.is_natural(n):
            raise ValueError('Expected n to be a positive integer.')

        y = 0
        n = abs(n)
        while n:
            y += n & 1
            n = n >> 1
        return y & 1
