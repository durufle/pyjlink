# Copyright 2017 Square, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
pyjlink __init__ module
"""
__version__ = '0.0.0'
__title__ = 'pyjlink'
__author__ = 'Square Embedded Software Team'
__author_email__ = 'laurent.bonnet@st.com'
__copyright__ = 'Copyright 2024 STMicroelectronics, Inc.'
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
