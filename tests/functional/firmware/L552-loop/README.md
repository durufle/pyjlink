# STM32L552 Loop

This build implements a simple polling loop.

## Building the Firmware

To build the firmware, run `make` from within the directory.  This will create
a build directory containing the binary files.

## Firmware Overview

This firmware does the following things on boot:

    1. Enters a polling loop incrementing a value.

# Board

Has been tested on NUCLEO-L552ZEQ board.