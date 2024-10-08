# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Laurent Bonnet
#
# License: MIT

import pyjlink
import pyjlink.__main__ as main
import logging

try:
    import StringIO
except ImportError:
    import io as StringIO
import ctypes
import sys
import unittest
from unittest.mock import Mock, patch


class TestMain(unittest.TestCase):
    """Tests the command-line interface."""

    def setUp(self):
        """
        Called before each test.

        Performs setup.
        """
        pass

    def tearDown(self):
        """
        Called after each test.

        Performs teardown.
        """
        pass

    @patch('sys.stderr', new_callable=StringIO.StringIO)
    @patch('sys.stdout', new_callable=StringIO.StringIO)
    @patch('pyjlink.__main__.pyjlink.JLink')
    def test_help(self, mock_jlink, mock_stdout, mock_stderr):
        """
        Tests printing out the command-line help.

        Args:
          self (TestMain): the ``TestMain`` instance
          mock_jlink (mock.Mock): the mocked ``JLink`` object
          mock_stdout (mock.Mock): mocked standard output stream
          mock_stderr (mock.Mock): mocked standard error stream

        Returns:
          ``None``
        """
        with self.assertRaises(SystemExit):
            main.main(['--help'])

        self.assertTrue('usage: pyjlink' in mock_stdout.getvalue())

    @patch('sys.argv', ['pyjlink', '--help'])
    @patch('sys.stderr', new_callable=StringIO.StringIO)
    @patch('sys.stdout', new_callable=StringIO.StringIO)
    @patch('pyjlink.__main__.pyjlink.JLink')
    def test_help_argv(self, mock_jlink, mock_stdout, mock_stderr):
        """
        Tests printing out the command-line help when called without args.

        Args:
          self (TestMain): the ``TestMain`` instance
          mock_jlink (mock.Mock): the mocked ``JLink`` object
          mock_stdout (mock.Mock): mocked standard output stream
          mock_stderr (mock.Mock): mocked standard error stream

        Returns:
          ``None``
        """
        with self.assertRaises(SystemExit):
            main.main()

        self.assertTrue('usage: pyjlink' in mock_stdout.getvalue())

    @patch('sys.stderr', new_callable=StringIO.StringIO)
    @patch('sys.stdout', new_callable=StringIO.StringIO)
    @patch('pyjlink.__main__.pyjlink.JLink')
    def test_version_command(self, mock_jlink, mock_stdout, mock_stderr):
        """
        Tests printing the version of the module.

        Args:
          mock_jlink (mock.Mock): the mocked ``JLink`` object
          mock_stdout (mock.Mock): mocked standard output stream
          mock_stderr (mock.Mock): mocked standard error stream
        """
        with self.assertRaises(SystemExit):
            main.main(['--version'])

        expected = 'pyjlink %s' % pyjlink.__version__
        if sys.version_info >= (3, 0):
            self.assertEqual(expected, mock_stdout.getvalue().strip())
        else:
            self.assertEqual(expected, mock_stderr.getvalue().strip())

    @patch('pyjlink.__main__.logging.basicConfig')
    @patch('sys.stderr', new_callable=StringIO.StringIO)
    @patch('sys.stdout', new_callable=StringIO.StringIO)
    @patch('pyjlink.__main__.pyjlink.JLink')
    def test_verbosity(self, mock_jlink, mock_stdout, mock_stderr, mock_config):
        """
        Tests setting the verbosity of the command-line tool.

        Args:
          mock_jlink (mock.Mock): the mocked ``JLink`` object
          mock_stdout (mock.Mock): mocked standard output stream
          mock_stderr (mock.Mock): mocked standard error stream
          mock_config (mock.Mock): mocked logging configuration function
        """
        args = ['emulator', '--test']

        # No levels of verbosity.
        self.assertEqual(0, main.main(args))
        mock_config.assert_called_with(level=logging.WARNING)

        # One level of verbosity.
        self.assertEqual(0, main.main(['-v'] + args))
        mock_config.assert_called_with(level=logging.INFO)

        # Two levels of verbosity.
        self.assertEqual(0, main.main(['-v', '-v'] + args))
        mock_config.assert_called_with(level=logging.DEBUG)

        # Three levels of verbosity.
        self.assertEqual(0, main.main(['-v', '-v', '-v'] + args))
        mock_config.assert_called_with(level=logging.DEBUG)

    @patch('sys.stderr', new_callable=StringIO.StringIO)
    @patch('sys.stdout', new_callable=StringIO.StringIO)
    @patch('pyjlink.__main__.pyjlink.JLink')
    def test_new_command_fail_validation(self, mock_jlink, mock_stdout, mock_stderr):
        """
        Tests creating a new command that fails validation.

        Args:
          mock_jlink (mock.Mock): the mocked ``JLink`` object
          mock_stdout (mock.Mock): mocked standard output stream
          mock_stderr (mock.Mock): mocked standard error stream
        """
        with self.assertRaises(ValueError):
            class a(main.Command):
                description = 'description'
                help = 'help'

        with self.assertRaises(ValueError):
            class a(main.Command):
                name = 'name'
                help = 'help'

        with self.assertRaises(ValueError):
            class a(main.Command):
                name = 'name'
                description = 'description'

    @patch('sys.stderr', new_callable=StringIO.StringIO)
    @patch('sys.stdout', new_callable=StringIO.StringIO)
    @patch('pyjlink.__main__.pyjlink.JLink')
    def test_new_command_method_not_implemented(self, mock_jlink, mock_stdout, mock_stderr):
        """
        Tests when a command is created, errors if method not implemented.

        Args:
          mock_jlink (mock.Mock): the mocked ``JLink`` object
          mock_stdout (mock.Mock): mocked standard output stream
          mock_stderr (mock.Mock): mocked standard error stream
        """

        class A(main.Command):
            name = 'name'
            description = 'description'
            help = 'help'

        with self.assertRaises(NotImplementedError):
            a = A()
            a.add_arguments(None)

        with self.assertRaises(NotImplementedError):
            a = A()
            a.run(None)

        main.CommandMeta.registry.pop('A')

    @patch('sys.stderr', new_callable=StringIO.StringIO)
    @patch('sys.stdout', new_callable=StringIO.StringIO)
    @patch('pyjlink.__main__.pyjlink.JLink')
    def test_main_jlink_exception(self, mock_jlink, mock_stdout, mock_stderr):
        """
        Tests when a J-Link exception is raised when a command is run.

        Args:
          mock_jlink (mock.Mock): the mocked ``JLink`` object
          mock_stdout (mock.Mock): mocked standard output stream
          mock_stderr (mock.Mock): mocked standard error stream
        """
        args = ['emulator', '--test']
        mock_jlink.side_effect = pyjlink.JLinkException('error')
        self.assertEqual(1, main.main(args))
        self.assertEqual('Error: error', mock_stderr.getvalue().strip())

    @patch('sys.stderr', new_callable=StringIO.StringIO)
    @patch('sys.stdout', new_callable=StringIO.StringIO)
    @patch('pyjlink.__main__.pyjlink.JLink')
    def test_emulator_test_command(self, mock_jlink, mock_stdout, mock_stderr):
        """
        Tests the emulator self-test command.

        Args:
          mock_jlink (mock.Mock): the mocked ``JLink`` object
          mock_stdout (mock.Mock): mocked standard output stream
          mock_stderr (mock.Mock): mocked standard error stream
        """
        args = ['emulator', '--test']

        mocked = Mock()
        mock_jlink.return_value = mocked

        mocked.test.return_value = True
        self.assertEqual(0, main.main(args))
        self.assertEqual('Self-test succeeded.', mock_stdout.getvalue().strip())

        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        mocked.test.return_value = False
        self.assertEqual(0, main.main(args))
        self.assertEqual('Self-test failed.', mock_stdout.getvalue().strip())

    @patch('sys.stderr', new_callable=StringIO.StringIO)
    @patch('sys.stdout', new_callable=StringIO.StringIO)
    @patch('pyjlink.__main__.pyjlink.JLink')
    def test_emulator_list_command(self, mock_jlink, mock_stdout, mock_stderr):
        """
        Tests the emulator list device command.

        Args:
          mock_jlink (mock.Mock): the mocked ``JLink`` object
          mock_stdout (mock.Mock): mocked standard output stream
          mock_stderr (mock.Mock): mocked standard error stream
        """
        usb_device = pyjlink.JLinkConnectInfo()
        usb_device.SerialNumber = 123456789
        usb_device.acProduct = b'J-Trace CM'
        usb_device.Connection = 1

        ip_device = pyjlink.JLinkConnectInfo()
        ip_device.SerialNumber = 987654321
        ip_device.acProduct = b'J-Link PRO'
        ip_device.Nickname = b'J-Link PRO'
        ip_device.acFWString = b'J-Link PRO compiled Mon. Nov. 7th 13:56:44'
        ip_device.Connection = 0

        mocked = Mock()
        mock_jlink.return_value = mocked

        args = ['emulator', '--list']
        mocked.connected_emulators.return_value = [usb_device, ip_device]
        self.assertEqual(0, main.main(args))
        mocked.connected_emulators.assert_called_with(pyjlink.JLinkHost.USB_OR_IP)
        self.assertTrue('Product Name: J-Trace CM' in mock_stdout.getvalue())
        self.assertTrue('Product Name: J-Link PRO' in mock_stdout.getvalue())

        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        args = ['emulator', '--list', 'usb']
        mocked.connected_emulators.return_value = [usb_device]
        self.assertEqual(0, main.main(args))
        mocked.connected_emulators.assert_called_with(pyjlink.JLinkHost.USB)
        self.assertTrue('Product Name: J-Trace CM' in mock_stdout.getvalue())
        self.assertTrue('Connection: USB' in mock_stdout.getvalue())
        self.assertFalse('Product Name: J-Link PRO' in mock_stdout.getvalue())

        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        args = ['emulator', '--list', 'ip']
        mocked.connected_emulators.return_value = [ip_device]
        self.assertEqual(0, main.main(args))
        mocked.connected_emulators.assert_called_with(pyjlink.JLinkHost.IP)
        self.assertFalse('Product Name: J-Trace CM' in mock_stdout.getvalue())
        self.assertTrue('Connection: IP' in mock_stdout.getvalue())
        self.assertTrue('Product Name: J-Link PRO' in mock_stdout.getvalue())

    @patch('sys.stderr', new_callable=StringIO.StringIO)
    @patch('sys.stdout', new_callable=StringIO.StringIO)
    @patch('pyjlink.__main__.pyjlink.JLink')
    def test_emulator_supported_command(self, mock_jlink, mock_stdout, mock_stderr):
        """
        Tests querying whether a device is supported.

        Args:
          mock_jlink (mock.Mock): the mocked ``JLink`` object
          mock_stdout (mock.Mock): mocked standard output stream
          mock_stderr (mock.Mock): mocked standard error stream
        """
        mocked = Mock()
        mock_jlink.return_value = mocked

        name = (ctypes.c_char * 10)(*b'CANADA')
        device = pyjlink.JLinkDeviceInfo()
        device.sName = name

        mocked.get_device_index.side_effect = pyjlink.errors.JLinkException('Unsupported device selected.')

        args = ['emulator', '-s', 'USA']
        self.assertEqual(0, main.main(args))
        self.assertEqual('USA is not supported :(', mock_stdout.getvalue().strip())

        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        mocked.get_device_index.side_effect = None
        mocked.get_device_index.return_value = 1
        mocked.supported_device.return_value = device

        args = ['emulator', '-s', 'CANADA']
        self.assertEqual(0, main.main(args))
        self.assertTrue('Device Name: CANADA' in mock_stdout.getvalue())

    @patch('sys.stderr', new_callable=StringIO.StringIO)
    @patch('sys.stdout', new_callable=StringIO.StringIO)
    @patch('pyjlink.__main__.pyjlink.JLink')
    def test_info_product_command(self, mock_jlink, mock_stdout, mock_stderr):
        """
        Tests the product information command.

        Args:
          self (TestMain): the ``TestMain`` instance
          mock_jlink (mock.Mock): the mocked ``JLink`` object
          mock_stdout (mock.Mock): mocked standard output stream
          mock_stderr (mock.Mock): mocked standard error stream

        Returns:
          ``None``
        """
        mocked = Mock()
        mock_jlink.return_value = mocked

        mocked.features = ['RDI', 'FlashBP']

        args = ['info', '--product', '--serial', '123456789']
        self.assertEqual(0, main.main(args))

        self.assertTrue('Product' in mock_stdout.getvalue())
        self.assertTrue('Features: RDI, FlashBP' in mock_stdout.getvalue())

    @patch('sys.stderr', new_callable=StringIO.StringIO)
    @patch('sys.stdout', new_callable=StringIO.StringIO)
    @patch('pyjlink.__main__.pyjlink.JLink')
    def test_info_pin_command(self, mock_jlink, mock_stdout, mock_stderr):
        """Tests the JTAG pin status information command.

        Args:
          self (TestMain): the ``TestMain`` instance
          mock_jlink (mock.Mock): the mocked ``JLink`` object
          mock_stdout (mock.Mock): mocked standard output stream
          mock_stderr (mock.Mock): mocked standard error stream

        Returns:
          ``None``
        """
        mocked = Mock()
        mock_jlink.return_value = mocked

        status = pyjlink.JLinkHardwareStatus()
        status.VTarget = 80
        status.tck = 0
        status.tdi = 0
        status.tdo = 0
        status.tms = 1
        status.tres = 0
        status.trst = 1

        mocked.hardware_status = status

        args = ['info', '--jtag', '--serial', '123456789']
        self.assertEqual(0, main.main(args))

        self.assertTrue('TCK Pin Status: 0' in mock_stdout.getvalue())
        self.assertTrue('TRST Pin Status: 1' in mock_stdout.getvalue())

    @patch('sys.stderr', new_callable=StringIO.StringIO)
    @patch('sys.stdout', new_callable=StringIO.StringIO)
    @patch('pyjlink.__main__.pyjlink.JLink')
    def test_firmware_upgrade_command(self, mock_jlink, mock_stdout, mock_stderr):
        """
        Tests the command t- upgrade the J-Link firmware.

        Args:
          mock_jlink (mock.Mock): the mocked ``JLink`` object
          mock_stdout (mock.Mock): mocked standard output stream
          mock_stderr (mock.Mock): mocked standard error stream
        """
        mocked = Mock()
        mock_jlink.return_value = mocked

        args = ['firmware', '--upgrade', '--serial', '504502376']

        # Firmware is already new, can't upgrade anymore.
        mocked.firmware_outdated.return_value = False
        self.assertEqual(0, main.main(args))
        self.assertTrue('DLL firmware is not newer' in mock_stdout.getvalue())
        self.assertEqual(0, mocked.update_firmware.call_count)

        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        # Firmware is older, so we can upgrade.
        mocked.firmware_outdated.return_value = True
        mocked.update_firmware.side_effect = pyjlink.JLinkException('message')
        self.assertEqual(0, main.main(args))
        mocked.update_firmware.assert_called_once()
        self.assertTrue('Firmware Updated' in mock_stdout.getvalue())

    @patch('sys.stderr', new_callable=StringIO.StringIO)
    @patch('sys.stdout', new_callable=StringIO.StringIO)
    @patch('pyjlink.__main__.pyjlink.JLink')
    def test_firmware_downgrade_command(self, mock_jlink, mock_stdout, mock_stderr):
        """
        Tests the command to downgrade the J-Link firmware.

        Args:
          mock_jlink (mock.Mock): the mocked ``JLink`` object
          mock_stdout (mock.Mock): mocked standard output stream
          mock_stderr (mock.Mock): mocked standard error stream

        """
        mocked = Mock()
        mock_jlink.return_value = mocked

        args = ['firmware', '--downgrade', '--serial', '123456789']

        # Firmware is older than the DLL firmware.
        mocked.firmware_newer.return_value = False
        self.assertEqual(0, main.main(args))
        self.assertTrue('DLL firmware is not older' in mock_stdout.getvalue())
        self.assertEqual(0, mocked.update_firmware.call_count)

        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        # Firmware is newer, so we can downgrade.
        mocked.firmware_newer.return_value = True
        mocked.update_firmware.side_effect = pyjlink.JLinkException('message')
        self.assertEqual(0, main.main(args))
        mocked.invalidate_firmware.assert_called_once()
        mocked.update_firmware.assert_called_once()
        self.assertTrue('Firmware Downgraded' in mock_stdout.getvalue())

    @patch('sys.stderr', new_callable=StringIO.StringIO)
    @patch('sys.stdout', new_callable=StringIO.StringIO)
    @patch('pyjlink.__main__.pyjlink.JLink')
    def test_flash_command(self, mock_jlink, mock_stdout, mock_stderr):
        """
        Tests running the flash command over JTAG and SWD.

        Args:
          self (TestMain): the ``TestMain`` instance
          mock_jlink (mock.Mock): the mocked ``JLink`` object
          mock_stdout (mock.Mock): mocked standard output stream
          mock_stderr (mock.Mock): mocked standard error stream

        Returns:
          ``None``
        """
        mocked = Mock()
        mock_jlink.return_value = mocked

        args = ['flash', '-t', 'swd', '-d', 'DEVICE', '-s', '123456789', 'fileA']
        self.assertEqual(0, main.main(args))
        mocked.flash_file.assert_called_with(addr=0,
                                             on_progress=pyjlink.utils.Utils.flash_progress_callback,
                                             path='fileA')

        args = ['flash', '-t', 'jtag', '-d', 'DEVICE', '-s', '123456789', 'fileB']
        self.assertEqual(0, main.main(args))
        mocked.flash_file.assert_called_with(addr=0,
                                             on_progress=pyjlink.utils.Utils.flash_progress_callback,
                                             path='fileB')

    @patch('pyjlink.unlock')
    @patch('sys.stderr', new_callable=StringIO.StringIO)
    @patch('sys.stdout', new_callable=StringIO.StringIO)
    @patch('pyjlink.__main__.pyjlink.JLink')
    def test_unlock_command(self, mock_jlink, mock_stdout, mock_stderr, mock_unlock):
        """Tests the command for unlocking a locked device.

        Args:
          self (TestMain): the ``TestMain`` instance
          mock_jlink (mock.Mock): the mocked ``JLink`` object
          mock_stdout (mock.Mock): mocked standard output stream
          mock_stderr (mock.Mock): mocked standard error stream
          mock_unlock (mock.Mock): mocked unlock device call

        Returns:
          ``None``
        """
        mocked = Mock()
        mock_jlink.return_value = mocked

        args = ['unlock', '-t', 'swd', '-d', 'DEVICE', '-s', '123456789', 'kinetis']

        mock_unlock.return_value = True
        self.assertEqual(0, main.main(args))
        self.assertEqual('Successfully unlocked device!', mock_stdout.getvalue().strip())

        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        mock_unlock.return_value = False
        self.assertEqual(0, main.main(args))
        self.assertEqual('Failed to unlock device!', mock_stdout.getvalue().strip())

    @patch('sys.stderr', new_callable=StringIO.StringIO)
    @patch('sys.stdout', new_callable=StringIO.StringIO)
    @patch('pyjlink.__main__.pyjlink.JLink')
    def test_erase_command(self, mock_jlink, mock_stdout, mock_stderr):
        """Tests the command for erasing the device.

        Args:
          self (TestMain): the ``TestMain`` instance
          mock_jlink (mock.Mock): the mocked ``JLink`` object
          mock_stdout (mock.Mock): mocked standard output stream
          mock_stderr (mock.Mock): mocked standard error stream

        Returns:
          ``None``
        """
        mocked = Mock()
        mock_jlink.return_value = mocked
        mocked.erase.return_value = 1337

        args = ['erase', '-t', 'swd', '-d', 'DEVICE', '-s', '123456789']

        self.assertEqual(0, main.main(args))
        self.assertEqual('Bytes Erased: 1337', mock_stdout.getvalue().strip())

    @patch('sys.stderr', new_callable=StringIO.StringIO)
    @patch('sys.stdout', new_callable=StringIO.StringIO)
    @patch('pyjlink.__main__.pyjlink.JLink')
    def test_license_list_command(self, mock_jlink, mock_stdout, mock_stderr):
        """Tests the command for listing emulator licenses.

        Args:
          mock_jlink (mock.Mock): the mocked ``JLink`` object
          mock_stdout (mock.Mock): mocked standard output stream
          mock_stderr (mock.Mock): mocked standard error stream
        """
        mocked = Mock()
        mock_jlink.return_value = mocked

        mocked.licenses = 'FlashBP,RDI'
        mocked.custom_licenses = 'GDB'

        args = ['license', '-l', '-s', '123456789']
        self.assertEqual(0, main.main(args))
        self.assertTrue('Built-in Licenses: FlashBP, RDI' in mock_stdout.getvalue())
        self.assertTrue('Custom Licenses: GDB' in mock_stdout.getvalue())

    @patch('sys.stderr', new_callable=StringIO.StringIO)
    @patch('sys.stdout', new_callable=StringIO.StringIO)
    @patch('pyjlink.__main__.pyjlink.JLink')
    def test_license_add_command(self, mock_jlink, mock_stdout, mock_stderr):
        """Tests the command for adding emulator licenses.

        Args:
          self (TestMain): the ``TestMain`` instance
          mock_jlink (mock.Mock): the mocked ``JLink`` object
          mock_stdout (mock.Mock): mocked standard output stream
          mock_stderr (mock.Mock): mocked standard error stream

        Returns:
          ``None``
        """
        mocked = Mock()
        mock_jlink.return_value = mocked

        args = ['license', '-a', 'GDB', '-s', '123456789']

        mocked.add_license.return_value = True
        self.assertEqual(0, main.main(args))
        self.assertEqual('Successfully added license.', mock_stdout.getvalue().strip())

        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        mocked.add_license.return_value = False
        self.assertEqual(0, main.main(args))
        self.assertEqual('License already exists.', mock_stdout.getvalue().strip())

    @patch('sys.stderr', new_callable=StringIO.StringIO)
    @patch('sys.stdout', new_callable=StringIO.StringIO)
    @patch('pyjlink.__main__.pyjlink.JLink')
    def test_license_erase_command(self, mock_jlink, mock_stdout, mock_stderr):
        """Tests the command for erasing licenses.

        Args:
          self (TestMain): the ``TestMain`` instance
          mock_jlink (mock.Mock): the mocked ``JLink`` object
          mock_stdout (mock.Mock): mocked standard output stream
          mock_stderr (mock.Mock): mocked standard error stream

        Returns:
          ``None``
        """
        mocked = Mock()
        mock_jlink.return_value = mocked

        args = ['license', '-e', '-s', '123456789']

        mocked.erase_licenses.return_value = True
        self.assertEqual(0, main.main(args))
        self.assertEqual('Successfully erased all custom licenses.', mock_stdout.getvalue().strip())

        mock_stdout.truncate(0)
        mock_stdout.seek(0)

        mocked.erase_licenses.return_value = False
        self.assertEqual(0, main.main(args))
        self.assertEqual('Failed to erase custom licenses.', mock_stdout.getvalue().strip())


if __name__ == '__main__':
    unittest.main()
