%define name tellprox
%define version 0.28
%define unmangled_version 0.28
%define unmangled_version 0.28
%define release 1

Summary: Python API to replicate Telldus Live
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: LICENSE.txt
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Pete Cracknell <p3tecracknell@gmail.com>
Url: https://github.com/p3tecracknell/tellprox

%description
tellprox
========

A local server to use in place of Tellstick Live. Initially based on remotestick-server (https://github.com/pakerfeldt/remotestick-server)

Trello: https://trello.com/b/YAE4Zk9h

Requirements
============
You will need telldus-core. On Windows it comes with TelldusCenter:
http://www.telldus.se/products/nativesoftware

There are instructions online for installing telldus-core on Mac/Linux. For example, to install on Raspbian:
http://elinux.org/R-Pi_Tellstick_core

To install Telldus-core on OpenWRT, follow:
http://blog.stfu.se/binary-openwrt-packages-for-telldus-core/

Essentially: opkg install [url]

Installation
============

Make sure python is installed (windows: http://www.activestate.com)

Download the source:

--Windows users, click on 'Download Zip' and extract.

--Linux users should install git and setuptools, for example:

--$sudo apt-get update

--$sudo apt-get install python-setuptools git

--$git clone git://github.com/p3tecracknell/tellprox.git

Then open a command prompt in the source and type:

$sudo python setup.py install

Finally, run with:

$python -m tellprox

Authentication is not set by default. To turn it on set the username and password in the config page


%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
