%define name tellive-py
%define version 0.5.2
%define unmangled_version 0.5.2
%define release 2

Summary: Python wrapper for connecting to Telldus Live
Name: %{name}
Version: %{version}
Release: %{release}%{?dist}
Source0: %{name}-%{unmangled_version}.tar.gz
Source1: tellive.service
Patch10: tellive-py-0.5.2-report-switches.patch
License: GPLv3+
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
Vendor: Erik Johansson <erik@ejohansson.se>
Url: https://github.com/erijo/tellive-py

%if 0%{?rhel}
BuildRequires: python34
%else
BuildRequires: python3
%endif
BuildRequires: systemd
%{?systemd_requires}

Requires(pre):	shadow-utils
Requires(pre):	telldus-core

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
%patch10 -p1

%build
python3 setup.py build

%install
python3 setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
install -m 0644 -D %SOURCE1 $RPM_BUILD_ROOT%{_unitdir}/tellive.service
install -d -m 0755 $RPM_BUILD_ROOT/etc/tellive
touch $RPM_BUILD_ROOT/etc/tellive/tellive.conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group tellive >/dev/null || groupadd -r tellive
getent passwd tellive >/dev/null || \
    useradd -r -g tellive -d / -s /sbin/nologin \
    -c "Tellive user" tellive
# Make us member of telldusd group for access to telldusd.
getent group telldusd | grep -q tellive || usermod -a -G telldusd tellive
exit 0

%post
%systemd_post tellive.service

%preun
%systemd_preun tellive.service

%postun
%systemd_postun_with_restart tellive.service

%files -f INSTALLED_FILES
%defattr(-,root,root)
%{_unitdir}/tellive.service
%dir %attr(0750,tellive,tellive) /etc/tellive
%config(noreplace) %attr(0640,tellive,tellive) %verify(not md5 mtime size) /etc/tellive/tellive.conf

%changelog
* Sun Nov 27 2016 Marcus Sundberg <marcus@marcussundberg.com> - 0.5.2-2
- Fix typo to make tellive report state for switches.

* Sun Nov 27 2016 Marcus Sundberg <marcus@marcussundberg.com> - 0.5.2-1
- Initial packaging.
