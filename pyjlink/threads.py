# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Laurent Bonnet
#
# License: MIT

import threading


class ThreadReturn(threading.Thread):
    """
    Implementation of a thread with a return value.

    See also:
      `StackOverflow <http://stackoverflow.com/questions/6893968/>`__.
    """

    def __init__(self, daemon=False, *args, **kwargs):
        """
        Initializes the thread.

        :param daemon (bool): if the thread should be spawned as a daemon
        :param args: optional list of arguments
        :param kwargs: optional key-word arguments
        """
        super(ThreadReturn, self).__init__(*args, **kwargs)
        self.daemon = daemon
        self._return = None

    def run(self):
        """
        Runs the thread.
        """
        target = getattr(self, '_Thread__target', getattr(self, '_target', None))
        args = getattr(self, '_Thread__args', getattr(self, '_args', None))
        kwargs = getattr(self, '_Thread__kwargs', getattr(self, '_kwargs', None))
        if target is not None:
            self._return = target(*args, **kwargs)

        return None

    def join(self, *args, **kwargs):
        """
        Joins the thread.

        :param args: optional list of arguments
        :param kwargs: optional key-word arguments

        :return:
          The return value of the exited thread.
        """
        super(ThreadReturn, self).join(*args, **kwargs)
        return self._return
