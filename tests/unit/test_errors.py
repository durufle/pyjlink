# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Laurent Bonnet
#
# License: MIT


import pyjlink.errors as errors

import unittest


class TestErrors(unittest.TestCase):
    """Unit test for the `errors` submodule."""

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

    def test_jlink_exception_with_message(self):
        """
        Tests that a `JLinkException` can be created with a message.
        """
        message = 'message'
        exception = errors.JLinkException(message)
        self.assertTrue(isinstance(exception.message, str))
        self.assertEqual(message, exception.message)
        self.assertEqual(None, getattr(exception, 'code', None))

    def test_jlink_exception_with_code(self):
        """
        Tests that a `JLinkException` can be created with a numeric code.
        """
        code = -1
        exception = errors.JLinkException(code)
        self.assertTrue(isinstance(exception.message, str))
        self.assertEqual('Unspecified error.', exception.message)
        self.assertEqual(code, getattr(exception, 'code', None))


if __name__ == '__main__':
    unittest.main()
