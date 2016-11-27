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
tellcore-py is a Python wrapper for `Telldus' <http://www.telldus.com/>`
home automation library `Telldus Core <http://developer.telldus.se/doxygen/>`.

* Documentation: https://tellcore-py.readthedocs.org/
* Official home page: https://github.com/erijo/tellcore-py
* Python package index: https://pypi.python.org/pypi/tellcore-py

Please report any problem as a `GitHub issue report
<https://github.com/erijo/tellcore-py/issues/new>`.

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
