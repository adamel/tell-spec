CentOS/RHEL/Fedora RPMs for TellStick
=====================================

This repository contains spec files to build RPMs of the following
TellStick software:

* telldus-core https://developer.telldus.com/wiki/TellStickInstallationSource
* tellcore-py https://github.com/erijo/tellcore-py
* tellprox https://github.com/p3tecracknell/tellprox
* tellive-py https://github.com/erijo/tellive-py

Supported distributions
-----------------------

I run these RPMs on CentOS 7 with my TellStick Duo, so this is where
the packages are actually tested. I also verify that the packages
build on Fedora 24 and Fedora 25, but don't have any such system to
test on.

The packages use systemd to implement services, so you will not be
able to build or use them on CentOS/RHEL 5/6 without modification.

Requirements
------------

To build the source RPMs you need the make, wget and rpm-build
packages. Install them using:

    sudo yum install make wget rpm-build

on CentOS/RHEL, or if on Fedora:

    sudo dnf install make wget rpm-build

The recommended way to build binary RPMs is to use mock. To install it
on CentOS/RHEL use:

    sudo yum install epel-release -y
    sudo yum install mock

and to install it on Fedora use:

    sudo dnf install mock

To be able to use mock you need to have a user who is a member of the
`mock` group. **IMPORTANT** - any user who is a member of the mock
group have full root privleges on the system, and can do anything they
want with it. To add a user with username $USER to the mock group,
run:

    sudo usermod -a -G mock $USER

Build
-----

If the requirements are fulfilled you should be able to build source
RPMs by simply running:

    make srpms

If this is the first time it is run the Makefile will use wget to
download tar files with the upstream source, and then verify the
sha256 checksum against the ones listed in sources.sha256

If you then want to build binary RPMs for CentOS/RHEL using mock you
run:

    make mockbuild

To build RPMs for Fedora 25 using mock run:

    make mockbuild DIST=fedora-25-$(uname -m)
