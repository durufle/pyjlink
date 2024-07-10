# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Laurent Bonnet
#
# License: MIT
import functools
from . import threads


def async_decorator(func):
    """
    Asynchronous function decorator.  Interprets the function as being asynchronous, so returns a function that will
    handle calling the Function asynchronously.

    :param func: function to be called asynchronously

    :return: The wrapped function.

    :raise:
      AttributeError: if ``func`` is not callable
    """

    @functools.wraps(func)
    def async_wrapper(*args, **kwargs):
        """
        Wraps up the call to ``func``, so that it is called from a separate thread.

        The callback, if given, will be called with two parameters, ``exception`` and ``result`` as
        ``callback(exception, result)``.  If

        the thread ran to completion without error, ``exception`` will be ``None``, otherwise ``exception``
        will be the generated exception that stopped the thread.  Result is the result of the expected function.

        :param args: list of arguments to pass to ``func``
        :param kwargs: key-word arguments dictionary to pass to ``func``

        :return:
          A thread if the call is asynchronous, otherwise the the return value
          of the wrapped function.

        :raise:
          TypeError: if ``callback`` is not callable or is missing
        """
        if 'callback' not in kwargs or not kwargs['callback']:
            return func(*args, **kwargs)

        callback = kwargs.pop('callback')

        if not callable(callback):
            raise TypeError('Expected \'callback\' is not callable.')

        def thread_func(*args, **kwargs):
            """
            Thread function on which the given ``func`` and ``callback`` are executed.

            :param args: list of arguments to pass to ``func``
            :param kwargs: key-word arguments dictionary to pass to ``func``

            :return:
              Return value of the wrapped function.
            """
            exception, res = None, None
            try:
                res = func(*args, **kwargs)
            except Exception as e:
                exception = e
            return callback(exception, res)

        thread = threads.ThreadReturn(target=thread_func, args=args, kwargs=kwargs)

        thread.daemon = True
        thread.start()
        return thread

    return async_wrapper
