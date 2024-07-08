# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Laurent Bonnet
#
# License: MIT

import pyjlink.threads as threads

import unittest


class TestThreads(unittest.TestCase):
    """Unit test for the `threads` submodule."""

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

    def test_thread(self):
        """
        Tests that a thread can be created and joined for a return value.
        """
        def thread_func():
            return 4

        def thread_func_with_args(x, y):
            return (x + y)

        thread = threads.ThreadReturn(target=thread_func)
        thread.start()
        self.assertEqual(4, thread.join())

        thread = threads.ThreadReturn(target=thread_func_with_args, args=(2, 3))
        thread.start()
        self.assertEqual(5, thread.join())


if __name__ == '__main__':
    unittest.main()
