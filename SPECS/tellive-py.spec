%define name tellive-py
%define version 0.5.2
%define unmangled_version 0.5.2
%define release 1

Summary: Python wrapper for connecting to Telldus Live
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
Url: https://github.com/erijo/tellive-py

%description
Python wrapper for Telldus Live
===============================

.. image:: https://badge.fury.io/py/tellive-py.png
    :target: https://pypi.python.org/pypi/tellive-py/

.. image:: https://secure.travis-ci.org/erijo/tellive-py.png?branch=master
    :target: http://travis-ci.org/erijo/tellive-py

tellive-py is a Python wrapper for `Telldus Live <http://live.telldus.com/>`_,
"a user friendly service for automating your TellStick connected gear using the
Internet".

* Official home page: https://github.com/erijo/tellive-py
* Python package index: https://pypi.python.org/pypi/tellive-py

Please report any problem as a `GitHub issue report
<https://github.com/erijo/tellive-py/issues/new>`_.

Features
--------

* Includes the script `tellive_core_connector
  <https://github.com/erijo/tellive-py/blob/master/bin/tellive_core_connector>`_
  for connecting a e.g. a Tellstick Duo to Telldus Live without needing Telldus
  Center. Supports both devices and sensors.
* Open source (`GPLv3+
  <https://github.com/erijo/tellive-py/blob/master/LICENSE.txt>`_).

Requirements
------------

* Python 3.2+
* `tellcore-py <https://github.com/erijo/tellcore-py>`_
* On Mac OS X, `appnope <https://pypi.python.org/pypi/appnope>`_ is
  recommended.

Installation
------------

.. code-block:: bash

    $ pip install tellive-py

Example
-------

To run the included program for connecting a TellStick to Telldus Live:

.. code-block:: bash

    $ tellive_core_connector ~/.config/tellive.conf

The first time you run the program (with a particular config file), it will
exit and ask you to visit a given URL to give the program access to your
account.

When you have done so, you can then edit the config file
(``~/.config/tellive.conf`` in this example) and add a name to the sensors that
you wish to send to Telldus Live. You can also disable devices that you don't
want to be controllable via Telldus Live (see ``tellive_core_connector --help``
for more info). Then start the program again as above.

The API can also be used by your own program. This how you would connect to
Telldus Live and register the client (with PUBLIC_KEY and PRIVATE_KEY from
`here <http://api.telldus.com/keys/index>`_):

.. code-block:: python

    client = TellstickLiveClient(PUBLIC_KEY, PRIVATE_KEY)
    (server, port) = client.connect_to_first_available_server()
    client.register(version="0.1")


Changelog
=========

0.5.2 (2014-11-25)
------------------

* Correctly handle last sent value when it is 0.


0.5.1 (2014-11-20)
------------------

* Don't try to start browser automatically during first run. In many cases it
  doesn't work and may hide the URL.
* Handle last_sent_value() returning None (issue #4).


0.5.0 (2014-11-19)
------------------

* Disable appnap on Mac OS X if appnope module is available (issue #2).
* Report new/changed/removed devices to Telldus live.
* Release socket(s) before waiting to re-connect.
* Require tellcore-py >= v1.1.0.


0.4.2 (2014-02-25)
------------------

* Fixed problem that could occur after disconnect from server.
* Fixed tellive_core_connector problem on Mac OS X (issue #1).


0.4.1 (2014-02-06)
------------------

* Add all sensors and devices to the config on the first run.


0.4.0 (2014-02-06)
------------------

* Fixed tellive_core_connector to not wake up two times every second, but
  instead only wake up when there is work to do.


0.3.0 (2014-02-04)
------------------

* Removed reload message as it is not supposed to be sent to clients.
* Better values for os and os-version in register message.
* Support marking devices as disabled to not show up in Telldus Live.


0.2.0 (2014-02-02)
------------------

* tellive_core_connector now uses official keys from Telldus, so you no longer
  need to use private tokens.
* Log using the standard logging module.
* Reconnect if connection is lost for some reason.
* Fixed problem with Python 3.2.
* Added support for reload request from server.
* Only report sensors that are named in the config file.


0.1.1 (2014-01-28)
------------------

* Fix some packaging issues.


0.1.0 (2014-01-28)
------------------

* Initial release.


%prep
%setup -n %{name}-%{unmangled_version}

%build
python3 setup.py build

%install
python3 setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
