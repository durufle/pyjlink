# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Laurent Bonnet
#
# License: MIT

import utility

import pyjlink

import behave

import os
import multiprocessing
import sys
import time


@behave.given('my J-link is connected')
def step_connected(context):
    """
    Asserts that the J-Link is connected.

    :param context: the ``Context`` instance
    """
    assert context.jlink.connected()


@behave.given('device {device}')
def step_connect_device(context, device):
    """
    Tries to connect to the given.

    :param context: the ``Context`` instance
    :param device: name of the device to connect to
    """
    try:
        jlink = context.jlink
        jlink.connect(str(device))
        # jlink.set_reset_strategy(pyjlink.JLinkResetStrategyCortexM3.NORMAL)
    except pyjlink.JLinkException as e:
        if e.code == pyjlink.JLinkGlobalErrors.VCC_FAILURE:
            context.scenario.skip(reason='Target is not powered.')
        elif e.code == pyjlink.JLinkGlobalErrors.NO_CPU_FOUND:
            context.scenario.skip(reason='Target core not found.')


@behave.given('target interface {interface}')
def step_target_interface(context, interface):
    """
    Sets the target interface for the JLink.

    :param context: the ``Context`` instance
    :param interface: the interface to use for the J-Link
    """
    if interface.lower() == 'jtag':
        context.jlink.set_tif(pyjlink.enums.JLinkInterfaces.JTAG)
    elif interface.lower() == 'swd':
        context.jlink.set_tif(pyjlink.enums.JLinkInterfaces.SWD)
    else:
        assert False, 'Unknown interface: %s' % interface


@behave.given('I close the J-Link')
def step_close(context):
    """
    Closes the J-Link.

    :param context: the ``Context`` instance
    """
    context.jlink.close()


@behave.when('I reset my device')
def step_device_reset(context):
    """
    Resets the target connected to the J-Link.

    :param context: the ``Context`` instance
    """
    jlink = context.jlink
    jlink.power_on()
    jlink.coresight_configure()
    jlink.reset(halt=False)
    time.sleep(1)


@behave.when('I flash the firmware {firmware}')
def step_flash_firmware_when(context, firmware):
    """
    Tries to flash the firmware.

    :param context: the ``Context`` instance
    :param firmware: the name of the firmware to flash
    """
    return step_flash_firmware_retries(context, firmware, 0)


@behave.when('I read the firmware {firmware} into a bytestream')
def step_read_firmware(context, firmware):
    """
    Reads the firmware file into a bytestream.

    :param context: the ``Context`` instance
    :param firmware: the name of the firmware to flash
    """
    firmware = utility.firmware_path(str(firmware))
    data = []
    with open(firmware, 'rb') as f:
        byte = f.read(1)
        while byte:
            data.append(ord(byte))
            byte = f.read(1)
    context.data = data


@behave.when('I halt the device')
def step_halt(context):
    """
    Halts the J-Link target.

    :param context: the ``Context`` instance
    """
    context.jlink.halt()


@behave.when('I create a new process with my J-Link')
def step_create_process(context):
    """
    Creates a new process to access the J-Link.

    :param context: the ``Context`` instance
    """
    context.process = multiprocessing.Process


@behave.then('the device should be halted')
def step_is_halted(context):
    """
    Assets that the device is halted / no longer running.

    :param context: the ``Context`` instance
    """
    assert context.jlink.halted()


@behave.then('the emulator should be connected')
def step_not_connected(context):
    """
    Checks that the JLink is not open.

    :param context: the ``Context`` instance
    """
    assert context.jlink.opened()
    assert context.jlink.connected()


@behave.then('the emulator should not be connected')
def step_not_connected(context):
    """
    Checks that the JLink is not open.

    :param context: the ``Context`` instance
    """
    assert not context.jlink.opened()
    assert not context.jlink.connected()


@behave.then('I can flash the firmware {firmware} with 1 retry')
def step_flash_firmware(context, firmware):
    """
    Tries to flash the firmware.

    :param context: the ``Context`` instance
    :param firmware: the name of the firmware to flash
    """
    return step_flash_firmware_retries(context, firmware, 1)


@behave.then('I can flash the firmware with {retries} retries')
def step_flash_firmware_bytestream_retries(context, retries):
    """
    Tries to flash the firmware from a bytestream.

    :param context: the ``Context`` instance
    :param retries: the number of retries when flashing
    """
    jlink = context.jlink
    retries = int(retries)
    data = context.data

    while retries >= 0:
        try:
            res = jlink.flash(context.data, 0)
            if res >= 0:
                break
        except pyjlink.JLinkException as e:
            retries = retries - 1

    assert retries >= 0

    written = list(map(int, jlink.memory_read8(0, len(data))))
    assert written == data


@behave.then('I can flash the firmware {firmware} with {retries} retries')
def step_flash_firmware_retries(context, firmware, retries):
    """
    Tries to flash the firmware with the given number of retries.

    :param context: the ``Context`` instance
    :param firmware: the name of the firmware to flash
    :param retries: the number of retries to do
    """
    jlink = context.jlink
    retries = int(retries)
    firmware = utility.firmware_path(str(firmware))
    assert firmware is not None

    while True:
        try:
            res = utility.flash_k21(jlink, firmware)
            if res >= 0:
                break
            else:
                retries = retries - 1
        except pyjlink.JLinkException as e:
            sys.stderr.write('%s%s' % (str(e), os.linesep))
            retries = retries - 1

        if retries < 0:
            break

    assert retries >= 0


@behave.then('a new J-Link should not be connected')
def step_new_jlink_not_connected(context):
    """
    Asserts that a new J-Link instance will not be connected.

    :param context: the ``Context`` instance
    """
    jlink_a, jlink_b = context.jlink, pyjlink.JLink()

    assert not jlink_b.opened()
    assert jlink_a.opened() != jlink_b.opened()

    assert not jlink_b.connected()
    assert jlink_a.connected() != jlink_b.connected()

    assert jlink_a.num_connected_emulators() == jlink_b.num_connected_emulators()

    jlink_b.close()

    assert jlink_a.opened()
    assert jlink_a.connected()


@behave.then('that process\'s J-Link is also connected')
def step_process_jlink_connected(context):
    """
    Asserts that the J-Link is connected in the second process.

    :param context: the ``Context`` instance
    """
    def f(jlink, queue):
        queue.put(jlink.opened())
        queue.put(jlink.connected())

    queue = multiprocessing.Queue()
    process = context.process(target=f, args=(context.jlink, queue))

    process.start()
    process.join()

    assert all(queue.get() for _ in range(2))


@behave.then('I should not be able to open a new connection to it')
def step_connection_open_jlink(context):
    """
    Asserts that we cannot open a new connection to an opened J-Link.

    :param context: the ``Context`` instance
    """
    serial_no = context.jlink.serial_number
    new_jlink = pyjlink.JLink()

    try:
        new_jlink.open(serial_no=serial_no)
    except pyjlink.JLinkException as e:
        pass
    else:
        assert False
