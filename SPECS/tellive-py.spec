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
BuildArch: noarch
Vendor: Erik Johansson <erik@ejohansson.se>
Url: https://github.com/erijo/tellive-py

%description
tellive-py is a Python wrapper for `Telldus Live <http://live.telldus.com/>`,
"a user friendly service for automating your TellStick connected gear
using the Internet".

* Official home page: https://github.com/erijo/tellive-py
* Python package index: https://pypi.python.org/pypi/tellive-py

Please report any problem as a `GitHub issue report
<https://github.com/erijo/tellive-py/issues/new>`.

Features
--------

* Includes the script `tellive_core_connector
  <https://github.com/erijo/tellive-py/blob/master/bin/tellive_core_connector>`
  for connecting a e.g. a Tellstick Duo to Telldus Live without needing Telldus
  Center. Supports both devices and sensors.
* Open source (`GPLv3+
  <https://github.com/erijo/tellive-py/blob/master/LICENSE.txt>`).

Example
-------

To run the included program for connecting a TellStick to Telldus Live:

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
`here <http://api.telldus.com/keys/index>`):

    client = TellstickLiveClient(PUBLIC_KEY, PRIVATE_KEY)
    (server, port) = client.connect_to_first_available_server()
    client.register(version="0.1")


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
