# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Laurent Bonnet
#
# License: MIT

from . import enums


class JLinkException(enums.JLinkGlobalErrors, Exception):
    """
    Generic J-Link exception."""

    def __init__(self, code):
        """
        Generates an exception by coercing the given ``code`` to an error
        string if is a number, otherwise assumes it is the message.

        Args:
          code (object): message or error code
        """
        message = code

        self.code = None
        if isinstance(code,int):
            message = self.to_string(code)
            self.code = code

        super(JLinkException, self).__init__(message)
        self.message = message


class JLinkEraseException(enums.JLinkEraseErrors, JLinkException):
    """J-Link erase exception."""
    pass


class JLinkFlashException(enums.JLinkFlashErrors, JLinkException):
    """J-Link flash exception."""
    pass


class JLinkWriteException(enums.JLinkWriteErrors, JLinkException):
    """J-Link write exception."""
    pass


class JLinkReadException(enums.JLinkReadErrors, JLinkException):
    """J-Link read exception."""
    pass


class JLinkDataException(enums.JLinkDataErrors, JLinkException):
    """J-Link data event exception."""
    pass


class JLinkRTTException(enums.JLinkRTTErrors, JLinkException):
    """J-Link RTT exception."""
    pass
