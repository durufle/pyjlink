PyLink: Control your J-Link with Python
=======================================

PyLink is a Python package that enables you to control your J-Link from Python.
This library was developed at `Square <http://squareup.com>`_ to enable us to
leverage our J-Link as a part of our test infrastructure, which was written in
Python.

Getting started is as simple as:

.. code:: python

   >>> import pyjlink
   >>> jlink = pyjlink.JLink()
   >>> jlink.open(serial_no=123456789)
   >>> jlink.product_name
   J-Trace Cortex-M

.. toctree::
   :maxdepth: 1
   :caption: Getting Started

   Installation <installation.rst>
   Tutorial <tutorial.rst>
   Command-Line <cli.rst>

.. toctree::
   :maxdepth: 1
   :caption: Documentation

   PyJLink <pyjlink.rst>
   Protocols <pyjlink.protocols.rst>
   Unlockers <pyjlink.unlockers.rst>
   Bindings <pyjlink.bindings.rst>
   Extras <pyjlink.extras.rst>
   Troubleshooting <troubleshooting.rst>

.. toctree::
   :maxdepth: 1
   :caption: Debugging

   Serial Wire Debug <swd.rst>

.. toctree::
   :caption: About PyJLink
   :hidden:

   About <about.rst>
