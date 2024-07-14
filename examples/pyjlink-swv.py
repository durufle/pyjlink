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
import string
import sys
import time


def serial_wire_viewer(device):
    """
    Implements a Serial Wire Viewer (SWV).

    A Serial Wire Viewer (SWV) allows us implement real-time logging of output
    from a connected device over Serial Wire Output (SWO).

    :param device: the target CPU

    :return:
      Always returns ``0``.

    :raise:
      JLinkException: on error
    """
    buf = StringIO.StringIO()
    jlink = pyjlink.JLink(log=buf.write, detailed_log=buf.write)
    jlink.open()

    # Use Serial Wire Debug as the target interface.  Need this in order to use
    # Serial Wire Output.
    jlink.set_tif(pyjlink.enums.JLinkInterfaces.SWD)
    jlink.connect(device, verbose=True)
    jlink.coresight_configure()
    jlink.set_reset_strategy(pyjlink.enums.JLinkResetStrategyCortexM3.RESETPIN)

    # Have to halt the CPU before getting its speed.
    jlink.reset()
    jlink.halt()

    cpu_speed = jlink.cpu_speed()
    swo_speed = jlink.swo_supported_speeds(cpu_speed, 10)[0]

    # Start logging serial wire output.
    jlink.swo_start(swo_speed)
    jlink.swo_flush()

    # Output the information about the program.
    sys.stdout.write('Serial Wire Viewer\n')
    sys.stdout.write('Press Ctrl-C to Exit\n')
    sys.stdout.write('Reading data from port 0:\n\n')

    # Reset the core without halting so that it runs.
    jlink.reset(ms=10, halt=False)

    # Use the `try` loop to catch a keyboard interrupt in order to stop logging
    # serial wire output.
    try:
        while True:
            # Check for any bytes in the stream.
            num_bytes = jlink.swo_num_bytes()

            if num_bytes == 0:
                # If no bytes exist, sleep for a bit before trying again.
                time.sleep(1)
                continue

            data = jlink.swo_read_stimulus(0, num_bytes)
            sys.stdout.write(''.join(map(chr, data)))
            sys.stdout.flush()
    except KeyboardInterrupt:
        pass

    sys.stdout.write('\n')

    # Stop logging serial wire output.
    jlink.swo_stop()

    return 0


if __name__ == '__main__':
    exit(serial_wire_viewer("CY8C6XX7_CM4"))
