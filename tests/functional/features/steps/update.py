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

import pyjlink

import behave


@behave.given('I invalidate the firmware')
def step_firmware_invalidate(context):
    """
    Invalidates the emulator's firmware.

    :param context: the ``Context`` instance
    """
    context.jlink.invalidate_firmware()


@behave.then('I can update the firmware')
def step_firmware_update(context):
    """
    Asserts that the firmware can be updated.

    :param context: the ``Context`` instance
    """
    assert context.jlink.update_firmware() >= 0


@behave.then('I can force a firmware update')
def step_force_firmware_update(context):
    """
    Asserts that the firmware can be force updated.

    :param context: the ``Context`` instance
    """
    assert context.jlink.update_firmware() >= 0

    log_messages = context.log.getvalue()
    assert 'New firmware booted successfully' in log_messages
