# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Laurent Bonnet
#
# License: MIT


import pyjlink
import sys
import time


def strace(device: str, trace_address: int, breakpoint_address: int):
    """
    Implements simple trace using the STrace API.

    Args:
      device: the device to connect to
      trace_address: address to begin tracing from
      breakpoint_address: address to breakpoint at
    """
    jlink = pyjlink.JLink()
    jlink.open()

    # Do the initial connection sequence.
    jlink.power_on()
    jlink.set_tif(pyjlink.JLinkInterfaces.SWD)
    jlink.connect(device)
    jlink.reset()

    # Clear any breakpoints that may exist as of now.
    jlink.breakpoint_clear_all()

    # Start the simple trace.
    op = pyjlink.JLinkStraceOperation.TRACE_START
    jlink.strace_clear_all()
    jlink.strace_start()

    # Set the breakpoint and trace events, then restart the CPU so that it
    # will execute.
    bphandle = jlink.breakpoint_set(breakpoint_address, thumb=True)
    trhandle = jlink.strace_code_fetch_event(op, address=trace_address)
    jlink.restart()
    time.sleep(1)

    # Run until the CPU halts due to the breakpoint being hit.
    while True:
        if jlink.halted():
            break

    # Print out all instructions that were captured by the trace.
    while True:
        instructions = jlink.strace_read(1)
        if len(instructions) == 0:
            break
        instruction = instructions[0]
        print(jlink.disassemble_instruction(instruction))

    jlink.power_off()
    jlink.close()


if __name__ == '__main__':
    exit(strace(sys.argv[1], int(sys.argv[2], 16), int(sys.argv[3], 16)))
