%define name tellprox
%define version 0.28_20140710_f1461664
%define unmangled_version f1461664020cd555567971068b577360a821b348
%define release 1

Summary: Python API to replicate Telldus Live
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GPLv3
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
Vendor: Pete Cracknell <p3tecracknell@gmail.com>
Url: https://github.com/p3tecracknell/tellprox

BuildRequires: python
BuildRequires: python-setuptools

Requires: python
Requires: tellcore-py
Requires: python-beaker
Requires: python-bottle
Requires: python-cherrypy
Requires: python-configobj
Requires: python-werkzeug

Requires(pre):	shadow-utils
Requires(pre):	telldus-core

%description
A local server to use in place of Tellstick Live. Initially based on
remotestick-server (https://github.com/pakerfeldt/remotestick-server)

Trello: https://trello.com/b/YAE4Zk9h

Run with:

$python -m tellprox

Authentication is not set by default. To turn it on set the username
and password in the config page.


%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
install -d -m 0755 $RPM_BUILD_ROOT/etc/tellprox
install -m 0640 configspec.ini $RPM_BUILD_ROOT/etc/tellprox/

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group tellprox >/dev/null || groupadd -r tellprox
getent passwd tellprox >/dev/null || \
    useradd -r -g tellprox -d / -s /sbin/nologin \
    -c "Tellprox user" tellprox
# Make us member of telldusd group for access to telldusd.
getent group telldusd | grep -q tellprox || usermod -a -G telldusd tellprox
exit 0

%files -f INSTALLED_FILES
%defattr(-,root,root)
%dir %attr(0770,root,tellprox) /etc/tellprox
%config(noreplace) %attr(0640,root,tellprox) /etc/tellprox/configspec.ini
%ghost %attr(0640,tellprox,tellprox) /etc/tellprox/config.ini
