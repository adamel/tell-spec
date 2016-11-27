# This spec file is originally licensed under:
# The MIT License (MIT)
# Copyright (c) 2010-2016 Mageia.Org
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

%define	major 2
%define	libname	libtelldus-core%{major}
%define	devname	libtelldus-core-devel

Summary:	TellStick controlling library
Name:		telldus-core
Version:	2.1.2
Release:	3.ts1%{?dist}
License:	LGPLv2.1+
Group:		System/Boot and Init
URL:		http://developer.telldus.se
Source0:	http://download.telldus.se/TellStick/Software/telldus-core/%{name}-%{version}.tar.gz
#Source0:	http://download.telldus.se/debian/pool/unstable/telldus-core_%{version}.orig.tar.gz
Source1:	Doxyfile.in
Source2:	telldusd.service
Patch0:		telldus-core-2.1.1-run-under-dedicated-user.diff
Patch1:		telldus-core-2.1.2_rc1-linkage_fix.diff
Patch2:		telldus-core-2.1.2-socket_dir.diff
Patch3:		0001-Only-create-the-socket-once.-If-we-fail-to-connect-i.patch
Patch4:		telldus-core-2.1.2-libftdi1.diff
Patch100:	telldus-core-2.1.2-narrowing-conversions.patch
BuildRequires:	pkgconfig(libftdi1)
BuildRequires:	pkgconfig(libconfuse)
BuildRequires:	cmake
BuildRequires:	doxygen help2man
BuildRequires:	systemd-units
%{?systemd_requires}
Requires(pre):	shadow-utils

%description
Telldus Core is the driver and tools for controlling a Telldus Technologies
TellStick. It does not containing any GUI tools which makes it suitable for
server use.
This package contains the tools.

%package -n	%{libname}
Summary:	Library for telldus-core
Group:		System/Libraries

%description -n	%{libname}
Telldus Core is the driver and tools for controlling a Telldus Technologies
TellStick. It does not containing any GUI tools which makes it suitable for
server use.
This package contains the library.

%package -n	%{devname}
Summary:	Development files for developing programs against telldus-core
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}

%description -n	%{devname}
Telldus Core is the driver and tools for controlling a Telldus Technologies
TellStick. It does not containing any GUI tools which makes it suitable for
server use.
This package contains development files for creating applications using
Telldus Core.

%prep

%setup -q
cp %{SOURCE1} .
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p2
%patch4 -p1
%patch100 -p2

perl -pi -e "s|/etc/udev/rules.d|%{_udevrulesdir}|g" tdadmin/CMakeLists.txt
perl -pi -e "s|%{_localstatedir}/state|%{_localstatedir}/lib/telldusd|g" service/CMakeLists.txt

%build
%cmake \
    -DGENERATE_MAN:BOOL=ON \
    -DSCRIPT_PATH="%{_datadir}/telldus/scripts"

make telldusd %{?_smp_mflags}
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

install -d %{buildroot}%{_unitdir}
install -m0644 %{SOURCE2} %{buildroot}%{_unitdir}/telldusd.service

install -d %{buildroot}%{_datadir}/telldus/scripts
for i in controllerevent devicechangeevent deviceevent rawdeviceevent sensorevent; do
cat > %{buildroot}%{_datadir}/telldus/scripts/$i << EOF
#!/bin/sh
# add something interesting to do for the $i trigger here
EOF
done

install -d %{buildroot}%{_localstatedir}/lib/telldusd

%pre
getent group telldusd >/dev/null || groupadd -r telldusd
getent passwd telldusd >/dev/null || \
	useradd -r -g telldusd -d %{_localstatedir}/lib/telldusd -s /bin/bash \
	-c "telldusd service user" telldusd
exit 0

%post
%systemd_post telldusd.service

%preun
%systemd_preun telldusd.service

%postun
%systemd_postun_with_restart telldusd.service

%files
%doc AUTHORS README
%attr(0640,telldusd,telldusd) %config(noreplace) %{_sysconfdir}/tellstick.conf
%{_udevrulesdir}/05-tellstick.rules
%{_unitdir}/telldusd.service
%{_bindir}/tdtool
%{_sbindir}/tdadmin
%{_sbindir}/telldusd
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/helpers/
%{_datadir}/%{name}/helpers/udev.sh
%dir %{_datadir}/telldus/scripts
%attr(0755,root,root) %config(noreplace) %{_datadir}/telldus/scripts/deviceevent
%attr(0755,root,root) %config(noreplace) %{_datadir}/telldus/scripts/devicechangeevent
%attr(0755,root,root) %config(noreplace) %{_datadir}/telldus/scripts/rawdeviceevent
%attr(0755,root,root) %config(noreplace) %{_datadir}/telldus/scripts/sensorevent
%attr(0755,root,root) %config(noreplace) %{_datadir}/telldus/scripts/controllerevent
%attr(0755,telldusd,telldusd) %dir %{_localstatedir}/lib/telldusd
%attr(0644,telldusd,telldusd) %config(noreplace) %{_localstatedir}/lib/telldusd/telldus-core.conf
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{devname}
%{_includedir}/%{name}.h
%{_libdir}/*.so


%changelog
* Sun Nov 27 2016 Marcus Sundberg <marcus@marcussundberg.com> - 2.1.2-3.ts1
- Make it build on EL/Fedora.
- Build man pages from source.
- Make build partly parallel.
- Fix narrowing conversions to make it build on Fedora 25.

* Mon Feb 08 2016 umeabot <umeabot> 2.1.2-3.mga6
+ Revision: 950223
- Mageia 6 Mass Rebuild

* Sat Oct 25 2014 oden <oden> 2.1.2-2.mga5
+ Revision: 793163
- really fix build
- P4: fix build (libftdi1)
- fix deps
- also add the patch
- P3:  Only create the socket once. If we fail to connect is we should try to reuse it later.
- various fixes
- fix group
- various fixes
- imported package telldus-core

