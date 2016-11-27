%define name tellcore-py
%define version 1.1.3
%define unmangled_version 1.1.3
%define release 1

Summary: Python wrapper for Telldus' home automation library
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GPLv3+
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Erik Johansson <erik@ejohansson.se>
Url: https://github.com/erijo/tellcore-py

%description
Python wrapper for Telldus Core
===============================

.. image:: https://badge.fury.io/py/tellcore-py.png
    :target: https://pypi.python.org/pypi/tellcore-py/

.. image:: https://secure.travis-ci.org/erijo/tellcore-py.png?branch=master
    :target: http://travis-ci.org/erijo/tellcore-py

tellcore-py is a Python wrapper for `Telldus' <http://www.telldus.com/>`_ home
automation library `Telldus Core <http://developer.telldus.se/doxygen/>`_.

* Documentation: https://tellcore-py.readthedocs.org/
* Official home page: https://github.com/erijo/tellcore-py
* Python package index: https://pypi.python.org/pypi/tellcore-py

Please report any problem as a `GitHub issue report
<https://github.com/erijo/tellcore-py/issues/new>`_.

Features
--------

* Wraps the C-interface with a python interface (with classes and exceptions).
* Automatically frees memory for returned strings.
* Throws an exception (TelldusError) in case a library function returns an
  error.
* Supports python 3 with automatic handling of strings (i.e. converting between
  bytes used by the C-library and strings as used by python).
* Takes care of making callbacks from the library thread-safe.
* Unit tested.
* Besides being useful with the regular Python implementation (a.k.a. `CPython
  <http://en.wikipedia.org/wiki/CPython>`_), it also works with `pypy
  <http://pypy.org/>`_.
* Open source (`GPLv3+
  <https://github.com/erijo/tellcore-py/blob/master/LICENSE.txt>`_).
* Works on Linux, Mac OS X and Windows.

Requirements
------------

* Python 2.7, 3.2+ or pypy
* `Telldus Core library <http://telldus.com/products/nativesoftware>`_

Installation
------------

.. code-block:: bash

    $ pip install tellcore-py

Can also be installed by cloning the `GIP repository
<https://github.com/erijo/tellcore-py>`_ or downloading the `ZIP archive
<https://github.com/erijo/tellcore-py/archive/master.zip>`_ from GitHub and
unpacking it. Then change directory to tellcore-py and run:

.. code-block:: bash

    $ python setup.py install

Users
-----

* `Home Assistant <https://home-assistant.io>`_ - Open-source home automation
  platform running on Python 3
* `Tellprox <https://github.com/p3tecracknell/tellprox/>`_ - A local server to
  use in place of Telldus Live
* `tellive-py <https://github.com/erijo/tellive-py>`_ - A Python wrapper for
  Telldus Live

Example
-------

A simple example for adding a new "lamp" device, turning it on and then turning
all devices off.

.. code-block:: python

    from tellcore.telldus import TelldusCore

    core = TelldusCore()
    lamp = core.add_device("lamp", "arctech", "selflearning-switch", house=12345, unit=1)
    lamp.turn_on()

    for device in core.devices():
        device.turn_off()

More examples can be found in the `bin
<https://github.com/erijo/tellcore-py/tree/master/bin>`_ directory.

Internals
---------

At the bottom there is the Library class which is a `ctypes
<http://docs.python.org/library/ctypes.html>`_ wrapper and closely matches the
API of the underlying Telldus Core library. The library class takes care of
freeing memory returned from the base library and converts errors returned to
TelldusException. The library class is not intended to be used directly.

Instead, the TelldusCore class provides a more python-ish API on top of the
library class. This class is used for e.g. adding new devices, or enumerating
the existing devices, sensors and/or controllers. E.g. calling the devices()
method returns a list of Device instances. The Device class in turn has methods
for turning the device on, off, etc.


Changelog
=========

1.1.3 (2016-11-22)
------------------

* Added datetime attribute to ``SensorValue``.

* Fixed strange problem in ``Library`` where the class itself could
  sometimes be None in ``__del__``.


1.1.2 (2015-06-24)
------------------

* Added option to ``Library`` to make it possible to select if strings should
  be decoded or not.

* Made tellcore_tool not decode strings (i.e. convert to unicode) when running
  under Python 2.x to avoid unicode errors when printing non ascii characters.


1.1.1 (2015-05-01)
------------------

* Fixed a bug that made tellcore_tool not work with Python 3.x.


1.1.0 (2014-11-19)
------------------

* The callback dispatcher is no longer global, but tied to a ``Library``
  instance. Applications wishing to use callbacks must now pass an explicit
  dispatcher instance to the ``TelldusCore`` constructor.


1.0.4 (2014-11-05)
------------------

* Made ``last_sent_value`` return an int instead of string.


1.0.3 (2014-02-02)
------------------

* Work around crash in Telldus Core (< v2.1.2) when re-initalizing the library
  after ``tdClose``.


1.0.2 (2014-01-28)
------------------

* Packaging fixes.


1.0.1 (2014-01-26)
------------------

* Added ``AsyncioCallbackDispatcher`` class for integrating callbacks with the
  new event loop available in Python 3.4 (asyncio).

* Include tools from bin/ when installing.


1.0.0 (2014-01-09)
------------------

* Added high level support for device groups in the form of the new class
  ``DeviceGroup``.

* More complete documentation.

* Removed the methods process_callback and process_pending_callbacks from
  ``TelldusCore``. Instead, callback_dispatcher is now a public attribute of
  ``TelldusCore`` and the default callback dispatcher
  ``QueuedCallbackDispatcher`` implements the two methods instead.


0.9.0 (2014-01-03)
------------------

* Telldus functions that used to return bool (``tdSetName``, ``tdSetProtocol``,
  ``tdSetModel``, ``tdSetDeviceParameter`` and ``tdRemoveDevice``) now raise an
  exception instead of returning False.

* Support for rain- and windsensors.

* Include data type in ``SensorValue``.


0.8.0 (2013-08-11)
------------------

* Improved callback handling to simplify integration with different event
  loops. Parameter conversion is now done in the library code and the
  adaptation to different event loops is done by a simple callback dispatch
  class. The default dispatcher (when using ``TelldusCore``) is still done
  using a queue.

* New documentation for parts of the package. Can be read online at
  https://tellcore-py.readthedocs.org/.

* Fix problem with strings and python 3 (issue #2).


0.1.0 (2013-06-26)
------------------

* First release.


%prep
%setup -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
