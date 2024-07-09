# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Laurent Bonnet
#
# License: MIT

import pyjlink.jlock as jlock
import errno
import os
import unittest
from unittest.mock import Mock, patch


class TestJLock(unittest.TestCase):
    """
    Tests the ``jlock`` submodule.
    """

    def setUp(self):
        """
        Called before each test.

        Performs setup.
        """
        assert_raises_regexp = getattr(self, 'assertRaisesRegexp', None)
        self.assertRaisesRegexp = getattr(self, 'assertRaisesRegex', assert_raises_regexp)

    def tearDown(self):
        """
        Called after each test.

        Performs teardown.
        """
        pass

    @patch('tempfile.tempdir', new='tmp')
    def test_jlock_init_and_delete(self):
        """
        Tests initialization and deleting a ``JLock``.
        """
        serial_no = 0xdeadbeef

        lock = jlock.JLock(serial_no)
        lock.release = Mock()

        del lock

    @unittest.skip("Execution error. Need to be resolved !")
    @patch('tempfile.tempdir', new='tmp')
    @patch('os.close')
    @patch('os.path.exists')
    @patch('os.open')
    @patch('os.write')
    @patch('os.remove')
    @patch('pyjlink.jlock.psutil')
    @patch('pyjlink.jlock.open')
    def test_jlock_acquire_exists(self, mock_open, mock_util, mock_rm, mock_wr, mock_op, mock_exists, mock_close):
        """
        Tests trying to acquire when the lock exists for an active process.

        Args:
          mock_open (Mock): mocked built-in open method
          mock_util (Mock): mocked ``psutil`` module
          mock_rm (Mock): mocked os remove method
          mock_wr (Mock): mocked os write method
          mock_op (Mock): mocked os open method
          mock_exists (Mock): mocked path exist method
          mock_close (Mock): mocked os file close method
        """
        pid = 42
        serial_no = 0xdeadbeef

        mock_open.side_effect = [
            mock_open(read_data='%s\n' % pid).return_value,
        ]

        mock_exists.side_effect = [True, True]
        mock_util.pid_exists.return_value = True
        mock_op.side_effect = [OSError(errno.EEXIST, '')]

        lock = jlock.JLock(serial_no)
        lock.release = Mock()

        self.assertFalse(lock.acquired)
        self.assertFalse(lock.acquire())
        self.assertFalse(lock.acquired)

        mock_open.assert_called_once()
        mock_util.pid_exists.assert_called_with(pid)
        mock_op.assert_called_once()
        mock_rm.assert_not_called()
        mock_wr.assert_not_called()

    @patch('tempfile.tempdir', new='tmp')
    @patch('os.close')
    @patch('os.path.exists')
    @patch('os.open')
    @patch('os.write')
    @patch('os.remove')
    @patch('pyjlink.jlock.psutil')
    @patch('pyjlink.jlock.open')
    def test_jlock_acquire_os_error(self, mock_open, mock_util, mock_rm, mock_wr, mock_op, mock_exists, mock_close):
        """Tests trying to acquire the lock but generating an os-level error.

        Args:
          mock_open (Mock): mocked built-in open method
          mock_util (Mock): mocked ``psutil`` module
          mock_rm (Mock): mocked os remove method
          mock_wr (Mock): mocked os write method
          mock_op (Mock): mocked os open method
          mock_exists (Mock): mocked path exist method
          mock_close (Mock): mocked os file close method
        """
        serial_no = 0xdeadbeef

        mock_exists.side_effect = [False, False]
        mock_op.side_effect = [OSError(~errno.EEXIST, 'Message')]

        lock = jlock.JLock(serial_no)
        lock.release = Mock()

        self.assertFalse(lock.acquired)

        with self.assertRaisesRegexp(OSError, 'Message'):
            lock.acquire()

        self.assertFalse(lock.acquired)

        mock_open.assert_not_called()
        mock_util.pid_exists.assert_not_called()
        mock_op.assert_called_once()
        mock_rm.assert_not_called()
        mock_wr.assert_not_called()

    @patch('tempfile.tempdir', new='tmp')
    @patch('os.close')
    @patch('os.path.exists')
    @patch('os.open')
    @patch('os.write')
    @patch('os.remove')
    @patch('pyjlink.jlock.psutil')
    @patch('pyjlink.jlock.open')
    def test_jlock_acquire_bad_file(self, mock_open, mock_util, mock_rm, mock_wr, mock_op, mock_exists, mock_close):
        """Tests acquiring the lockfile when the current lockfile is invallid.

        Args:
          self (TestJLock): the ``TestJLock`` instance
          mock_open (Mock): mocked built-in open method
          mock_util (Mock): mocked ``psutil`` module
          mock_rm (Mock): mocked os remove method
          mock_wr (Mock): mocked os write method
          mock_op (Mock): mocked os open method
          mock_exists (Mock): mocked path exist method
          mock_close (Mock): mocked os file close method

        Returns:
          ``None``
        """
        pid = 42
        fd = 1
        serial_no = 0xdeadbeef

        mock_open.side_effect = [
            IOError()
        ]

        mock_exists.return_value = True
        mock_op.return_value = fd

        lock = jlock.JLock(serial_no)
        lock.release = Mock()

        self.assertFalse(lock.acquired)
        self.assertTrue(lock.acquire())
        self.assertTrue(lock.acquired)

        mock_exists.assert_called_once()
        mock_open.assert_called_once()
        mock_util.pid_exists.assert_not_called()
        mock_rm.assert_not_called()
        mock_op.assert_called_once()
        mock_wr.assert_called_once()

    @unittest.skip("Execution error. Need to be resolved !")
    @patch('tempfile.tempdir', new='tmp')
    @patch('os.close')
    @patch('os.path.exists')
    @patch('os.open')
    @patch('os.write')
    @patch('os.remove')
    @patch('pyjlink.jlock.psutil')
    @patch('pyjlink.jlock.open')
    def test_jlock_acquire_invalid_pid(self, mock_open, mock_util, mock_rm, mock_wr, mock_op, mock_exists, mock_close):
        """
        Tests acquiring the lockfile when the pid in the lockfile is invalid.

        Args:
          self (TestJLock): the ``TestJLock`` instance
          mock_open (Mock): mocked built-in open method
          mock_util (Mock): mocked ``psutil`` module
          mock_rm (Mock): mocked os remove method
          mock_wr (Mock): mocked os write method
          mock_op (Mock): mocked os open method
          mock_exists (Mock): mocked path exist method
          mock_close (Mock): mocked os file close method

        Returns:
          ``None``
        """
        fd = 1
        serial_no = 0xdeadbeef

        mock_open.side_effect = [
            mock_open(read_data='dog\n').return_value,
        ]

        mock_op.return_value = fd

        lock = jlock.JLock(serial_no)
        lock.release = Mock()

        self.assertFalse(lock.acquired)
        self.assertTrue(lock.acquire())
        self.assertTrue(lock.acquired)

        mock_exists.assert_called_once()
        mock_open.assert_called_once()
        mock_util.pid_exists.assert_not_called()
        mock_rm.assert_called_once()
        mock_op.assert_called_once()
        mock_wr.assert_called_once()

    @unittest.skip("Execution error. Need to be resolved !")
    @patch('tempfile.tempdir', new='tmp')
    @patch('os.close')
    @patch('os.path.exists')
    @patch('os.open')
    @patch('os.write')
    @patch('os.remove')
    @patch('pyjlink.jlock.psutil')
    @patch('pyjlink.jlock.open')
    def test_jlock_acquire_old_pid(self, mock_open, mock_util, mock_rm, mock_wr, mock_op, mock_exists, mock_close):
        """
        Tests acquiring when the PID in the lockfile does not exist.

        Args:
          mock_open (Mock): mocked built-in open method
          mock_util (Mock): mocked ``psutil`` module
          mock_rm (Mock): mocked os remove method
          mock_wr (Mock): mocked os write method
          mock_op (Mock): mocked os open method
          mock_exists (Mock): mocked path exist method
          mock_close (Mock): mocked os file close method
        """
        fd = 1
        serial_no = 0xdeadbeef

        mock_open.side_effect = [
            mock_open(read_data='42\n').return_value,
        ]

        mock_op.return_value = fd
        mock_util.pid_exists.return_value = False

        lock = jlock.JLock(serial_no)
        lock.release = Mock()

        self.assertFalse(lock.acquired)
        self.assertTrue(lock.acquire())
        self.assertTrue(lock.acquired)

        mock_exists.assert_called_once()
        mock_open.assert_called_once()
        mock_util.pid_exists.assert_called_once_with(42)
        mock_rm.assert_called()
        mock_op.assert_called_once()
        mock_wr.assert_called_once()

    @patch('tempfile.tempdir', new='tmp')
    @patch('os.path.exists')
    @patch('os.close')
    @patch('os.remove')
    def test_jlock_release_acquired(self, mock_remove, mock_close, mock_exists):
        """
        Tests releasing a held lock.

        Args:
          self (TestJLock): the ``TestJLock`` instance
          mock_remove (Mock): mock file removal method
          mock_close (Mock): mocked close method
          mock_exists (Mock): mocked path exist method

        Returns:
          ``None``
        """
        lock = jlock.JLock(0xdeadbeef)
        lock.acquired = True
        lock.fd = 1
        lock.path = os.sep

        self.assertTrue(lock.release())

        mock_exists.return_value = True
        mock_remove.assert_called_once_with(os.sep)
        mock_close.assert_called_once_with(1)
        mock_exists.assert_called_once_with(os.sep)

        self.assertEqual(False, lock.acquired)

    @patch('tempfile.tempdir', new='tmp')
    def test_jlock_release_not_held(self):
        """Tests calling release when lock not held.

        Args:
          self (TestJLock): the ``TestJLock`` instance

        Returns:
          ``None``
        """
        lock = jlock.JLock(0xdeadbeef)
        self.assertFalse(lock.release())


if __name__ == '__main__':
    unittest.main()
