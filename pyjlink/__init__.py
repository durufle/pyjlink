# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Laurent Bonnet
#
# License: MIT
"""
pyjlink __init__ module
"""
__version__ = '0.0.0'
__title__ = 'pyjlink'
__author__ = 'ragnarok team'
__author_email__ = 'laurent.woolcap@free.com'
__copyright__ = 'Copyright 2024 '
__license__ = 'MIT'
__url__ = ''
__description__ = 'Python interface for SEGGER J-Link probe.'
__long_description__ = '''This module provides a Python implementation of the J-Link SDK by leveraging the SDK's DLL.'''

from .enums import *
from .errors import *
from .jlink import *
from .library import *
from .structs import *
from .unlockers import *
