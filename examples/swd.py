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
import sys
import time


def main(device: str):
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
            # Check the vector catch.
            if jlink.register_read(0x0) != 0x05:
                continue

            offset = jlink.register_read(0x1)
            handle, ptr, num_bytes = jlink.memory_read32(offset, 3)
            read = ''.join(map(chr, jlink.memory_read8(ptr, num_bytes)))

            if num_bytes == 0:
                # If no bytes exist, sleep for a bit before trying again.
                time.sleep(1)
                continue

            jlink.register_write(0x0, 0)
            jlink.step(thumb=True)
            jlink.restart(2, skip_breakpoints=True)

            sys.stdout.write(read)
            sys.stdout.flush()
    except KeyboardInterrupt:
        pass

    sys.stdout.write('\n')

    return 0


if __name__ == '__main__':
    exit(main("CY8C6XX7_CM4"))
