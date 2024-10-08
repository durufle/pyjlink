# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Laurent Bonnet
#
# License: MIT

import pyjlink
import argparse
import logging
import os
import six
import sys

from pyjlink.utils import Utils


class CommandMeta(type):
    """
    Metaclass for a command.
    """

    registry = {}

    def __new__(cls, name, parents, dct):
        """
        Creates a new Command class and validates it.

        Args:
          cls (Class): the class object being created
          name (name): the name of the class being created
          parents (list): list of parent classes
          dct (dictionary): class attributes

        Returns:
          ``Class``
        """
        new_class = super(CommandMeta, cls).__new__(cls, name, parents, dct)

        if name != 'Command':
            for attribute in ['name', 'description', 'help']:
                if attribute not in dct or dct[attribute] is None:
                    raise ValueError('%s cannot be None.' % attribute)
            CommandMeta.registry[name] = new_class

        return new_class


class Command(six.with_metaclass(CommandMeta)):
    """
    Base command-class.

    All commands should inherit from this class.

    Attributes:
      name: name of the command, should be unique.
      description: command description string.
      help: command help string.
    """
    name = None
    description = None
    help = None

    @staticmethod
    def create_jlink(args):
        """
        Creates an instance of a J-Link from the given arguments.

        Args:
          args (Namespace): arguments to construct the ``JLink`` instance from

        Returns:
          An instance of a ``JLink``.
        """
        jlink = pyjlink.JLink()
        jlink.open(args.serial_no, args.ip_addr)

        if hasattr(args, 'tif') and args.tif is not None:
            if args.tif.lower() == 'swd':
                jlink.set_tif(pyjlink.JLinkInterfaces.SWD)
            else:
                jlink.set_tif(pyjlink.JLinkInterfaces.JTAG)

        if hasattr(args, 'device') and args.device is not None:
            jlink.connect(args.device)

        return jlink

    @staticmethod
    def add_common_arguments(parser, has_device=False):
        """
        Adds common arguments to the given parser.

        Common arguments for a J-Link command are the target interface, and
        J-Link serial number or IP address.

        Args:
          parser (argparse.ArgumentParser): the parser to add the arguments to
          has_device (bool): boolean indicating if it has the device argument

        Returns:
          ``None``
        """
        if has_device:
            parser.add_argument('-t', '--tif', required=True, choices=['jtag', 'swd'], type=str.lower,
                                help='target interface (JTAG | SWD)')
            parser.add_argument('-d', '--device', required=True,
                                help='specify the target device name')

        group = parser.add_mutually_exclusive_group(required=False)
        group.add_argument('-s', '--serial', dest='serial_no',
                           help='specify the J-Link serial number')
        group.add_argument('-i', '--ip_addr', dest='ip_addr',
                           help='J-Link IP address')

        return None

    def add_arguments(self, parser):
        """
        Adds arguments to the given parser.

        Not implemented.  The derived class must implement this.

        Args:
          self (Command): the ``Command`` instance
          parser (argparse.ArgumentParser): the parser to add the arguments to

        Returns:
          ``None``

        Raises:
          NotImplementedError: always.
        """
        raise NotImplementedError('%s not implemented.' % self.__class__.__name__)

    def run(self, args):
        """Runs the command.

        Not implemented.  The derived class must implement this.

        Args:
          self (Command): the ``Command`` instance
          args (Namespace): the arguments passed on the command-line

        Returns:
          ``None``

        Raises:
          NotImplementedError: always.
        """
        raise NotImplementedError('%s not implemented.' % self.__class__.__name__)


class EraseCommand(Command):
    """Defines the erase command for erasing a device."""
    name = 'erase'
    description = 'Erases the target device.'
    help = 'erases the device connected to the J-Link'

    def add_arguments(self, parser):
        """
        Adds the erase command arguments to the parser.

        Args:
          self (EraseCommand): the ``EraseCommand`` instance
          parser (argparse.ArgumentParser): the parser to add the arguments to

        Returns:
          ``None``
        """
        return self.add_common_arguments(parser, True)

    def run(self, args):
        """Erases the device connected to the J-Link.

        Args:
          self (EraseCommand): the ``EraseCommand`` instance
          args (Namespace): the arguments passed on the command-line

        Returns:
          ``None``
        """
        jlink = self.create_jlink(args)
        erased = jlink.erase()
        print('Bytes Erased: %d' % erased)


class MemoryCommand(Command):
    """Defines the Memory command for memory access"""
    name = 'mem'
    description = 'Memory read access'
    help = 'memory read '

    def add_arguments(self, parser):
        """Adds the Memory command arguments to the parser.

        Args:
          self (FlashCommand): the ``FlashCommand`` instance
          parser (argparse.ArgumentParser): the parser to add the arguments to

        Returns:
          ``None``
        """
        parser.add_argument('-a', '--addr', type=str, help='memory address to read from in hex')
        parser.add_argument('-u', '--unit', type=int, default=8, choices=[8, 16, 32, 64], help='Memory unit')
        parser.add_argument('-n', '--num', type=int, default=1, help='number of unit to read')
        return self.add_common_arguments(parser, True)

    def run(self, args):
        """Read memory values

        Args:
          self (MemoryCommand): the ``MemoryCommand`` instance
          args (Namespace): the arguments passed on the command-line

        Returns:
          ``None``
        """
        address = int(args.addr, 16)
        kwargs = {'addr': address, 'num_units': args.num, 'zone': None, 'nbits': args.unit}
        jlink = self.create_jlink(args)
        result = jlink.memory_read(**kwargs)
        print(f'->  {[hex(n) for n in result]}')


class FlashCommand(Command):
    """Defines the flash command for flashing a device."""
    name = 'flash'
    description = 'Flashes firmware from a file to a device connected to a J-Link.'
    help = 'flash a device connected to the J-Link'

    def add_arguments(self, parser):
        """Adds the flash command arguments to the parser.

        Args:
          self (FlashCommand): the ``FlashCommand`` instance
          parser (argparse.ArgumentParser): the parser to add the arguments to

        Returns:
          ``None``
        """
        parser.add_argument('-a', '--addr', type=int, default=0,
                            help='start address to flash from')
        parser.add_argument('file', nargs=1, help='file to flash onto device')
        return self.add_common_arguments(parser, True)

    def run(self, args):
        """Flashes the device connected to the J-Link.

        Args:
          self (FlashCommand): the ``FlashCommand`` instance
          args (Namespace): the arguments passed on the command-line

        Returns:
          ``None``
        """
        kwargs = {'path': args.file[0], 'addr': args.addr, 'on_progress': Utils.flash_progress_callback}

        jlink = self.create_jlink(args)
        _ = jlink.flash_file(**kwargs)
        print('Flashed device successfully.')


class UnlockCommand(Command):
    """Command for unlocking a device."""
    name = 'unlock'
    description = (
        'Unlocks a device connected to a J-Link.  '
        'Note that this will erase the device.'
    )
    help = 'unlock a connected device'

    def add_arguments(self, parser):
        """Adds the unlock command arguments to the parser.

        Args:
          self (UnlockCommand): the ``UnlockCommand`` instance
          parser (argparse.ArgumentParser): the parser to add the arguments to

        Returns:
          ``None``
        """
        parser.add_argument('name', nargs=1, choices=['kinetis'],
                            help='name of MCU to unlock')
        return self.add_common_arguments(parser, True)

    def run(self, args):
        """Unlocks the target device.

        Args:
          self (UnlockCommand): the ``UnlockCommand`` instance
          args (Namespace): the arguments passed on the command-line

        Returns:
          ``None``
        """
        jlink = self.create_jlink(args)
        mcu = args.name[0].lower()
        if pyjlink.unlock(jlink, mcu):
            print('Successfully unlocked device!')
        else:
            print('Failed to unlock device!')


class LicenseCommand(Command):
    """Command for managing the J-Link's licenses."""
    name = 'license'
    description = 'Manage the licenses of the J-Link.'
    help = 'manage the licenses of your J-Link'

    def add_arguments(self, parser):
        """Adds the license command arguments to the parser.

        Args:
          self (LicenseCommand): the ``LicenseCommand`` instance
          parser (argparse.ArgumentParser): the parser to add the arguments to

        Returns:
          ``None``
        """
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-l', '--list', action='store_true',
                           help='list the licenses of the J-Link')
        group.add_argument('-a', '--add', dest='add',
                           help='add a custom license to the J-Link')
        group.add_argument('-e', '--erase', action='store_true',
                           help='erase the custom licenses on the J-Link')
        return self.add_common_arguments(parser, False)

    def run(self, args):
        """Runs the license command.

        Args:
          self (LicenseCommand): the ``LicenseCommand`` instance
          args (Namespace): the arguments passed on the command-line

        Returns:
          ``None``
        """
        jlink = self.create_jlink(args)
        if args.list:
            print('Built-in Licenses: %s' % ', '.join(jlink.licenses.split(',')))
            print('Custom Licenses: %s' % ', '.join(jlink.custom_licenses.split(',')))
        elif args.add is not None:
            if jlink.add_license(args.add):
                print('Successfully added license.')
            else:
                print('License already exists.')
        elif args.erase:
            if jlink.erase_licenses():
                print('Successfully erased all custom licenses.')
            else:
                print('Failed to erase custom licenses.')


class InfoCommand(Command):
    """Command for getting information about the hardware / DLL."""
    name = 'info'
    description = 'Get information about the J-Link.'
    help = 'get information about the J-Link'

    def add_arguments(self, parser):
        """Adds the information commands to the parser.

        Args:
          self (InfoCommand): the ``InfoCommand`` instance
          parser (argparse.ArgumentParser): the parser to add the arguments to

        Returns:
          ``None``
        """
        parser.add_argument('-p', '--product', action='store_true',
                            help='print the production information')
        parser.add_argument('-j', '--jtag', action='store_true',
                            help='print the JTAG pin status')
        return self.add_common_arguments(parser, False)

    def run(self, args):
        """Runs the information command.

        Args:
          self (InfoCommand): the ``InfoCommand`` instance
          args (Namespace): the arguments passed on the command-line

        Returns:
          ``None``
        """
        jlink = self.create_jlink(args)
        if args.product:
            print('Product: %s' % jlink.product_name)

            manufacturer = 'SEGGER' if jlink.oem is None else jlink.oem
            print('Manufacturer: %s' % manufacturer)

            print('Hardware Version: %s' % jlink.hardware_version)
            print('Firmware: %s' % jlink.firmware_version)
            print('DLL Version: %s' % jlink.version)
            print('Features: %s' % ', '.join(jlink.features))
        elif args.jtag:
            status = jlink.hardware_status
            print('TCK Pin Status: %d' % status.tck)
            print('TDI Pin Status: %d' % status.tdi)
            print('TDO Pin Status: %d' % status.tdo)
            print('TMS Pin Status: %d' % status.tms)
            print('TRES Pin Status: %d' % status.tres)
            print('TRST Pin Status: %d' % status.trst)


class EmulatorCommand(Command):
    """
    Command for querying about emulator support, or connected emulators.
    """
    name = 'emulator'
    description = 'Query for information about emulators or support.'
    help = 'query for information about emulators or support'

    def add_arguments(self, parser):
        """Adds the arguments for the emulator command.

        Args:
          self (EmulatorCommand): the ``EmulatorCommand`` instance
          parser (argparse.ArgumentParser): parser to add the commands to

        Returns:
          ``None``
        """
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-l', '--list', nargs='?',
                           type=str.lower, default='_',
                           choices=['usb', 'ip'],
                           help='list all the connected emulators')
        group.add_argument('-s', '--supported', nargs=1,
                           help='query whether a device is supported')
        group.add_argument('-t', '--test', action='store_true',
                           help='perform a self-test')
        return None

    def run(self, args):
        """
        Runs the emulator command.

        :param args: arguments to parse
        """
        jlink = pyjlink.JLink()

        if args.test:
            if jlink.test():
                print('Self-test succeeded.')
            else:
                print('Self-test failed.')
        elif args.list is None or args.list in ['usb', 'ip']:
            host = pyjlink.JLinkHost.USB_OR_IP
            if args.list == 'usb':
                host = pyjlink.JLinkHost.USB
            elif args.list == 'ip':
                host = pyjlink.JLinkHost.IP

            emulators = jlink.connected_emulators(host)
            for (index, emulator) in enumerate(emulators):
                if index > 0:
                    print('')

                print('Product Name: %s' % emulator.acProduct.decode())
                print('Serial Number: %s' % emulator.SerialNumber)

                usb = bool(emulator.Connection)
                if not usb:
                    print('Nickname: %s' % emulator.acNickname.decode())
                    print('Firmware: %s' % emulator.acFWString.decode())

                print('Connection: %s' % ('USB' if usb else 'IP'))

                if not usb:
                    print('IP Address: %s' % emulator.aIPAddr)
        elif args.supported is not None:
            device = args.supported[0]
            try:
                index = jlink.get_device_index(device)
            except pyjlink.errors.JLinkException:
                print('%s is not supported :(' % device)
                return None

            found_device = jlink.supported_device(index)

            print('Device Name: %s' % device)
            print('Core ID: %s' % found_device.CoreId)
            print('Flash Address: %s' % found_device.FlashAddr)
            print('Flash Size: %s bytes' % found_device.FlashSize)
            print('RAM Address: %s' % found_device.RAMAddr)
            print('RAM Size: %s bytes' % found_device.RAMSize)
            print('Manufacturer: %s' % found_device.manufacturer)

        return None


class FirmwareCommand(Command):
    """
    Command for upgrading and downgrading J-Link firmware.
    """
    name = 'firmware'
    description = 'Modify the J-Link firmware.'
    help = 'modify the J-Link firmware'

    def add_arguments(self, parser):
        """
        Adds the arguments for the firmware command.

        :param parser: parser to add the commands to
        """
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-d', '--downgrade', action='store_true',
                           help='downgrade the J-Link firmware')
        group.add_argument('-u', '--upgrade', action='store_true',
                           help='upgrade the J-Link firmware')
        return self.add_common_arguments(parser, False)

    def run(self, args):
        """
        Runs the firmware command.

        :param args: arguments to parse
        """
        jlink = self.create_jlink(args)
        if args.downgrade:
            if not jlink.firmware_newer():
                print('DLL firmware is not older than J-Link firmware.')
            else:
                jlink.invalidate_firmware()

                try:
                    # Change to the firmware of the connected DLL.
                    jlink.update_firmware()
                except pyjlink.JLinkException as e:
                    # On J-Link versions < 5.0.0, an exception will be thrown as
                    # the connection will be lost, so we have to re-establish.
                    jlink = self.create_jlink(args)

                print('Firmware Downgraded: %s' % jlink.firmware_version)
        elif args.upgrade:
            if not jlink.firmware_outdated():
                print('DLL firmware is not newer than J-Link firmware.')
            else:
                try:
                    # Upgrade the firmware.
                    jlink.update_firmware()
                except pyjlink.JLinkException as e:
                    # On J-Link versions < 5.0.0, an exception will be thrown as
                    # the connection will be lost, so we have to re-establish.
                    jlink = self.create_jlink(args)
                print('Firmware Updated: %s' % jlink.firmware_version)

        return None


def commands():
    """
    Returns the program commands.

    :return:
      A list of commands.
    """
    return map(lambda c: c(), CommandMeta.registry.values())


def create_parser():
    """Builds the command parser.

    This needs to be exported in order for Sphinx to document it correctly.

    :return:
      An instance of an ``argparse.ArgumentParser`` that parses all the commands supported by the PyLink CLI.
    """
    parser = argparse.ArgumentParser(prog=pyjlink.__title__,
                                     description=pyjlink.__description__,
                                     epilog=pyjlink.__copyright__)
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + pyjlink.__version__)
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='increase output verbosity')

    kwargs = {'title': 'command', 'description': 'specify subcommand to run', 'help': 'subcommands'}
    subparsers = parser.add_subparsers(**kwargs)

    for command in commands():
        kwargs = {'name': command.name, 'description': command.description, 'help': command.help}
        subparser = subparsers.add_parser(**kwargs)
        subparser.set_defaults(command=command.run)
        command.add_arguments(subparser)

    return parser


def main(args=None):
    """
    Main command-line interface entrypoint.

    Runs the given subcommand or argument that were specified.  If not given a ``args`` parameter, assumes the
    arguments are passed on the command-line.

    :param args: list of command-line arguments

    :return:
      Zero on success, non-zero otherwise.
    """
    if args is None:
        args = sys.argv[1:]

    parser = create_parser()
    args = parser.parse_args(args)

    if args.verbose >= 2:
        level = logging.DEBUG
    elif args.verbose >= 1:
        level = logging.INFO
    else:
        level = logging.WARNING

    logging.basicConfig(level=level)

    try:
        if hasattr(args, 'command'):
            args.command(args)
        else:
            parser.error('too few arguments')
    except pyjlink.JLinkException as e:
        sys.stderr.write('Error: %s%s' % (str(e), os.linesep))
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
