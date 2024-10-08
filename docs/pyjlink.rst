PyJLink
=======

The PyJLink package provides a Pythonic interface for interacting with the
J-Link C SDK.  This interface is provided through the ``JLink`` class, which
provides several of the functions provided by the native SDK.  Some methods
require a specific interface, a target being connected, or an emulator being
connected, and will raise errors as appropriate if these conditions are not
met.

In lieu of return codes, this library uses the object-oriented paradigm of
raising an exception.  All exceptions are inherited from the ``JLinkException``
base class.

Exceptions
----------

This submodule defines the different exceptions that can be generated by the
``JLink`` methods.

.. automodule:: pyjlink.errors
    :members:
    :undoc-members:
    :show-inheritance:


Library
-------

This submodule defines a ``Library``.  This is not needed unless explicitly
specifying a different version of the J-Link dynamic library.

.. automodule:: pyjlink.library
    :members:
    :undoc-members:
    :show-inheritance:

JLock
-----

This submodule defines a ``JLock``.  This acts as a lockfile-like interface for
interacting with a particular emulator in order to prevent multiple threads or
processes from creating instances of ``JLink`` to interact with the same
emulator.

.. automodule:: pyjlink.jlock
    :members:
    :undoc-members:
    :show-inheritance:

JLink
-----

This submodule provides the definition for the ``JLink`` class, which is the
interface to the J-Link.

.. automodule:: pyjlink.jlink
    :members:
    :undoc-members:
    :show-inheritance:
